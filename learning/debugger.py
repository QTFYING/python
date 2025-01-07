# 例1
d = 1
class A:
    a = 1
    def __init__(self):
        self.b = 2
    def f(self):
        c = 3
        print(d, self.a, self.b, c)


print(d)
a = A()
a.f()