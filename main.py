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

class Simplex:

    def __init__(self, points):
        self.points = points

    def __sort__(self):
        for i in range(2):
            for j in range(2):
                if Q(self.points[j])> Q(self.points[j+1]):
                    self.points[j], self.points[j+1] = self.points[j+1], self.points[j]

def algorithm():
    Point1 = Point(random.randint(1,10),random.randint(1,10))
    Point2 = Point(random.randint(1, 10), random.randint(1, 10))
    Point3 = Point(random.randint(1, 10), random.randint(1, 10))
    simplex = Simplex([Point1, Point2, Point3])
    simplex.__sort__()
    P1 = simplex.points[0]
    P2 = simplex.points[1]
    P3 = simplex.points[2]

    BestX = (P1.x + P2.x) / 2
    BestY = (P1.y + P2.y) / 2
    M = Point(BestX, BestY)
    Mx = M.x + (M.x - P3.x)
    My = M.y + (M.y - P3.y)
    W = Point(Mx, My)

expression = input("Введите функцию")
algorithm()
