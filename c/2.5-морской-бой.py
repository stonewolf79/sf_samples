
from curses.ascii import isdigit
from random import randint, choice

from numpy import append

class Ship:
    '''корабль'''
    
    def __init__(self, x, y, length, horizontal):
        self._x = x
        self._y = y
        self._length = length # длина
        self._lives = length # прочность
        self._horizontal = horizontal

    def __str__(self):
        o = 'H' if self._horizontal else 'V'
        return f'{self.x}:{self.y}:{self._length}-{o}'

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def length(self):
        return self._length

    @property
    def horizontal(self):
        return self._horizontal

    @property
    def lives(self):
        return self._lives

    def damage(self):
        '''кораблю нанесён урон'''
        self._lives -= 1

    @property
    def isAlive(self):
        return self._lives>0

class Dash:
    '''поле'''
    def __init__(self, size=6, fill=False):
        self.sConfig = '3-1 2-2 1-4' # длина - количество
        while True:
            # конфигурация кораблей (длина,количество)
            self.mShips = [list(map(int, t.split('-'))) for t in self.sConfig.split(' ')]
            self._ships = [] # список кораблей
            self._live = 0 # количество живых клеток
            self._map = {}
            self._size = size # размер поля
            if fill: 
                try:
                    self.fillShips()
                    break
                except:
                    continue
            break
    
    def clearRestricted(self):
        m = self._map
        mdel = [k for k,v in m.items() if v=='r']
        for k in mdel: del m[k]

    @property
    def live(self):
        '''количество живых клеток'''
        return self._live

    @live.setter
    def live(self, value):
        raise SyntaxError('Нельзя устанавливать свойство live')

    def print(self, m):
        print()
        for i in range(self._size): print(i,end='')
        print()
        for line in range(self._size):
            s = str(line)
            for col in range(self._size):
                coords = (line+1, col+1)
                if m[coords]: s+='O'
                else: s+='-'
            print(s)

    def fillShips(self):
        '''расстановка кореблей'''
        print('расстановка кореблей')
        for shipType in self.mShips:
            shipLen = shipType[0]
            print(shipLen,'',end='')
            for _ in range(shipType[1]):
                print('.',end='')
                for i in range(10):
                    ok = self.setShip(shipLen)
                    if ok: break
                if not ok: # за 10 попыток не удалось установить корабль, всё переделываем
                    raise TimeoutError('не получилось установить корабли')
                print('ok')
                self._live += shipLen
        #print([str(s) for s in self._ships])

    def setShip(self, shiplen):
        '''установка корабля на поле'''

        # выбор координат
        for _ in range(20): # 20 попыток установить корабль. если не получилось - выбираем всё подряд
            horizontal = randint(0, 1)
            # из размера сразу вычитаем длину, чтобы не проверять потом границы
            qsize = self._size
            if horizontal:
                size = (qsize-shiplen, qsize)
            else:
                size = (qsize, qsize-shiplen)
            x, y = randint(1,size[0]), randint(1,size[1])
            ok = self.checkSet(x, y, shiplen, horizontal)
            if ok: break
        
        if not ok:
            horizontal = 1
            for y in range(1, self._size+1):
                for x in range(1, self._size-shiplen+1):
                    ok = self.checkSet(x, y, shiplen, 1)
                    if ok: break
                if ok: 
                    break

        if not ok: return False

        ship = Ship(x,y,shiplen,horizontal)
        self.setShipOnMap(ship)

        return True

    def setShipOnMap(self, ship:Ship):
        self._ships.append(ship)

        x = ship.x
        y = ship.y
        for i in range(ship.length):
            if ship.horizontal:
                self._map[(x+i, y)] = ship
            else:
                self._map[(x, y+i)] = ship

        self.setRestricted(ship) # зона вокруг

    def setRestricted(self, ship:Ship):
        '''зона вокруг корабля'''
        for i in range(-1, ship.length+1):
            for k in range(-1, 2):
                coords = (ship.x+i, ship.y+k) if ship.horizontal else (ship.x+k, ship.y+i)
                # координата выходит за границы, можно было бы не проверять, но пусть будет
                if not 0<coords[0]<=self._size or not 0<coords[1]<=self._size:
                    continue
                if not coords in self._map:
                    print('coords',coords)
                    self._map[coords] = 'r'
    
    def checkSet(self, x, y, shiplen, horizontal):
        '''проверка корректности установки'''
        # проверка препятствий
        for i in range(shiplen):
            coords = (x+i, y) if horizontal else (x, y+i)
            if coords in self._map: return False
        return True

    def shot(self, x, y, checkArea=False):
        '''выстрел
        checkArea = проверять допустимую область вокруг кораблей (для ии)
        None если выстрел недопустим
        0 если промах
        1 если выстрел произведён успешно
        2 если утопил
        '''
        print(f'выстрел в {y}:{x}')
        coords = (x,y)
        m = self._map
        if coords in m:
            v = m[coords]
            if type(v) is Ship:
                ship = m[coords]
                ship.damage()
                m[coords] = 'd'
                self._live -= 1
                return (1,ship) if ship.isAlive else (2,ship)
            elif checkArea and v=='r': return (None,None)
            elif v in 'dm': return (None,None)
            m [coords] = 'm'
            return (0,None)
        else:
            m[coords] = 'm'
            return (0,None)

