'''
        Подвиг 3. Объявите класс Point так, чтобы объекты этого класса можно было создавать командами:

        p1 = Point(10, 20)
        p2 = Point(12, 5, 'red')

        Здесь первые два значения - это координаты точки на плоскости (локальные свойства x, y), а третий
        необязательный аргумент - цвет точки (локальное свойство color). Если цвет не указывается,
        то он по умолчанию принимает значение black.

        Создайте тысячу таких объектов с координатами (1, 1), (3, 3), (5, 5), ... то есть,
        с увеличением на два для каждой новой точки. Каждый объект следует поместить в список points (по порядку).
        Для второго объекта в списке points укажите цвет 'yellow'.

        P.S. На экран в программе ничего выводить не нужно.
'''

class Point:
    def __init__(self, x, y, color='black'):
        self.x = x
        self.y = y
        self.color = color


# points = []
# step = 0
# for i in range(1, 1001):
#     if step == 1:
#         points.append(Point(i + step, i + step, color='yellow'))
#         step += 1
#         continue
#     points.append(Point(i + step, i + step))
#     step += 1

points = [Point(i, i) if i != 3 else Point(i, i, color='yellow') for i in range(1, 2000, 2)]

print(len(points))
for point in points:
    print(point.__dict__)