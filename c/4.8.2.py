c=0
array = [2, 3, 1, 4, 6, 5, 9, 8, 7]
for i in range(len(array)): # проходим по всему массиву

        idx_min = i # сохраняем индекс предположительно минимального элемента
        for j in range(i+1, len(array)):
                c+=1
                if array[j] < array[idx_min]:
                        idx_min = j
        if i != idx_min: # если индекс не совпадает с минимальным, меняем
            array[i], array[idx_min] = array[idx_min], array[i]

print(array)
print(c)