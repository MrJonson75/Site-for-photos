'''
        Подвиг 5. Объявите класс TriangleChecker, объекты которого можно было бы создавать командой:

        tr = TriangleChecker(a, b, c)

        Здесь a, b, c - длины сторон треугольника.

        В классе TriangleChecker необходимо объявить метод is_triangle(), который бы возвращал следующие коды:

        1 - если хотя бы одна сторона не число (не float или int) или хотя бы одно число меньше или равно нулю;
        2 - указанные числа a, b, c не могут являться длинами сторон треугольника;
        3 - стороны a, b, c образуют треугольник.

        Проверку параметров a, b, c проводить именно в таком порядке.

        Прочитайте из входного потока строку, содержащую три числа, разделенных пробелами, командой:

        a, b, c = map(int, input().split())
        Затем, создайте объект tr класса TriangleChecker и передайте ему прочитанные значения a, b, c.
        Вызовите метод is_triangle() из объекта tr и выведите результат на экран (код, который она вернет).

        Sample Input:

        3 4 5
        Sample Output:

        3
'''

# здесь объявите класс TriangleChecker
class TriangleChecker:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def is_triangle(self):
        for side in [self.a, self.b, self.c]:
            if isinstance(side, bool) or not isinstance(side, (int, float)) or side <= 0:
                return 1
        # if not all(isinstance(side, (int, float)) for side in [self.a, self.b, self.c]):
        #     return 1
        # if any(side <= 0 for side in [self.a, self.b, self.c]):
        #     return 1
        # a, b, c = sorted([self.a, self.b, self.c])
        # if a + b > c:
        #     return 3
        # return 2
        if (self.a + self.b < self.c) or (self.a + self.c < self.b) or (self.b + self.c < self.a):
            return 2
        return 3

    '''
            Способов проверить существует или нет несколько например:
        
        1й используя неравенство треугольника как у меня в коде
        
        2й Через сортировку сторон 
        a, b, c = sorted([a, b, c])    # Теперь c — наибольшая сторона 
        return a + b > c               # Если True, треугольник возможен
        
        3й Через площадь (формула Герона)
        p = (a + b + c) / 2
        area = (p * (p - a) * (p - b) * (p - c)) ** 0.5
        return not (area <= 0 or math.isnan(area))  # True, если треугольник возможен
         
        Лучший способ — неравенство треугольника (первый метод). Он простой, быстрый и покрывает все случаи
    '''


a, b, c = map(int, input().split()) # эту строчку не менять
# здесь создайте экземпляр tr класса TriangleChecker и вызовите метод is_triangle() с выводом информации на экран
tr = TriangleChecker(a, b, c)
print(tr.is_triangle())