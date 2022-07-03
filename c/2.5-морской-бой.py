
from random import randint, choice

class Ship:
    '''корабль'''
    
    def __init__(self, x, y, length, horizontal):
        self._x = x
        self._y = y
        self._length = length
        self._horizontal = horizontal

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

class Dash:
    '''поле'''
    # можно было бы сделать матрицу со статусами, но так интереснее

    def __init__(self, size=6, fill=False):
        self._ships = [] # список кораблей
        self._live = 0 # количество живых клеток
        self._occupies = {} # занятые кораблями клетки (x,y):ship
        self._restricted = [] # запрещённые к расстановке клетки включая зону вокруг кораблей(x,y)
        self._size = size # размер поля
        self._damaged = [] # попадания
        self._miss = [] # промахи
        if fill: self.fillShips()

    @property
    def live(self):
        '''количество живых клеток'''
        return self._live

    def fillShips(self):
        '''расстановка кореблей'''
        sConfig = '3-1 2-2 1-4' # длина - количество
        mShips = map(int, [t.split('-') for t in sConfig.split(' ')])
        
        for shipType in mShips:
            shipLen = shipType[0]
            for _ in range(shipType[1]):
                self.setShip(shipLen)
                live += shipLen

    def setShip(self, shiplen):
        '''установка корабля на поле'''

        # выбор координат
        while True:
            # из размера сразу вычитаем длину, чтобы не проверять потом границы            
            size = self._size-shiplen

            x, y = randint(1, size), randint(1, size)

            horizontal = randint(0,1)
            ok = self.checkSet(x, y, shiplen, horizontal)
            if ok: break
        
        ship = Ship(x,y,shiplen,horizontal)
        self._ships.append(ship)
        self._occupies[(x,y)] = ship

        # зона вокруг корабля
        for i in range(-1, shiplen+1):
            for k in range(-1, 2):
                coords = (x+i,y+k) if horizontal else (x+k,y+i)
                # координата выходит за границы, можно было бы не проверять, но пусть будет
                if not 0<coords[0]<=self._size or not 0<coords[1]<=self._size:
                    continue
                if not coords in self._restricted: self._restricted.append(coords)
    
    def checkSet(self, x, y, shiplen, horizontal):
        '''проверка корректности установки'''
        # проверка препятствий
        for i in range(shiplen):
            coords = (x+i,y) if horizontal else (x,y+i)
            if coords in self._restricted: return False

        self._ships.append(Ship(x, y, shiplen))

        return True

    def shot(self, x, y):
        '''выстрел
        False если выстрел недопустим, True если выстрел произведён успешно'''
        coords = (x,y)
        if coords in self._miss or coords in self._damaged: return False
        if coords in self._occupies:
            self._damaged += coords
            self._live -= 1
        else:
            self._miss += coords
        return True

class Game:
    def __init__(self, size):
        self.debug = False
        self.mode = 'set' # set=расстановка кораблей game=игра
        self.size = size
        self.dPlayer = Dash(size)
        self.dComp = Dash(size, fill=True)
        
        Game.sShip = '▓'
        Game.sDamage = 'X'
        Game.sMiss = 'o'
        Game.sArea = '░'

        msg = 'Не переживай, ты ещё не раз проиграешь!/Что ж, это была неплохая попытка, кожаный.../Я так могу весь день делать.'
        self.losMsg = choice(msg.split('/'))

        msg = 'Что-то я отвлёкся, ты тут сам с собой что ли играешь?/Статистически ты всё равно проиграл./Опять мухлюешь, кожаный.'
        self.winMsg = choice(msg.split('/'))

    @classmethod
    def getSign(cls, coords, dash:Dash, showZones=False, showCompShips=False):
        '''символ ячейки'''
        if coords in dash._damaged: # повреждение
            rValue = cls.sDamage
        elif coords in dash._miss: # промах
            rValue = cls.sMiss
        elif coords in dash._occupies: # корабль
            rValue = cls.sShip
        elif showZones and coords in dash._restricted: # зона вокруг корабля
            rValue = cls.sArea
        elif showCompShips and coords in dash._occupies: # корабль противника
            rValue = cls.sShip
        else:
            rValue = ' '
        return rValue

    def print(self, showZones=False, showCompShips=False):
        
        fieldWidth = self.size+1 # ширина поля с заголовком
        print('Ваш флот'.center(fieldWidth) + 'Противник'.center(fieldWidth))
        w = [n+1 for n in range(self.size)]
        print((' '+w)*2) # верхняя строка с номерами колонок

        d1 = self.dPlayer
        d2 = self.dComp
        for y in self.size:
            s1 = ''
            s2 = ''
            for x in self.size:
                coords = (x,y)
                s1 += Game.getSign(coords, d1, showZones=showZones)
                s2 += Game.getSign(coords, d2, showCompShips=showCompShips)
            print(f'{y+1}{s1}{y+1}{s2}{y+1}')
        print((' '+w)*2) # нижняя строка с номерами колонок

    def run(self):

        self.print()

        if self.mode=='set':
            print('Расставьте корабли. Введите координаты корабля в виде [строка колонка ориентация],'
                +'\n\tгде строка ориентация - "h" или "v" для горизонтального или вертикального расположения')
        else: print('Введите координаты выстрела в виде [строка колонка]')

        cmd = input('Ввод: ')
        if cmd=='debug': self.debug=True


def test():
    d = Dash()
    d.fillShips()
    print(d)

if __name__=='__main__':
    game = Game(6)
    game.run()