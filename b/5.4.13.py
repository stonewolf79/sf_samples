
def e():
    n=0
    while(True):
        n += 1
        yield (1+1/n)**n

last = 0
for a in e(): # e() - генератор
    if (a - last) < 0.00000001: # ограничение на точность
        print(a)
        break # после достижения которого завершаем цикл
    else:
        last = a # иначе - присваиваем новое значение 