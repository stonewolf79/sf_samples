
class Square:

    def __init__(self) -> None:
        self.s = 0

    @property
    def area(self):
        return self.s**2

    @property
    def size(self):
        return self.s

    @size.setter
    def size(self,value):
        self.s = value

s = Square()
#s.size = 3
print(s.area)