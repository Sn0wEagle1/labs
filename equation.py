a = int(input())
b = int(input())
c = int(input())
d = b**2 - 4*a*c
x1 = (-1*b+d**0.5)/2*a
x2 = (-1*b-d**0.5)/2*a
if d > 0:
    print('Корни квадратного уравнения:', x1, x2)
if d == 0:
    print('Корень квадратного уравнения:', x1)
if d < 0:
    print('Корней нет')