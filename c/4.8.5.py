array = [2, 3, 1, 4, 6, 5, 9, 8, 7]

cnt = 0
for i in range(1, len(array)):
    x = array[i]
    idx = i
    while True:
        if not(idx > 0): break 
        cnt += 1
        if not array[idx-1] > x: break
        array[idx] = array[idx-1]
        idx -= 1
    array[idx] = x   

print(cnt)

