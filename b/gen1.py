def f():
    a=0
    while True:
        yield a
        a+=1
        if a>10: break

for v in f():
    print(v)

g=f()
for _ in range(10):
    print(g.__next__())

