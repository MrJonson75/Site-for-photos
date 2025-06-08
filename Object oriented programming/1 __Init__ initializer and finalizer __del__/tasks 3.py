'''
        Подвиг 4. Объявите три класса геометрических фигур: Line, Rect, Ellipse. Должна быть возможность
        создавать объекты каждого класса следующими командами:

        g1 = Line(a, b, c, d)
        g2 = Rect(a, b, c, d)
        g3 = Ellipse(a, b, c, d)

        Здесь в качестве аргументов a, b, c, d передаются координаты верхнего правого и нижнего левого углов
        (произвольные числа). В каждом объекте координаты должны сохраняться
        в локальных свойствах sp (верхний правый угол) и ep (нижний левый) в виде кортежей (a, b) и (c, d)
        соответственно.

        Сформируйте 217 объектов этих классов: для каждого текущего объекта класс выбирается
        случайно (или Line, или Rect, или Ellipse).

        Координаты также генерируются случайным образом (числовые значения).
        Все объекты сохраните в списке elements.

        В списке elements обнулите координаты объектов только для класса Line.

        P.S. На экран в программе ничего выводить не нужно.
'''
import random as rnd

class Line:
    def __init__(self, a, b, c, d):
        self.sp = (a, b)        # (верхний правый угол)
        self.ep = (c, d)        # (нижний левый)


class Rect:
    def __init__(self, a, b, c, d):
        self.sp = (a, b)        # (верхний правый угол)
        self.ep = (c, d)        # (нижний левый)


class Ellipse:
    def __init__(self, a, b, c, d):
        self.sp = (a, b)        # (верхний правый угол)
        self.ep = (c, d)        # (нижний левый)


elements = []

for i in range(217):
    a, b, c, d = [round(rnd.random() * 100) for _ in range(4)]
    elements.append(
        rnd.choice([Line, Rect, Ellipse])(a, b, c, d)
    )

for element in elements:
    if isinstance(element, Line):
        element.sp = (0, 0)
        element.ep = (0, 0)



for element in elements:
    print(element)
    print(element.__dict__)