import sqlite3 as sq
import hashlib
import getpass

class Journal:
    def __init__(self, name = 'school'):
        self.conn = sq.connect(f"journal-{name}.db")
        self.login = ""  
        self.cur = self.conn.cursor()
        self.bootstrap_db()

    def bootstrap_db(self):
        """Создание таблиц и добавление стандартного админа"""
        self.cur.executescript("""
            CREATE TABLE IF NOT EXISTS teachers (
                login TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login_teacher TEXT,
                name TEXT NOT NULL,
                sername TEXT NOT NULL,
                class_num INTEGER,
                class_letter TEXT,
                FOREIGN KEY (login_teacher) REFERENCES teachers(login)
            );

            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                grade INTEGER NOT NULL,
                date DATE DEFAULT CURRENT_DATE,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            );
        """)
        
        # создание админки, для первого входа 
        self.cur.execute("SELECT COUNT(*) FROM teachers")
        if self.cur.fetchone()[0] == 0:
            admin_hash = hashlib.sha256("admin".encode()).hexdigest()
            self.cur.execute("INSERT INTO teachers (login, password_hash) VALUES (?, ?)", 
                           ("admin", admin_hash))
            self.conn.commit()

    def register_teacher(self):
        """Регистрация нового преподавателя"""
        print("\n" + "="*30)
        print("РЕГИСТРАЦИЯ ПРЕПОДАВАТЕЛЯ")
        print("="*30)
        
        login = input("Придумайте логин: ").strip()
        if not login:
            print("Логин не может быть пустым!")
            return False
        
        # Проверяем, существует ли уже такой логин
        self.cur.execute("SELECT login FROM teachers WHERE login = ?", (login,))
        if self.cur.fetchone():
            print(f"Преподаватель с логином '{login}' уже существует!")
            return False
        
        password = getpass.getpass("Придумайте пароль: ")
        if not password:
            print("Пароль не может быть пустым!")
            return False
        
        confirm_password = getpass.getpass("Подтвердите пароль: ")
        if password != confirm_password:
            print("Пароли не совпадают!")
            return False
        
        try:
            pass_hash = hashlib.sha256(password.encode()).hexdigest()
            self.cur.execute("INSERT INTO teachers (login, password_hash) VALUES (?, ?)", 
                           (login, pass_hash))
            self.conn.commit()
            
            print(f"\nПреподаватель '{login}' успешно зарегистрирован!")
            return True
        except Exception as e:
            print(f"Ошибка при регистрации: {e}")
            self.conn.rollback()
            return False

    def login_teacher(self):  
        """Авторизация учителя"""
        print("\n" + "="*30 + "\nВХОД В СИСТЕМУ\n" + "="*30)
        print("1. Войти")
        print("2. Зарегистрироваться")
        print("3. Выйти")
        
        choice = input("\nВыберите действие: ").strip()
        
        if choice == '2':
            if self.register_teacher():
                # После регистрации возвращаемся к меню входа
                return self.login_teacher()
            else:
                return self.login_teacher()
        elif choice == '3':
            return 'stop'
        
        # Обычный вход
        login = input("\nЛогин: ").strip()
        if login == '':
            return 'stop'
        
        password = getpass.getpass("Пароль: ")
        pass_hash = hashlib.sha256(password.encode()).hexdigest()

        self.cur.execute("SELECT * FROM teachers WHERE login = ? AND password_hash = ?", (login, pass_hash))
        if self.cur.fetchone():
            print(f"\n Успешный вход! Добро пожаловать, {login}.")
            self.login = login
            return True
        
        print("\nНеверный логин или пароль!")
        return False

    def show_current_profile(self):
        """Просмотр данных текущего преподавателя"""
        self.cur.execute("""
            SELECT DISTINCT class_num, class_letter 
            FROM students 
            WHERE login_teacher = ?
        """, (self.login,))
        rows = self.cur.fetchall()
        
        print("\n" + "-"*30)
        print("ТЕКУЩИЙ ПРОФИЛЬ:")
        print("-"*30)
        print(f"Пользователь: {self.login}")
        
        if rows:
            class_list = [f"{row[0]}{row[1]}" for row in rows if row[0] and row[1]]
            print(f"Ваш класс: {', '.join(class_list)}")
        else:
            print("Ваш класс: Не закреплён")
        print("-"*30)

    def ret_cur(self): 
        return self.cur 

    def _get_student_by_identifier(self, identifier):
        """Вспомогательный метод: ищет студента по ID, имени или фамилии"""
        if identifier.isdigit():
            self.cur.execute("SELECT id, name, sername FROM students WHERE id = ?", (int(identifier),))
        else:
            self.cur.execute("""
                SELECT id, name, sername FROM students 
                WHERE name LIKE ? OR sername LIKE ?
            """, (f"%{identifier}%", f"%{identifier}%"))
        return self.cur.fetchall()

    def add_student(self):
        """Добавление студента в журнал"""
        print("\n" + "-"*30)
        print("ДОБАВЛЕНИЕ СТУДЕНТА")
        print("-"*30)
        
        if not self.login:
            print("Ошибка: вы не авторизованы!")
            return
        
        # Ввод данных
        name = input("Введите имя студента: ").strip()
        surname = input("Введите фамилию студента: ").strip()
        class_num = input("Введите номер класса: ").strip()
        class_letter = input("Введите букву класса: ").strip().upper()
        
        if not name or not surname:
            print("Ошибка: имя и фамилия не могут быть пустыми!")
            return
        
        if not class_num or not class_letter:
            print("Ошибка: класс не может быть пустым!")
            return
        
        try:
            self.cur.execute("""
                INSERT INTO students (login_teacher, name, sername, class_num, class_letter) 
                VALUES (?, ?, ?, ?, ?)
            """, (self.login, name, surname, class_num, class_letter))
            
            self.conn.commit()
            student_id = self.cur.lastrowid
            
            print(f"\nСтудент успешно добавлен!")
            print(f"   ID: {student_id}")
            print(f"   Имя: {name}")
            print(f"   Фамилия: {surname}")
            print(f"   Класс: {class_num}{class_letter}")
            print(f"   Учитель: {self.login}")
            
        except Exception as e:
            print(f" Ошибка при добавлении студента: {e}")
            self.conn.rollback()

    def add_grade(self):
        """Выставление балла"""
        identifier = input("\nВведите ID или имя студента: ")
        matches = self._get_student_by_identifier(identifier)

        if not matches:
            print(" Студент не найден!")
            return
        elif len(matches) > 1:
            print("⚠ Найдено несколько студентов, уточните ID:")
            for sid, name, sername in matches:
                print(f"   [{sid}] {sername} {name}")
            return

        student_id, name, sername = matches[0]
        try:
            grade = int(input(f"Введите оценку для {sername} {name} (2-5): "))
            if grade < 2 or grade > 5:
                print(" Оценка должна быть от 2 до 5!")
                return
                
            self.cur.execute("INSERT INTO grades (student_id, grade) VALUES (?, ?)", (student_id, grade))
            self.conn.commit()
            print(f" Оценка {grade} успешно добавлена!")
        except ValueError:
            print(" Оценка должна быть числом!")
        except Exception as e:
            print(f" Ошибка: {e}")

    def show_student_grades(self):
        """Получение баллов по имени или ID"""
        identifier = input("\nВведите ID или имя студента: ")
        matches = self._get_student_by_identifier(identifier)

        if not matches:
            print(" Студент не найден!")
            return

        for student_id, name, sername in matches:
            self.cur.execute("SELECT grade, date FROM grades WHERE student_id = ? ORDER BY date DESC", (student_id,))
            grades_data = self.cur.fetchall()
            
            if not grades_data:
                print(f"[{student_id}] {sername} {name} |  Нет оценок")
            else:
                grades_str = ", ".join([str(g[0]) for g in grades_data])
                print(f"[{student_id}] {sername} {name} | Оценки: [{grades_str}]")

    def show_all(self):
        """Вывод студентов конкретного учителя и их результатов"""
        if not self.login:
            print("Ошибка: вы не авторизованы!")
            return
            
        if self.login == 'admin':
            # Админ видит всех студентов
            self.cur.execute("""
                SELECT s.id, s.name, s.sername, s.class_num, s.class_letter, 
                       GROUP_CONCAT(g.grade, ', ') as grades,
                       ROUND(AVG(g.grade), 2) as avg_grade
                FROM students s
                LEFT JOIN grades g ON s.id = g.student_id
                GROUP BY s.id
                ORDER BY s.class_num, s.class_letter, s.sername
            """)
        else:
            # Учитель видит только своих студентов
            self.cur.execute("""
                SELECT s.id, s.name, s.sername, s.class_num, s.class_letter, 
                       GROUP_CONCAT(g.grade, ', ') as grades,
                       ROUND(AVG(g.grade), 2) as avg_grade
                FROM students s
                LEFT JOIN grades g ON s.id = g.student_id
                WHERE s.login_teacher = ?
                GROUP BY s.id
                ORDER BY s.class_num, s.class_letter, s.sername
            """, (self.login,))
        
        print("\n" + "="*70)
        print("ЭЛЕКТРОННЫЙ ЖУРНАЛ".center(70))
        print("="*70)
        rows = self.cur.fetchall()
        
        if not rows:
            print("В вашем классе пока нет студентов или журнал пуст.")
        else:
            print(f"{'ID':<4} {'Фамилия':<15} {'Имя':<12} {'Класс':<6} {'Оценки':<25} {'Ср.':<5}")
            print("-"*70)
            for row in rows:
                sid, name, sername, class_num, class_letter, grades, avg = row
                class_str = f"{class_num}{class_letter}" if class_num else "-"
                grades_str = str(grades)[:22] + ".." if grades and len(str(grades)) > 22 else (str(grades) if grades else "нет")
                avg_str = str(avg) if avg else "-"
                print(f"{sid:<4} {sername:<15} {name:<12} {class_str:<6} {grades_str:<25} {avg_str:<5}")
        print("="*70)

    def menu(self):
        """Главное меню системы"""
        while True:
            print("\n" + "─"*40)
            print("ГЛАВНОЕ МЕНЮ".center(40))
            print("─"*40)
            print("1. Добавить учеников")
            print("2. Поставить оценку")
            print("3. Поиск оценок ученика")
            print("4. Показать журнал класса")
            print("5. Посмотреть мой профиль")
            print("6. Сменить преподавателя")
            print("0. Выйти из программы")
            
            choice = input("\nВыберите действие: ").strip()
            
            if choice == '1': 
                self.add_student()
            elif choice == '2': 
                self.add_grade()
            elif choice == '3': 
                self.show_student_grades()
            elif choice == '4': 
                self.show_all()
            elif choice == '5': 
                self.show_current_profile()
            elif choice == '6': 
                print(f"\nСессия пользователя {self.login} завершена.")
                self.login = ""
                self.login_teacher()
                return "change_user" 
            elif choice == '0': 
                print("\n До свидания!")
                self.conn.close()
                exit()
                return "exit"
            else:
                print("Неверный выбор!")