class Game:
    def __init__(self, size):
        self.debug = False
        self.mode = 'set' # set=расстановка кораблей game=игра
        self.size = size
        self.dPlayer = Dash(size)
        self.dComp = Dash(size, fill=True)
        self.lastResult = False # результат последнего выстрела
        
        Game.sShip = '▓'
        Game.sDamage = 'X'
        Game.sMiss = 'T'
        Game.sArea = '░'
        Game.sSpace = '.'

        msg = 'Не переживай, ты ещё не раз проиграешь!/Что ж, это была неплохая попытка, кожаный.../Я так могу весь день делать.'
        self.losMsg = choice(msg.split('/'))

        msg = 'Что-то я отвлёкся, ты тут сам с собой что ли играешь?/Статистически ты всё равно проиграл./Опять мухлюешь, кожаный.'
        self.winMsg = choice(msg.split('/'))

    @classmethod
    def getSign(cls, coords, dash:Dash, showZones=False, showShips=False):
        '''символ ячейки'''
        rValue = cls.sSpace
        if coords in dash._map: 
            v = dash._map[coords]
            if showShips and type(v) is Ship: # корабль
                rValue = cls.sShip
            if v=='d': # повреждение
                rValue = cls.sDamage
            elif v=='m': # промах
                rValue = cls.sMiss
            elif showZones and v=='r': # зона вокруг корабля
                rValue = cls.sArea
        return rValue

    def draw(self, showZones=False, showCompShips=False):
        '''отрисовка полей'''
        
        fieldWidth = self.size*2+1 # ширина поля с заголовком
        print('Ваш флот'.center(fieldWidth) +' '*2+ 'Противник'.center(fieldWidth))
        w = ' '.join([str(n+1) for n in range(self.size)])
        print('  '+w+' '*3+w) # верхняя строка с номерами колонок

        d1 = self.dPlayer
        d2 = self.dComp
        for y in range(self.size):
            s1 = s2 = ' '
            for x in range(self.size):
                coords = (x+1,y+1)
                s1 += Game.getSign(coords, d1, showZones=showZones, showShips=True)+' '
                s2 += Game.getSign(coords, d2, showZones=self.debug, showShips=showCompShips)+' '
            print(f'{y+1}{s1}{y+1}{s2}{y+1}')
        print('  '+w+' '*3+w) # нижняя строка с номерами колонок

    def checkInput(self, sCmd:str):
        rval = [] # результат
        s = sCmd.lower().strip()
        isSetMode = self.mode=='set'
        plen = 3 if isSetMode else 2 # количество параметров
        size = self.size
        
        # короткая форма без разделителей если размер поля меньше 10
        if size<10 and len(s)==plen:
            if not s[0].isdigit() or not s[1].isdigit(): raise ValueError('координаты должны быть числом')
            rval.append(int(s[0])) # строка
            rval.append(int(s[1])) # колонка
            if isSetMode: rval.append(s[2]) # ориентация

        else: # полная форма
            if len(s)<plen*2-1: raise ValueError('неверный формат')
            if not s[0].isdigit(): raise ValueError('первый аргумент не число')
            delim = '' # разделитель между аргументами. должен быть не число и не буква
            for c in s: 
                if not c.isdigit() and not s.isalpha(): 
                    delim = c
                    break
            m = s.split(delim)
            rval.append(int(m[0])) # строка
            rval.append(int(m[1])) # колонка
            if isSetMode: rval.append(m[2]) # ориентация

        # проверка корректности значений
        if not 1<=rval[0]<=size: raise ValueError(f'номер строки вне допустимого диапазона [1-{size}]')
        if not 1<=rval[1]<=size: raise ValueError(f'номер колонки вне допустимого диапазона [1-{size}]')
        if isSetMode and not rval[2] in 'hv': raise ValueError('ориентация может быть только "h" или "v"')

        return rval

    def getPlanCoords(self):
        '''плановая координата если не было попадания'''
        # сначала наугад по количеству клеток, потом заполнение

        for _ in range(self.size**2):
            coords = (randint(1,self.size+1), randint(1,self.size+1))
            yield coords

        if False:# для отладки
            # сначала пройдём по диагонали \
            for i in range(self.size):
                yield (i+1, i+1)

        # заполним что осталось
        for i in range(self.size):
            for k in range(self.size):
                yield (i+1, k+1)

        yield None

    def getcoords(self, coords, direction, distance):
        '''возвращает соседние координаты по указанному направлению'''
        if direction=='r': return (coords[0], coords[1]+distance)
        elif direction=='l': return (coords[0], coords[1]-distance)
        elif direction=='d': return (coords[0]+distance, coords[1])
        elif direction=='u': return (coords[0]-distance, coords[1])
        else: raise ValueError(f'направление не может быть "{direction}"')

    def inverseDirection(self, direction):
        '''обратное переданному направление'''
        dir = 'rudl'
        return dir[3-dir.index(direction)]

    def doAIshot(self):
        '''ии = искуственный идиот делает выстрел'''
        nextCoords = self.getPlanCoords()
        while True:
            while True:
                coords = nextCoords.__next__()
                r, ship = self.dPlayer.shot(*coords, True) # результат выстрела
                if r is not None: break
            yield r
            if r==0 or r==2: # промазал или добил = дальше по плану
                if r==2:
                    self.dPlayer.setRestricted()
                self.lastResult = False
                continue
            # куда-то попали, но не добили, надо добить
            # бьём в выбранном направлении, если недопустимое поле - то в обратном, если и там нет - выбираем новое
            # варианты выстрела
            shoots = list('rdlu') # r=вправо d=вниз l=влево u=вверх
            r = 0
            while True:
                if not shoots: break
                if not r:
                    direction = choice(shoots)
                    shoots.remove(direction)
                for i in range(1, self.size):
                    coords2 = self.getcoords(coords, direction, i)
                    r, ship = self.dPlayer.shot(*coords2, True) # результат выстрела
                    if r is None: break # недопустимый выстрел не будет сделан, целим другую клетку
                    if ship is not None: continue
                    yield r
                    if not r: 
                        direction = self.inverseDirection(direction)
                        if not direction in shoots: continue
                        shoots.remove(direction)
                    elif r==2: break
                if r==2: break
            if r==2: # ставим границу вокруг
                ship = self.dPlayer._map[coords]
                self.dPlayer.setRestricted(ship)

    def run(self):
        '''главный цикл'''

        m = self.dPlayer.mShips.copy()
        mShipsConfig = []
        for cfg in m:
            for _ in range(cfg[1]):
                mShipsConfig.append(cfg[0])

        currentShip = 0 # текущий корабль для установки
        debugMessage = '[режим отладки] '
        err = '' # текст сообщения об ошибке

        # прокрутка экрана
        scroll = '\n'*1

        ai = self.doAIshot()

        while(True):

            print(scroll)

            if self.mode=='set':
                    print('Расставьте корабли. Введите координаты корабля в виде [строка колонка ориентация],'
                        +'\n\tгде строка ориентация - "h" или "v" для горизонтального или вертикального расположения'
                        +'\n\tдля автоматической расстановки введите "auto"'
                        +'\n\tесли хотите сдаться, введите "drop"'
                        )
            else: print('Введите координаты выстрела в виде [строка колонка]')

            print()
            self.draw(showZones=self.mode=='set' or self.debug, showCompShips=self.debug)
            print()

            print(err)
            err = ''

            # счёт
            print(f'счёт: человек {self.dPlayer.live} компьютер {self.dComp.live}')

            if self.mode=='set':
                shipMsg = f'[ режим установки корабля. длина = {mShipsConfig[currentShip]} ] '
            else: shipMsg = ''

            cmd = input(f'{debugMessage if self.debug else ""}{shipMsg}Ввод: ')
            
            if self.mode=='gameover': return # выход
            
            if cmd=='debug': 
                self.debug=True
                continue
            elif cmd=='drop':
                self.draw(showCompShips=True)
                self.mode = 'gameover'
                break
            elif self.mode=='set' and cmd=='auto':
                self.mode = 'game'
                self.dPlayer = Dash(self.size, True)
                self.dPlayer.clearRestricted()
                continue

            try:
                rcmd = self.checkInput(cmd)
            except Exception as e:
                err = str(e) # покажем ошибку при следующем обновлении экрана
                continue

            # ход человека
            if self.mode=='set':
                if rcmd:
                    y, x, orient = rcmd
                    shipLen = mShipsConfig[currentShip]
                    if not self.dPlayer.checkSet(x, y, shipLen, orient=='h'):
                        err = 'Нельзя поставить корабль в выбранную позицию'
                        continue
                    ship = Ship(x, y, shipLen, orient=='h')
                    self.dPlayer.setShipOnMap(ship)
                    currentShip += 1
                    if currentShip==len(mShipsConfig):
                        self.mode = 'game'
                        self.dPlayer.clearRestricted()
                        continue
            elif rcmd:
                y, x = rcmd
                result = self.dComp.shot(x, y)
                if result is None: 
                    err = 'недопустимая позиция'
                    continue
                elif result==1:
                    err = 'ранил!'
                    continue
                elif result==2:
                    err = 'убил!'
                    if self.dComp.live==0:
                        err = self.winMsg
                        self.mode = 'gameover'
                    continue

            # ход компьютера
            ok = True
            while(ok): # стреляем пока попадаем или неправильные координаты
                r = ai.__next__()
                ok = r is None or r==1 or r==2
                if r==2:
                    if self.dPlayer.live==0:
                        err = self.losMsg
                        self.mode = 'gameover'
                        break

def test():
    #d = Dash()
    #d.fillShips()
    #print(d)
    d = Dash()
    d.live = 1

    g = Game(6)
    g.checkInput('11 2 e')


if __name__=='__main__':
    #test()
    game = Game(6)
    game.run()