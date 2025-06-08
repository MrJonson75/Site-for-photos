'''
        Большой подвиг 10. Объявите два класса:

        Cell - для представления клетки игрового поля;
        GamePole - для управления игровым полем, размером N x N клеток.

        С помощью класса Cell предполагается создавать отдельные клетки командой:

        c1 = Cell(around_mines, mine)
        Здесь around_mines - число мин вокруг данной клетки поля; mine - булева величина (True/False),
        означающая наличие мины в текущей клетке.
        При этом, в каждом объекте класса Cell должны создаваться локальные свойства:

        around_mines - число мин вокруг клетки (начальное значение 0);
        mine - наличие/отсутствие мины в текущей клетке (True/False);
        fl_open - открыта/закрыта клетка - булево значение (True/False). Изначально все клетки закрыты (False).



        С помощью класса GamePole должна быть возможность создавать квадратное игровое поле с числом клеток N x N:

        pole_game = GamePole(N, M)
        Здесь N - размер поля; M - общее число мин на поле. При этом, каждая клетка представляется объектом
        класса Cell и все объекты хранятся в двумерном списке N x N элементов - локальном
        свойстве pole объекта класса GamePole.

        В классе GamePole должны быть также реализованы следующие методы:

        init() - инициализация поля с новой расстановкой M мин
                (случайным образом по игровому полю, разумеется каждая мина должна находиться в отдельной клетке).

        show() - отображение поля в консоли в виде таблицы чисел открытых клеток
                (если клетка не открыта, то отображается символ #;
                мина отображается символом *;
                между клетками при отображении ставить пробел).

        При создании экземпляра класса GamePole в его инициализаторе следует вызывать метод init()
        для первоначальной инициализации игрового поля.

        В классе GamePole могут быть и другие вспомогательные методы.

        Создайте экземпляр pole_game класса GamePole с размером поля N = 10 и числом мин M = 12.

        P.S. На экран в программе ничего выводить не нужно.
'''
import random as rnd

class Cell:
    def __init__(self, around_mines, mine):
        self.around_mines = around_mines  # число мин вокруг клетки (начальное значение 0)
        self.mine = mine                  # наличие/отсутствие мины в текущей клетке (True/False)
        self.fl_open = True              # открыта/закрыта клетка - булево значение (True/False)

class GamePole:
    def __init__(self, N, M):
        self.N = N  # размер поля
        self.M = M  # общее число мин на поле
        self.init()


    def init(self):
        self.pole = [[Cell(0, False) for _ in range(self.N)] for _ in range(self.N)]
        self.set_mine()     # Минируем
        self.set_number_of_min()  # Описываем поля вокруг мин

    def show(self):
        for line in self.pole:
            for val in line:
                if val.fl_open:
                    if val.mine:
                        print('*', end=' ')
                    else:
                        print(val.around_mines, end=' ')
                else:
                    print('#', end=' ')
            print()

    def set_mine(self):
        count = self.M
        while count > 0:
            i = rnd.randint(0, self.N - 1)
            j = rnd.randint(0, self.N - 1)
            if self.pole[i][j].mine:
                continue
            self.pole[i][j] = Cell(0, True)
            count -= 1

    def set_number_of_min(self):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        for i in range(self.N):
            for j in range(self.N):
                if self.pole[i][j].mine:
                    continue
                count = 0
                for x, y in directions:
                    dx, dy = i + x, j + y
                    if 0 <= dx < self.N and 0 <= dy < self.N and self.pole[dx][dy].mine:
                        count += 1
                self.pole[i][j].around_mines = count

    def get_open(self, i, j):
        self.pole[i][j].fl_open = True


pole_game = GamePole(10, 12)
pole_game.show()
# while True:
#     a, b = map(int, input().split())
#     pole_game.get_open(a, b)
#     pole_game.show()
