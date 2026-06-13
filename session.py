from colorama import init, Fore, Style
init()

from time import sleep


# Задачи на 25 
def bubиle(mass:list)->list: 
    """Реализовать сортировку пузырьком для массива чисел. Необходимо не просто отсортировать
    массив, но и вывести массив после каждого прохода алгоритма, чтобы было видно, как
    элементы постепенно «всплывают»."""
    for i in range(len(mass)-1):
        for j in range(len(mass)-i-1):
            if mass[j] > mass[j+1]: 
                print(*mass[:j],Fore.RED + str(mass[j]), str(mass[j+1]) + Style.RESET_ALL, *mass[j+2:])
                temp = mass[j]
                mass[j] = mass[j+1]
                mass[j+1] = temp       
    return mass

def is_mass_increasing(mass:list)->bool:
    """Проверить, отсортирован ли массив по возрастанию. Программа должна работать без
    использования встроенных функций сортировки."""
    for i in range(len(mass)-1):
        if mass[i] > mass[i+1]: 
            return False
    return True

def second_max(mass:list):
    """Найти второй по величине элемент массива без сортировки всего массива. Нужно придумать
    эффективный алгоритм за один проход."""
    max1 = max(mass[0],mass[1])
    max2 =  min(mass[0],mass[1])

    count = 1
    while(max1==max2 and count<len(mass)):
        if mass[count] != max1:
            max1 = max(mass[0],mass[count])
            max2 =  min(mass[0],mass[count])
        count+=1

    for i in range(len(mass)):
        if (mass[i] > max1):
            max2 = max1
            max1 = mass[i]
         
    return max2 

def search(mass:list, num:int)->int:
    """Реализовать линейный поиск элемента в массиве. Если элемент найден — вывести его индекс,
    иначе сообщить, что элемента нет."""
    for i in range(len(mass)):
        if mass[i] == num: return i
    return None

class Stek:
    """Реализовать простейший стек на массиве с операциями push, pop и top"""
    def __init__(self):
        self.stek = []
        self.count = 0

    def push(self,num:int):
        self.stek = [num] + self.stek
        self.count+=1
    
    def pop(self):
        pop = self.stek[0]
        self.stek = self.stek[1:]
        self.count-=1
        return pop
    
    def top(self):
        return self.stek[0] 
    
    def prin(self): 
        print(self.stek)

class Queue:
    """Реализовать очередь на массиве с операциями enqueue и dequeue"""
    def __init__(self):
        self.stek = []
        self.count = 0

    def enqueue(self,num:int):
        self.queue += [num] 
        self.count+=1
    
    def dequeue(self):
        pop = self.queue[self.count-1]
        self.queue = self.queue[:self.count-1]
        self.count-=1
        return pop
    
    def prin(self): 
        print(self.queue)

def correctness_brackets(stroka:str)->bool:
    """Проверить корректность расстановки круглых и квадратных скобок в выражении с помощью стека."""
    proverka = list(
        map( str,stroka )
    )
    

    brackets = {
        "]" : "[",
        ")" : "(",
        "}" : "{"
    }

    stek = []
    for el in proverka:
        if el in ["[", "(", "{"]:
            stek = [el] + stek
        else: 
            if stek.pop(0) != brackets[el]:
                return False
    return len(stek)==0

def chenge_money(summa:int, s = 0, ans = [])->list:
    """Разменять сумму минимальным количеством монет для номиналов 1, 2, 5 и 10. Нужно
    реализовать жадный алгоритм."""
    if s+10 <= summa: return  chenge_money(summa,s+10,ans+[10]) 
    if s+5 <= summa: return chenge_money(summa,s+5,ans+[5])
    if s+2 <= summa:  return chenge_money(summa,s+2,ans+[2])
    if s+1 <= summa:  return chenge_money(summa,s+1,ans+[1]) 
    return ans 

