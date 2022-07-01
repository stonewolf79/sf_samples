
def decor(f):
    cnt = 0
    def wrapper(*a,**kwa):
        nonlocal cnt
        cnt += 1
        r = f(*a,**kwa)
        print(f'вызовов: {cnt}')
        return r
    return wrapper

@decor
def f():
    pass

for i in range(10):
    f()
