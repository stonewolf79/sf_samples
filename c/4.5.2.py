
from time import sleep


g = {
    "Адмиралтейская": {
        "Садовая": 4},
    "Садовая": {
        "Сенная площадь": 4,
        "Спасская": 3,
        "Адмиралтейская": 4,
        "Звенигородская": 5},
    "Сенная площадь": {
        "Садовая": 4,
        "Спасская": 4},
    "Спасская": {
        "Садовая": 3,
        "Сенная площадь": 4,
        "Достоевская": 6},
    "Звенигородская": {
        "Пушкинская": 3,
        "Садовая": 5},
    "Пушкинская": {
        "Звенигородская": 3,
        "Владимирская": 4},
    "Владимирская": {
        "Достоевская": 3,
        "Пушкинская": 4},
    "Достоевская": {
        "Владимирская": 3,
        "Спасская": 6}
}
'''
d = {k:100 for k in g.keys()}

d[list(d)[0]] = 0
see = {k:False for k in g.keys()}

for _ in range(len(d)):
    
    notsee = [k for k,v in see.items() if not v]
    kmin = min(notsee, key=lambda x: d[x])
    print(f'kmin={kmin} unsee={notsee}')
    see[kmin] = True

    for gk,gv in g[kmin].items():
        dmin = min(d[gk], d[kmin]+g[kmin][gk])
        print(f'dmin={dmin} d[gk]={d[gk]} d[kmin]+gv={d[kmin]+gv}')
        d[gk] = dmin

print(d)
'''
G=g
D = {k : 100 for k in G.keys()}  # расстояния
start_k = 'Адмиралтейская'  # стартовая вершина
D[start_k] = 0  # расстояние от неё до самой себя равно нулю
U = {k : False for k in G.keys()}  # флаги просмотра вершин
p = {}

for _ in range(len(D)):
    # выбираем среди непросмотренных наименьшее по расстоянию
    min_k = min([k for k in U.keys() if not U[k]], key = lambda x: D[x])

    for v in G[min_k].keys():  # проходимся по всем смежным вершинам
        D[v] = min(D[v], D[min_k] + G[min_k][v])  # минимум
        p[v] = min_k
    U[min_k] = True  # просмотренную вершину помечаем
    
print(D)
print(p)

for k in D.keys(): print(k,end=', ')

pointer = 'Спасская'
path = []
while(pointer is not None):
    path.append(pointer)
    print(pointer)
    pointer = p[pointer]
    sleep(1)
path.reverse()
print(path)