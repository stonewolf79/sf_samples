
from random import randint

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
    '''Поле'''

    def __init__(self, size=6, fill=False):
        self.ships = [] # список кораблей
        self.size = size # размер поля
        if fill: self.fillShips()

    def fillShips(self):
        '''расстановка кореблей'''
        sconfig = '3-1 2-2 1-4' # длина - количество
        mships = [t.split('-') for t in sconfig.split(' ')]
        
        self.denyPos = {i+1:[] for i in range(self.size)}

        for shiptype in mships:
            shiplen = shiptype[0]
            for _ in range(shiptype[1]):
                self.setShip(shiplen)

    def setShip(self, shiplen):
        '''установка корабля на поле'''
        while True:
            x, y = randint(1, self.size), randint(1, self.size)
            horizontal = randint(0,1)
            ok = self.checkSet(x, y, shiplen, horizontal)
            if ok: break
    
    def checkSet(self, x, y, shiplen, horizontal):
        '''проверка корректности установки'''
        ok = True
        for ship in self.ships:


        if ok: self.ships.append(Ship(x, y, shiplen))
        return ok

def test():
    d=Dash()
    d.fillShips()

if __name__=='__main__':
    test()