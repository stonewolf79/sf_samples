import random  # модуль, с помощью которого перемешиваем массив

# пусть имеем массив всего лишь из 9 элементов
cnt = 100
array = [random.randint(0,cnt) for _ in range(cnt)] 

is_sort = False  # станет True, если отсортирован
count = 0  # счётчик количества перестановок

while not is_sort:  # пока не отсортирован
    count += 1  # прибавляем 1 к счётчику
    
    random.shuffle(array)  # перемешиваем массив
    
    # проверяем отсортирован ли
    is_sort = True
    for i in range(len(array)-1):
        if array[i] > array[i+1]:
            is_sort = False
            break
            
print(array)
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(count)