from random import randint
data = list(map(int,'6 5 3 1 8 7 2 4'.split()))
data = [2, 3, 1, 4, 6, 5, 9, 8, 7]
#data = [6,5]

'''
data = []
while len(data)<20:
    i = randint(0, 100)
    if i not in data: data.append(i)
'''

def srt(data:list):
    cnt = 0
    ldata = len(data)
    for i in range(ldata):
        for j in range(i, ldata):
            cnt += 1
            if data[j]<data[i]:
                q = data.pop(j)
                data.insert(i, q)
                print(data)
    return cnt

def srt1(data): # пузырьковая
    cnt = 0
    for i in range(len(data), 1, -1):
        for j in range(i-1):
            if data[j]>data[j+1]:
                cnt += 1
                q = data[j]
                data[j] = data[j+1]
                data[j+1] = q
                print(data)
    return cnt

def srt2(data): # хрень
    cnt = 0
    for i in range(len(data), 1, -1):
        print(i, cnt)
        for j in range(i-1):
            if data[j]>data[j+1]:
                cnt += 1
                q = data[j]
                data[j] = data[j+1]
                data[j+1] = q
                print(data, 1)
        for j in range(i-2, 0, -1):
            if data[j]>data[j+1]:
                cnt += 1
                q = data[j]
                data[j] = data[j+1]
                data[j+1] = q
                print(data, 2)
    return cnt
    
print(data, 0)
cnt = srt(data)
print(data, cnt)
