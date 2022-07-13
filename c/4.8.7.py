
from numpy import append


def srt(data:list):
    dlen = len(data)
    if dlen==1: return data
    if dlen==2: return data if data[0]<data[1] else data.reverse()
    d = dlen//2
    v = data[d]
    r1, r2 = [], []
    for e in data:
        if e<v: r1.append(e)
        elif e>v: r2.append(e)
    if len(r2)>1: r2 = srt(r2)
    return r1+[d]+r2

src = [2, 3, 1, 4, 6, 5, 9, 8, 7]

print(src)
r = srt(src)
print(r)