def meet(mass:list)->int:
    """Выбрать максимальное количество непересекающихся встреч. Каждая встреча задаётся
    временем начала и конца."""

    time = [] # Собирем сюда значений начала и конча в минутах каждого из мироприятий
    for el in mass:
        start, end = el 
        time.append(
            (
                list(map(int,start.split(":")))[0]*60 + list(map(int,start.split(":")))[1], 
                list(map(int,end.split(":")))[0]*60 + list(map(int,end.split(":")))[1] 
            )
        )


    # ВАРИАНТ 1 - берём те, которые занимают меньще всего времени 
    print(time)
    delta_time = [i[1]-i[0] for i in time]
    posetil = []
    # проверяем все встречи, сначала выбирая самы короткие 
    while (delta_time):
        index_min_time_for_vstr = delta_time.index(min(delta_time))
        vstr = time [ index_min_time_for_vstr ]
        delta_time.pop( index_min_time_for_vstr )
        flag = True
        for el in posetil:
            if not(vstr[0] > el[1]) or (vstr[1] < el[0]): # Проходимся по всем занятым всттечам и проверяем, что можем попасть на эту встречу 
                flag = False # типа она должна или начинаться позже, чем другая заканчивается 
                break    # или закончится раньше, чем другая начнётся 
        if flag:
            posetil.append(vstr)

    # Для запуска и проверки 
    # print(
    #         meet(
    #            [
    #             ["12:34", "16:12"],
    #             ["09:00", "10:30"], 
    #             ["14:00", "15:45"], 
    #             ["10:00", "11:15"], 
    #             ["16:00", "17:30"]
    #         ]
    #         )
    #     )
    return len(posetil)



# Задачи на 35 
def hanoe(n,i,j):
    if n == 1:
        print("Диск 1 переложить с",i,"на", j)
    else:
        tmp = 6 - i - j
        hanoe(n-1,i,tmp)
        print("Диск", n, "переложить с",i,"на", j )
        hanoe(n-1,tmp, j)

def QuikSort(mass):
    """Реализовать Quick Sort. Необходимо самостоятельно выбрать способ выбора pivot и
    объяснить, как он влияет на производительность."""
    if len(mass)<=1:
        return mass
    else:
        piv = mass[0]
        pivot = [i for i in mass if piv==i]
        bol = [i for i in mass if piv<i]
        men  = [i for i in mass if piv>i]
        print(men, pivot,bol)
        return QuikSort(men) + pivot + QuikSort(bol)

def Merge(mass1, mass2):
    ans = [] 
    i,j = 0,0
    while (i+j != len(mass1)+len(mass2)):
        if i<len(mass1) and j<len(mass2):
            if mass1[i]<mass2[j]:
                ans.append(mass1[i])
                i+=1
            else:
                ans.append(mass2[j])
                j+=1
        elif i>len(mass1):
            ans.append(mass2[j])
            j+=1
        else:
            ans.append(mass1[i])
            i+=1
    return ans 

def MergeSort(mass):
    """Реализовать Merge Sort. Дополнительно вывести количество операций слияния массивов"""
    if len(mass)<=1:
        return mass
    else:
        mid = len(mass)//2
        mass1 = MergeSort( mass[:mid] )
        mass2 = MergeSort ( mass[mid:] )
        return Merge (mass1, mass2)
        
def BinSearch(mass, num):
    """Реализовать рекурсивный бинарный поиск. Программа должна корректно обрабатывать
    случай отсутствия элемента."""
    if len(mass)==1:
        if mass[0]==num:
            return True
        return False
    else:
        mid = len(mass)//2
        if mass[mid] == num:
            return True
        elif mass[mid]>num:
            return BinSearch(mass[:mid],num)
        else: 
            return BinSearch(mass[mid+1:], num ) 

class Patrt():
    """Реализовать односвязный список с операциями вставки, удаления и поиска элемента"""
    def __init__(self, value = None):
        self.value = value
        self.next = None

class ListSimpl():
    def __init__(self):
        self.head = None

    def put(self, value):
        if self.head is None: 
            self.head = Patrt(value)
        else: 
            temp = self.head
            while (temp.next is not None): 
                temp = temp.next
            temp.next = Patrt(value)
        return 0 
            
    def delete(self, value):
        if self.head.value == value:
            self.head = self.head.next
        else:
            post_chek = self.head
            chek = self.head.next 
            while post_chek.next is not None and post_chek.next.value != value:
                post_chek = post_chek.next

            if post_chek.next is None:
                return -1
            else:
                post_chek.next = post_chek.next.next
        return 0 
                
    def search(self, value):
        chek = self.head
        while chek is not None and chek.value != value:
            chek = chek.next
        return chek if chek is not None else -1

