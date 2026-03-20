import random

expression =""

def Q(point):
    x = point.x
    y = point.y
    return eval(expression)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x}, {self.y})"
def reflect(m, p3, alpha=1.0):
    return Point(
        m.x + alpha * (m.x - p3.x),
        m.y + alpha * (m.y - p3.y)
    )

def expand(m, w, gamma=2.0):
    return Point(
        m.x + gamma * (w.x - m.x),
        m.y + gamma * (w.y - m.y)
    )

def contract(m, p3, beta=0.5):
    return Point(
        m.x + beta * (p3.x - m.x),
        m.y + beta * (p3.y - m.y)
    )

class Simplex:

    def __init__(self, points):
        self.points = points

    def __sort__(self):
        for i in range(2):
            for j in range(2):
                if Q(self.points[j])> Q(self.points[j+1]):
                    self.points[j], self.points[j+1] = self.points[j+1], self.points[j]

def __repr__(self):
    return f"({self.x}, {self.y})"

def algorithm():
    Point1 = Point(random.randint(1,10),random.randint(1,10))
    Point2 = Point(random.randint(1, 10), random.randint(1, 10))
    Point3 = Point(random.randint(1, 10), random.randint(1, 10))
    simplex = Simplex([Point1, Point2, Point3])
    simplex.__sort__()
    P1 = simplex.points[0]
    P2 = simplex.points[1]
    P3 = simplex.points[2]

    mx = (P1.x + P2.x) / 2
    my = (P1.y + P2.y) / 2
    m = Point(mx, my)

    w = reflect(m, P3)

    if Q(P1) <= Q(w) < Q(P2):
        simplex.points[2] = w
        print("Сделано отражение")
        print(simplex.points)
        return

    if Q(w) < Q(P1):
        e = expand(m, w)
        if Q(e) < Q(w):
            simplex.points[2] = e
            print("Сделано растяжение")
        else:
            simplex.points[2] = w
            print("Сделано отражение после проверки растяжения")
        print(simplex.points)
        return
    c = contract(m, P3)
    if Q(c) < Q(P3):
        simplex.points[2] = c
        print("Сделано сжатие")
        print(simplex.points)
        return

    print("Нужно глобальное сжатие симплекса, но этот шаг пока не реализован")
    print(simplex.points)

expression = input("Введите функцию")
algorithm()
