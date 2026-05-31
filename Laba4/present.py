class Journal:
    def __init__(self):
        # Структура map (словаря): {id: {'name': 'Имя', 'grades': [5, 4, ...]}, ...}
        self.students = {}
        self.next_id = 1

    def add_student(self):
        """Добавление студента в журнал"""
        name = input("\nВведите имя студента: ").strip()
        if not name:
            print("Имя не может быть пустым!")
            return
            
        self.students[self.next_id] = {'name': name, 'grades': []}
        print(f"Студент '{name}' успешно добавлен! Его ID: {self.next_id}")
        self.next_id += 1

    def add_grade(self):
        """Выставление балла"""
        identifier = input("\nВведите ID или имя студента: ").strip()
        student_id = self._find_student_id(identifier)
        
        if not student_id:
            print("Студент не найден!")
            return
            
        try:
            grade = int(input(f"Введите оценку для {self.students[student_id]['name']}: "))
            self.students[student_id]['grades'].append(grade)
            print("Оценка успешно добавлена!")
        except ValueError:
            print("Ошибка: Оценка должна быть числом!")

    def show_student_grades(self):
        """Получение баллов по имени или ID"""
        identifier = input("\nВведите ID или имя студента: ").strip()
        student_id = self._find_student_id(identifier)
        
        if not student_id:
            print("Студент не найден!")
            return
            
        student = self.students[student_id]
        grades_str = ", ".join(map(str, student['grades'])) if student['grades'] else "нет оценок"
        print(f"[{student_id}] {student['name']} | Оценки: {grades_str}")

    def show_all(self):
        """Вывод всех студентов и их результатов"""
        print("\n" + "="*50)
        print("ЭЛЕКТРОННЫЙ ЖУРНАЛ".center(50))
        print("="*50)
        
        if not self.students:
            print("Журнал пуст.")
        else:
            print(f"{'ID':<4} | {'Имя':<15} | {'Оценки'}")
            print("-" * 50)
            for sid, data in self.students.items():
                grades_str = ", ".join(map(str, data['grades'])) if data['grades'] else "нет"
                print(f"{sid:<4} | {data['name']:<15} | {grades_str}")
        print("="*50)

    def _find_student_id(self, identifier):
        """Вспомогательный метод для поиска ID студента по имени или ID"""
        # Поиск по ID
        if identifier.isdigit() and int(identifier) in self.students:
            return int(identifier)
            
        # Поиск по имени (без учета регистра)
        for sid, data in self.students.items():
            if data['name'].lower() == identifier.lower():
                return sid
                
        return None

    def menu(self):
        """Главное меню системы"""
        while True:
            print("\n" + "─"*30)
            print("МЕНЮ".center(30))
            print("─"*30)
            print("1. Добавить ученика")
            print("2. Поставить оценку")
            print("3. Поиск оценок ученика")
            print("4. Показать весь журнал")
            print("0. Выйти")
            
            choice = input("\nВыберите действие: ").strip()
            
            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.add_grade()
            elif choice == '3':
                self.show_student_grades()
            elif choice == '4':
                self.show_all()
            elif choice == '0':
                print("Работа завершена. До свидания!")
                break
            else:
                print("Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    journal = Journal()
    journal.menu()