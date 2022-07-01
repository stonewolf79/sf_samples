
def decor(f):
    d={}
    def wrapper(*a,**kwa):
        k = a[0]
        if k in d: 
            print('из кэша')
            return d[k]
        r = f(*a,**kwa)
        print('из функции')
        d[k] = r
        return r
    return wrapper

@decor
def f(n):
    return n * 123456789

print(f(1))
print(f(2))
print(f(3))
print(f(2))