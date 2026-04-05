import random
import math

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

    def global_contract(self, delta=0.5):# сжатие всех точек к лучшей     
        best = self.points[0]
        for i in range(1, len(self.points)):
            self.points[i] = Point(
                best.x + delta * (self.points[i].x - best.x),
                best.y + delta * (self.points[i].y - best.y)
            )


def simplex_size(simplex):# для остановки 
    max_dist = 0
    for i in range(len(simplex.points)):
        for j in range(i + 1, len(simplex.points)):
            dx = simplex.points[i].x - simplex.points[j].x
            dy = simplex.points[i].y - simplex.points[j].y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist > max_dist:
                max_dist = dist
    return max_dist

def __repr__(self):
    return f"({self.x}, {self.y})"

def algorithm(max_iter=10, eps=1e-6):
    Point1 = Point(random.randint(1,10),random.randint(1,10))
    Point2 = Point(random.randint(1, 10), random.randint(1, 10))
    Point3 = Point(random.randint(1, 10), random.randint(1, 10))
    simplex = Simplex([Point1, Point2, Point3])
    for iteration in range(max_iter):
        simplex.__sort__()
        P1 = simplex.points[0]
        P2 = simplex.points[1]
        P3 = simplex.points[2]

        print(f"\nИтерация {iteration + 1}")
        print("Текущий симплекс:", simplex.points)
        print("Значения функции:", Q(P1), Q(P2), Q(P3))

        if simplex_size(simplex) < eps:
            print("\nДocтиgнyт критерий остановки.")
            print("Приближённый минимум в точке:", P1)
            print("Значение функции:", Q(P1))
            return

        mx = (P1.x + P2.x) / 2
        my = (P1.y + P2.y) / 2
        m = Point(mx, my)

        w = reflect(m, P3)

        if Q(P1) <= Q(w) < Q(P2):
            simplex.points[2] = w
            print("Сделано отражение")
            print(simplex.points)
            continue

        if Q(w) < Q(P1):
            e = expand(m, w)
            if Q(e) < Q(w):
                simplex.points[2] = e
                print("Сделано растяжение")
            else:
                simplex.points[2] = w
                print("Сделано отражение после проверки растяжения")
            print(simplex.points)
            continue
        c = contract(m, P3)
        if Q(c) < Q(P3):
            simplex.points[2] = c
            print("Сделано сжатие")
            print(simplex.points)
            continue

        simplex.global_contract()
        print("Сделано глобальное сжатие симплекса")

        simplex.__sort__()
    print("\nДостигнуто максимальное число итераций.")
    print("Лучшее найденное приближение:", simplex.points[0])
    print("Значение функции:", Q(simplex.points[0]))

expression = input("Введите функцию")
algorithm()
