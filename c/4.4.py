from sys import maxsize


class Queue:
    # Конструктор нашего класса, в нём происходит нужная инициализация объекта
    def __init__(self, max_size):
        self.max_size = max_size  # размер очереди
        self.task_num = 0  # будем хранить сквозной номер задачи

        self.tasks = [0 for _ in range(self.max_size)]  # инициализируем список с нулевыми элементами
        self.head = 0  # указатель на начало очереди
        self.tail = 0  # указатель на элемент следующий за концом очереди
    
    def is_empty(self):
        return self.head==self.tail==0

    def size(self):
        if self.is_empty(): return 0
        elif self.tail>self.head: return self.tail-self.head
        else: return self.max_size-self.head+self.tail

    def add(self):
        size = self.size()
        if size==self.max_size:
            raise MemoryError('достигнут максимальный размер')
        elif self.tail<self.max_size:
            num = self.tail+1
        else:
            num = 0
        self.task_num += 1
        self.tasks[self.tail] = self.task_num
        self.tail = (self.tail+1)%self.max_size
        print(f"Задача №{self.task_num} добавлена")

    def show(self):
        v = self.tasks[self.head]
        print(f'Задача №{v} в приоритете')

    def do(self):
        v = self.tasks[self.head]
        print(f'do {v}')
        self.head = (self.head+1)%self.max_size

# Используем класс
#size = int(input("Определите размер очереди: "))
#q = Queue(size)
q = Queue(20)

mcmd = 'add add add add do do add add do add do do add add add do exit'.split()
for cmd in mcmd:
#while True:
    #cmd = input("Введите команду:")
    if cmd == "empty": 
        if q.is_empty():
            print("Очередь пустая")
        else:
            print("В очереди есть задачи")
    elif cmd == "size":
        print("Количество задач в очереди:", q.size())
    elif cmd == "add": 
        if q.size() != q.max_size:
            q.add()
        else:
            print("Очередь переполнена")
    elif cmd == "show": 
        if q.is_empty():
            print("Очередь пустая")
        else:
            q.show()
    elif cmd == "do": 
        if q.is_empty():
            print("Очередь пустая")
        else:
            q.do()
    elif cmd == "exit": 
        print(cmd)
        for _ in range(q.size()):
            q.do()
        print("Очередь пустая. Завершение работы")
        break
    else:
        print("Введена неверная команда")

