from sys import platform

print('ход вводится в виде координат в формате "строка колонка"')
signs = ['X', 'O']
names = [input(f'имя игрока {i+1} ({signs[i]}): ') for i in range(2)]

data = [[' ' for i in range(3)] for j in range(3)]
dsize = len(data)

currentPlayer = 0
turnCount = 0
isLinux = platform!='linux'

# перевод курсора вверх в линукс
def up(cnt=1):
    if isLinux: print('\033[K\033[F'*cnt, end='')
    pass

def getPlayerName(p):
    return f'{names[p]} ({signs[p]})'

def getint(sval,name):
    if not sval.isdigit():
        return f'{name} должна быть числом'
    v = int(sval)
    if not(0<=v<=2):
        return f'неправильная {name} {sval}. допутимые значения: 0, 1, 2'
    return v

def check(v):
    v = v.strip()

    # проверка формата
    vl = len(v)
    if not (2<=vl<=3):
        return f'неправильный формат: {v}'
    elif vl==3:
        v = v[0]+v[2]

    # отдельными строками чтобы не съехал вывод. показываем только 1 ошибку
    row = getint(v[0], 'строка')
    if type(row) is str: return row
    col = getint(v[1], 'колонка')
    if type(col) is str: return col
    
    # если ячейка занята
    if data[row][col]!=' ':
        return f'ячейка ({row} {col}) уже занята'

    data[row][col] = signs[currentPlayer]
    
    return ''

err = ''
def refresh(binput=True):
    global currentPlayer, turnCount, err
    if turnCount>0: up(7)
    print(f'Ходов: {turnCount}')
    print('  0 1 2')
    for sn in range(3):
        print(sn, end=' ')
        for k in data[sn]:
            print(k, end=' ')
        print()
    print(err)
    if not binput: return
    v = input(f'Ход игрока {getPlayerName(currentPlayer)}. Введите ход: ')
    err = check(v)
    if not err:
        turnCount += 1
        currentPlayer = 1-currentPlayer
        err = ''

def checkRules():
    '''проверка правил'''

    global dsize

    # строки
    for r in data:
        v = r[0]
        if v==' ': continue
        cnt = sum([1 for i in range(dsize) if r[i]==v])
        if cnt==dsize: return v

    # колонки
    for c in range(dsize):
        v = data[0][c]
        if v==' ': continue
        cnt = sum([1 for r in data if r[c]==v])
        if cnt==dsize: return v

    # диагонали
    # \
    v = data[0][0]
    if v!=' ':
        cnt = sum([1 for i in range(dsize) if data[i][i]==v])
        if cnt==dsize: return v

    # /
    v = data[dsize-1][0]
    if v!=' ':
        cnt = sum([1 for i in range(dsize) if data[dsize-i-1][i]==v])
        if cnt==dsize: return v

    # все ячейки заполнениы = ничья
    s = 0
    for r in data:
        for c in r:
            if c!=' ': s += 1
    if s==dsize**2: return ' '

    return None


def main():
    '''главный цикл'''
    gameOver = None
    while gameOver is None:
        refresh()
        gameOver = checkRules()
    refresh(False)
    if gameOver==' ':
        print(f'Ничья. Ходов: {turnCount}')
    else:
        name = names[signs.index(gameOver)]
        print(f'Победил {name}. Ходов: {turnCount}')
    input('нажмите Enter для выхода') # чтобы консоль в винде не закрылось

main()