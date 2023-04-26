# Лабараторная работа по реализации трех алгоритмов нахождения количества прямоугольников, к которым принадлажит данная точка
___
## Навигация по файлу
1. [Реализация структур для хранения данных](#реализация-структур-для-хранения-данных)
2. [Алгоритмы](#алгоритмы)
    - [Первый алгоритм - алгоритм перебора](#первый-алгоритм---алгоритм-перебора)
    - [Второй алгоритм - построение карты с сжатыми координатами](#второй-алгоритм---построение-карты-с-сжатыми-координатами)
    - [Третий алгоритм -  алгоритм на дереве](#третий-алгоритм----алгоритм-на-дереве)
3. [Тесты](#тесты)
4. [Выводы](#выводы)
5. [Запуск](#запуск)

___
## Реализация структур для хранения данных

```
class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class RectangleClass:
    def __init__(self, x1, y1, x2, y2):
        self.LeftDown = Point2D(x1, y1)
        self.RightUp = Point2D(x2, y2)

```
___
## Алгоритмы
___
### Первый алгоритм - алгоритм перебора

Подготовка алгоритма является присвоение данных и выполняется за О(1)
```
def BuildData(self, Rectangles):
    self.Rectangles = Rectangles
```

Сам процесс работы алгоритма является перебор и провека принадлежности точки к каждому прямоугольнику и выполняется за O(N)
```
def GetAnswer(self, Point):
    count = 0
    for Rectangle in self.Rectangles:
        if Rectangle.LeftDown.x < Point.x < Rectangle.RightUp.x and Rectangle.LeftDown.y < Point.y < Rectangle.RightUp.y:
            ++count
    return count
```
___
### Второй алгоритм - построение карты с сжатыми координатами

Подготовка данных заключается в сжатие координат и заполнение каждой точки карты тем количеством прямоугольников, которые пересекают ее. Сложность O(N^3)
```
def BuildData(self, Rectangles):
    n = len(Rectangles)
    if n == 0:
        self.DataIsEmpty = True
        return
    self.DataIsEmpty = False

    self.CompressedX = [0] * (n * 3)
    self.CompressedY = [0] * (n * 3)
    for i in range(n):
        self.CompressedX[i * 3] = Rectangles[i].LeftDown.x
        self.CompressedX[i * 3 + 1] = Rectangles[i].RightUp.x
        self.CompressedX[i * 3 + 2] = Rectangles[i].RightUp.x + 1
        self.CompressedY[i * 3] = Rectangles[i].LeftDown.y
        self.CompressedY[i * 3 + 1] = Rectangles[i].RightUp.y
        self.CompressedY[i * 3 + 2] = Rectangles[i].RightUp.y + 1

    self.CompressedX = sorted(list(set(self.CompressedX)))
    self.CompressedY = sorted(list(set(self.CompressedY)))
    self.Map = [[0 for i in range(len(self.CompressedY))] for j in range(len(self.CompressedX))]

    for Rectangle in Rectangles:
        for i in range(self.FindPos(self.CompressedX, Rectangle.LeftDown.x),
                       self.FindPos(self.CompressedX, Rectangle.RightUp.x) + 1):
            for j in range(self.FindPos(self.CompressedY, Rectangle.LeftDown.y),
                           self.FindPos(self.CompressedY, Rectangle.RightUp.y) + 1):
                self.Map[i][j] += 1
```

Процесс нахождения ответа заключается в нахождении сжатых координат точки, которую мы хотим проверить, и возврат в качестве ответа значение точки на карте с такими сжатыми координатыми. Сложность O(logN)
```
def GetAnswer(self, Point):
    if Point.x < self.CompressedX[0] or Point.y < self.CompressedY[0]:
        return 0
    return self.Map[self.FindPos(self.CompressedX, Point.x)][self.FindPos(self.CompressedY, Point.y)]
```
___
### Третий алгоритм -  алгоритм на дереве

Для этого алгоритма понадобится дополнительный класс данных - event, который будет содержать координату по x(начала или конца), обе координаты по y и bool переменную, которая показывает начало это или конец прямоугольника 
```
class Event:
    def __init__(self, IndexX, StartY, EndY, isStart):
        self.ComprIndexX = IndexX
        self.ComprStartY = StartY
        self.ComprEndY = EndY
        self.isStart = isStart
```


Подготовка данных заключается в сжатие координат также как во втором случае
```
def BuildData(self, Rectangles):
    n = len(Rectangles)
    if n == 0:
        self.DataIsEmpty = True
        return
    self.DataIsEmpty = False

    self.CompressedX = [0] * (n * 3)
    self.CompressedY = [0] * (n * 3)
    for i in range(n):
        self.CompressedX[i * 3] = Rectangles[i].LeftDown.x
        self.CompressedX[i * 3 + 1] = Rectangles[i].RightUp.x
        self.CompressedX[i * 3 + 2] = Rectangles[i].RightUp.x + 1
        self.CompressedY[i * 3] = Rectangles[i].LeftDown.y
        self.CompressedY[i * 3 + 1] = Rectangles[i].RightUp.y
        self.CompressedY[i * 3 + 2] = Rectangles[i].RightUp.y + 1

    self.CompressedX = sorted(list(set(self.CompressedX)))
    self.CompressedY = sorted(list(set(self.CompressedY)))
    self.LenComprX = len(self.CompressedX)
    self.LenComprY = len(self.CompressedY)
```

Далее создаем список всех событий(начала и конца прямоугольников)
```
Events = [0] * 2 * n
for i in range(n):
    Events[i * 2] = Event(self.FindPos(self.CompressedX, Rectangles[i].LeftDown.x),
                          self.FindPos(self.CompressedY, Rectangles[i].LeftDown.y),
                          self.FindPos(self.CompressedY, Rectangles[i].RightUp.y + 1), True)
    Events[i * 2 + 1] = Event(self.FindPos(self.CompressedX, Rectangles[i].RightUp.x + 1),
                              self.FindPos(self.CompressedY, Rectangles[i].LeftDown.y),
                              self.FindPos(self.CompressedY, Rectangles[i].RightUp.y + 1), False)
Events = sorted(Events, key=lambda EventCase: EventCase.ComprIndexX)
```

И далее построении дерева отрезков, где используем список максимальной длина от самой большой до самой маленькой сжатой координаты y. В течение перебора всех событий дерево изменяется и копируется в массив для каждой сжатой координаты. Сложность O(NlogN)
```
self.CompressedTreesX = [0] * self.LenComprX
LogLenComprY = math.log2(self.LenComprY)
LenTree = self.LenComprY * 2 - 1 if LogLenComprY % 1 == 0 else 2 ** (int(LogLenComprY) + 2) - 1
self.LenComprCoorTree = 2 ** LogLenComprY if LogLenComprY % 1 == 0 else 2 ** (int(LogLenComprY) + 1)
self.Trees = [[0] * LenTree] * self.LenComprX
self.Tree = [0] * LenTree

i = 0
for event in Events:
    if event.ComprIndexX != CompXCoor:
        self.Trees[i] = self.Tree.copy()
        self.CompressedTreesX[i] = CompXCoor
        i += 1
        CompXCoor = event.ComprIndexX
    self.ChangeTree(0, 0, self.LenComprCoorTree, event.ComprStartY, event.ComprEndY,
                    1 if event.isStart else -1)

self.Trees[i] = self.Tree.copy()
self.CompressedTreesX[i] = CompXCoor
```

Сам алгоритм построения: 
```
def ChangeTree(self, Index, Left, Right, StartY, EndY, isStartValue):
    if StartY <= Left and Right <= EndY:
        self.Tree[Index] += isStartValue
        return
    Mid = (Left + Right) // 2
    if Mid > StartY and Left < EndY:
        self.ChangeTree(Index * 2 + 1, Left, Mid, StartY, EndY, isStartValue)
    if Right > StartY and Mid < EndY:
        self.ChangeTree(Index * 2 + 2, Mid, Right, StartY, EndY, isStartValue)
```

Для поиска количества прямоугольников, пересекающих точку, нужно сжать координаты и считать сумму всех вершин дерева, пока идем к точке
```
def GetSum(self, Tree, Index, Left, Right, Target):
    if Right - Left == 1:
        return Tree[Index]
    Mid = (Left + Right) // 2
    if Target < Mid:
        return Tree[Index] + self.GetSum(Tree, Index * 2 + 1, Left, Mid, Target)
    else:
        return Tree[Index] + self.GetSum(Tree, Index * 2 + 2, Mid, Right, Target)

def GetAnswer(self, Point):
    if Point.x < self.CompressedX[0] or Point.y < self.CompressedY[0]:
        return 0
    return self.GetSum(
        self.Trees[self.FindPosMore(self.CompressedTreesX, self.FindPosMore(self.CompressedX, Point.x) - 1) - 1], 0,
        0, self.LenComprCoorTree, self.FindPosMore(self.CompressedY, Point.y) - 1)
```

___
## Тесты

Временная сложность построения данных. По графику видно, что время алгоритма, основанного на карте, ведет себя как степенная функция. Время построения на 1000 элементов более 450(с). График дествительно похож на O(N^3)

![image](https://user-images.githubusercontent.com/90086457/233473179-cdbb0ea3-12f3-45f4-82ae-daa23550998b.png)

Чтобы распознать более детально построение других алгоритмов, запустим их отдельно. Как видно по графику, время построения алгоритма перебора действительно константное O(1). Время построения дерева не растет так быстро, и действительно сложность составляет примерно O(NlogN)

![image](https://user-images.githubusercontent.com/90086457/233474402-ed854822-24c2-47a5-b6ba-96a400b9b7f3.png)

Время ответа ведет себя не стабильно на графике, тк оно очень мало, но в целом видно, что сложность алгоритма перебора O(N), тк при 400 прямоугольниках время примерно 0.006(с), а при 800 уже почти 0.012(с). Также видно, что и у алгоритма карты и у алгоритма дерева сложность возрастает, но медленно O(logN)

![image](https://user-images.githubusercontent.com/90086457/233476951-5e482605-900e-4e72-9ef6-22d57af86844.png)

Прогоним тесты для общего времени работы: те построения и ответа при одинаковом количестве данных

![image](https://user-images.githubusercontent.com/90086457/233494326-f2b228aa-5bfa-4d73-90ec-446841a70712.png)

Как видим алгоритм на карте работает дольше всех, поэтому сделаем только для двух других для большей наглядности

![image](https://user-images.githubusercontent.com/90086457/233494976-ece5ac6b-0ffd-48d7-9432-8897d9dd17cb.png)

По графику видно, что общее время работы алгоритма перебора меньше, чем дерева. Скорее всего это связано с особенностями оптимизации Python, тк алгоритм дерева на больших данных должен быть эффективнее.

## Выводы:

Если у нас очень большие входные данные с прямоугольниками, но при этом мало точек, то тут больше подойдет алгоритм перебора (тк N*logN + M*logN > N*M при маленьких M). Если не много прямоугольник, но очень много точек, то алгоритм карты подойдет больше.
Если же много данных и точек и прямоугольников, то алгоритм дерева решит проблему лучше другихю. (N - количество прямоугольникв, M - количество точек)

## Запуск 

Чтобы запустить проект, достаточно установить все не встроенные использованные библиотеки
Чтобы это сделать достаточно, достаточно перейте в командню строоку или терминал и открыть директорию проекта, после чего вписать команду
```
pip install -r requirements.txt
```
или установить библиотеки из этого файла вручную
