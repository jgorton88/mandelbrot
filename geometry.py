
class Point(object):
    def __init__(self, location=(0.0, 0.0)):
        self.x = location[0]
        self.y = location[1]

    def __add__(self, other):
        return Point((self.x+other.x, self.y+other.y))

    def __sub__(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        # print('__sub__', self.x, other.x, dx, '::', self.y, other.y, dy)
        return Point((dx, dy))

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, scalar):
        return Point((self.x*scalar, self.y*scalar))

    def __div__(self, scalar):
        return Point((self.x/scalar, self.y/scalar))

    def __imul__(self, scalar):
        self.x *= scalar
        self.y *= scalar
        return self

    def __idiv__(self, scalar):
        self.x /= scalar
        self.y /= scalar
        return self

    def __str__(self):
        return '('+str(self.x)+', '+str(self.y)+')'

class Rect(object):
    def __init__(self, dimensions=(1.0, 1.0), origin=(0.0, 0.0)):
        if isinstance(dimensions, Point):
            self.dim = dimensions
        else:
            self.dim = Point(dimensions)

        if isinstance(origin, Point):
            self.origin = origin
        else:
            self.origin = Point(origin)

    def get_p0(self):
        return self.origin

    def set_p0(self, other):
        if isinstance(other, Point): 
            self.origin = other
        else:
            self.origin = Point(other)
        return self

    def get_p1(self):
        return self.origin + self.dim

    def set_p1(self, other):
        if isinstance(other, Point):
            self.dim = other - self.origin
        else:
            self.dim = Point(other) - self.origin
        return self.origin + self.dim

    p0 = property(get_p0, set_p0)

    p1 = property(get_p1, set_p1)

    def __add__(self, other):
        return Rect(self.dim, self.origin+other)

    def __sub__(self, other):
        return Rect(self.dim, self.origin-other)

    def __iadd__(self, other):
        self.origin += other
        return self
    
    def __isub__(self, other):
        self.origin -= other
        return self

    def center(self):
        return Point((self.origin.x+self.dim.x/2.0, self.origin.y+self.dim.y/2.0))

    def __mul__(self, scalar):
        pcenter = self.center()
        dim = self.dim * scalar
        origin = Point((pcenter.x-dim.x/2.0, pcenter.y-dim.y/2.0))
        return Rect(dim, origin)

    def __div__(self, scalar):
        pcenter = self.center()
        dim = self.dim / scalar
        origin = Point((pcenter.x-dim.x/2.0, pcenter.y-dim.y/2.0))
        return Rect(dim, origin)

    def __imul__(self, scalar):
        pcenter = self.center()
        self.dim *= scalar
        self.origin = Point((pcenter.x-self.dim.x/2.0, pcenter.y-self.dim.y/2.0))
        return self

    def __idiv__(self, scalar):
        pcenter = self.center()
        self.dim /= scalar
        self.origin = Point((pcenter.x-self.dim.x/2.0, pcenter.y-self.dim.y/2.0))
        return self

    def __str__(self):
        return str(self.origin) + ' dx ' + str(self.dim.x) + ' dy ' + str(self.dim.y)

if __name__ == '__main__':
    a = Point((2, 3))
    b = Point((-7, 9))

    print(a)

    print(a, b)

    c = a + b
    print('a+b', c)

    d = c - a
    print('c-a', d)

    a = Point((1, 3))
    for k in range(5):
        a += Point((0, 1))
        print(a)
