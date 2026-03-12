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

expression = input("Введите функцию")
algorithm()
