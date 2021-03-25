import os

class pos():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class circle():
    def __init__(self, p, r):
        self.p = p
        self.r = r
    def get(self):
        return self

if __name__ == '__main__':
    p = pos(1, 2)
    c = circle(p, 5)
    input(c.get())