class Ochered:
    """Реализация очереди через два стека."""
    def __init__(self):
        self.in_stak = []
        self.out_stak = []

    def __bool__(self):
        return bool(self.in_stak or self.out_stak)

    def append_to_stak(self, value):
        self.in_stak.append(value)

    def pop_in_stak(self):
        if not self:
            return -1

        if not self.out_stak:
            while self.in_stak:
                self.out_stak.append(self.in_stak.pop())

        return self.out_stak.pop()
    
class StekMin():
    """Реализовать стек с поддержкой получения минимального элемента за O(1)."""
    def __init__(self):
        self.stek = []
        self.count = 0
    
    def put(self,value):
        if self.count == 0:
            self.stek.append(
                (value,value)
            )
        else:
            self.stek.append(
                (value,min(value,self.stek[-1][1]))
            )
    def take(self):
        return self.stek.pop(-1)[0]
    
    def take_min_num(self):
          return self.stek.pop(-1)

def dijkstra_matrix(matrix, start):
    """Реализовать алгоритм Дейкстры для поиска кратчайшего пути во взвешенном графе. Нужно
    вывести не только расстояние, но и сам путь."""

    n = len(matrix)
    dist = [float("inf")]*n
    dist[start] = 0
    posetil = [False]*n
    prev = [-1] * n

    for _ in range(n):
            min_ves = float("inf")
            u = -1 
            for i in range(n):
                if (not posetil[i]) and (dist[i] < min_ves):
                    u = i
                    min_ves = dist[i]
                
            if u == -1:
                break

            posetil[u] = True

            for j in range(n):
                ves = matrix[u][j] 
                if ves!=0:
                    if dist[u] + ves < dist[j]:
                        prev[j] = u
                        dist[j] = dist[u] + ves

          
            paths = []
            for v in range(n):
                if dist[v] == float("inf"):
                    paths.append(None)   # нет пути
                else:
                    cur = v
                    path = []
                    while cur != -1:
                        path.append(cur)
                        cur = prev[cur]
                    path.reverse()
                    paths.append(path)

    return dist, prev 

def algoritm_prima(matrix):

    unvisited = [i for i in range(len(matrix))]
    visited = []
    edges = {}

    while ( unvisited ):
        if len(visited) == 0:
            rebro = unvisited.pop(0)
            visited.append(rebro)
            sosede = [i for i in range(len(matrix)) if matrix[rebro][i] > 0] # Номер соседа в матрице, который подходит 
            min_sosed = float("inf")
            u = -1
            for i in sosede:
                if min_sosed > matrix[rebro][i]:
                    min_sosed = matrix[rebro][i]
                    u = i 
            if u != -1 and u in unvisited:
                unvisited.remove(u)
                visited.append(u)
            edges[(rebro, u)] = min_sosed

        else: 
            sosede = [] # Номер соседа в матрице, который подходит 
            for i in visited:
                for j in range(len(matrix)):
                    if (matrix[i][j] > 0 ) and (j not in  visited) and (j not in  sosede):
                        sosede.append(j)

            min_sosed = float("inf")
            u = -1
            dad = -1

            for i in visited:
                for j in  sosede:
                    if min_sosed > matrix[i][j] and matrix[i][j] > 0:
                        min_sosed = matrix[i][j]
                        dad = i 
                        u = j 
            
            if u != -1 and u in unvisited:
                unvisited.remove(u)
                visited.append(u)
            edges[(dad, u)] = min_sosed
         
    return edges


if __name__ == "__main__":
    matrix= ((0, 3, 1, 3, 0, 0),
             (3, 0, 4, 0, 0, 0),
             (1, 4, 0, 0, 7, 5),
             (3, 0, 0, 0, 0, 2),
             (0, 0, 7, 0, 0, 4),
             (0, 0, 5, 2, 4, 0)) 
    

    print(
        algoritm_prima(matrix)
    )

    print(
         bubиle( [9,8,7,6,5,4,3,2,1] ) 

    )






