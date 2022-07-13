
def srt(src):
    l = len(src)
    d = int(l/2)
    s1 = src[:d]
    s2 = src[d:]
    if l>2:
        s1 = srt(s1)
        s2 = srt(s2)
    i1 = 0
    i2 = 0
    l1 = len(s1)
    l2 = len(s2)
    r = []
    while True:
        if i1==l1 and i2==l2: break
        elif i1==l1 and i2<l2:
            r.append(s2[i2])
            i2 += 1
            continue
        elif i1<l1 and i2==l2:
            r.append(s1[i1])
            i1 += 1
            continue
        elif s1[i1]<s2[i2]:
            r.append(s1[i1])
            if i1<len(s1): i1 += 1
        else:
            r.append(s2[i2])
            if i2<len(s2): i2 += 1
    return r

src = [2, 3, 1, 4, 6, 5, 9, 8, 7]

print(src)
r = srt(src)
print(r)
