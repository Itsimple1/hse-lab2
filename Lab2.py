import random
import time
import math

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm


class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class RectangleClass:
    def __init__(self, x1, y1, x2, y2):
        self.LeftDown = Point2D(x1, y1)
        self.RightUp = Point2D(x2, y2)


class Event:
    def __init__(self, IndexX, StartY, EndY, isStart):
        self.ComprIndexX = IndexX
        self.ComprStartY = StartY
        self.ComprEndY = EndY
        self.isStart = isStart


class BrutForce:
    def __init__(self):
        self.Rectangles = None

    def BuildData(self, Rectangles):
        self.Rectangles = Rectangles

    def GetAnswer(self, Point):
        count = 0
        for Rectangle in self.Rectangles:
            if Rectangle.LeftDown.x < Point.x < Rectangle.RightUp.x and Rectangle.LeftDown.y < Point.y < Rectangle.RightUp.y:
                ++count
        return count

    def GetAnswers(self, Points):
        a = []
        for Point in Points:
            count = 0
            for Rectangle in self.Rectangles:
                if Rectangle.LeftDown.x <= Point.x <= Rectangle.RightUp.x and \
                        Rectangle.LeftDown.y <= Point.y <= Rectangle.RightUp.y:
                    count += 1
            a.append(count)
        return a

    def TimeBuild(self, Rectangles):
        start = time.time()
        self.BuildData(Rectangles)
        return time.time() - start

    def TimeAnswers(self, Points):
        start = time.time()
        self.GetAnswers(Points)
        return time.time() - start

    def TimeBuildAndAnswers(self, Rectangles, Points):
        start = time.time()
        self.BuildData(Rectangles)
        self.GetAnswers(Points)
        return time.time() - start

class MapAlgo:
    def __init__(self):
        self.DataIsEmpty = None

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

    def GetAnswer(self, Point):
        if Point.x < self.CompressedX[0] or Point.y < self.CompressedY[0]:
            return 0
        return self.Map[self.FindPos(self.CompressedX, Point.x)][self.FindPos(self.CompressedY, Point.y)]

    def GetAnswers(self, Points):
        if self.DataIsEmpty or len(Points) == 0:
            return []
        answers = []
        for Point in Points:
            answers.append(self.GetAnswer(Point))
        return answers

    def FindPos(self, CompressedCoor, Coordinate):
        for i in range(len(CompressedCoor)):
            if CompressedCoor[i] > Coordinate:
                return i - 1
        return len(CompressedCoor) - 1

    def TimeBuild(self, Rectangles):
        start = time.time()
        self.BuildData(Rectangles)
        return time.time() - start

    def TimeAnswers(self, Points):
        start = time.time()
        self.GetAnswers(Points)
        return time.time() - start

    def TimeBuildAndAnswers(self, Rectangles, Points):
        start = time.time()
        self.BuildData(Rectangles)
        self.GetAnswers(Points)
        return time.time() - start


class TreeAlgo:
    def __init__(self):
        self.Tree = None
        self.Trees = None
        self.LenComprY = None
        self.LenComprCoorTree = None
        self.LenComprX = None
        self.CompressedTreesX = None
        self.Roots = None
        self.CompressedRootsX = None
        self.CompressedY = None
        self.CompressedX = None
        self.DataIsEmpty = None

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

        Events = [0] * 2 * n
        for i in range(n):
            Events[i * 2] = Event(self.FindPos(self.CompressedX, Rectangles[i].LeftDown.x),
                                  self.FindPos(self.CompressedY, Rectangles[i].LeftDown.y),
                                  self.FindPos(self.CompressedY, Rectangles[i].RightUp.y + 1), True)
            Events[i * 2 + 1] = Event(self.FindPos(self.CompressedX, Rectangles[i].RightUp.x + 1),
                                      self.FindPos(self.CompressedY, Rectangles[i].LeftDown.y),
                                      self.FindPos(self.CompressedY, Rectangles[i].RightUp.y + 1), False)
        Events = sorted(Events, key=lambda EventCase: EventCase.ComprIndexX)

        CompXCoor = Events[0].ComprIndexX

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

    def ChangeTree(self, Index, Left, Right, StartY, EndY, isStartValue):
        if StartY <= Left and Right <= EndY:
            self.Tree[Index] += isStartValue
            return
        Mid = (Left + Right) // 2
        if Mid > StartY and Left < EndY:
            self.ChangeTree(Index * 2 + 1, Left, Mid, StartY, EndY, isStartValue)
        if Right > StartY and Mid < EndY:
            self.ChangeTree(Index * 2 + 2, Mid, Right, StartY, EndY, isStartValue)

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

    def GetAnswers(self, Points):
        if self.DataIsEmpty or len(Points) == 0:
            return []
        answers = []
        for Point in Points:
            answers.append(self.GetAnswer(Point))
        return answers

    def FindPos(self, CompressedCoors, Coordinate):
        for i in range(len(CompressedCoors)):
            if CompressedCoors[i] >= Coordinate:
                return i
        return len(CompressedCoors)

    def FindPosMore(self, CompressedCoors, Coordinate):
        for i in range(len(CompressedCoors)):
            if CompressedCoors[i] > Coordinate:
                return i
        return len(CompressedCoors)

    def TimeBuild(self, Rectangles):
        start = time.time()
        self.BuildData(Rectangles)
        return time.time() - start

    def TimeAnswers(self, Points):
        start = time.time()
        self.GetAnswers(Points)
        return time.time() - start

    def TimeBuildAndAnswers(self, Rectangles, Points):
        start = time.time()
        self.BuildData(Rectangles)
        self.GetAnswers(Points)
        return time.time() - start


class Tests:
    def __init__(self):
        self.Prime = [909, 2917, 2927, 2939, 2953, 2957, 2963, 2969, 2971, 2999, 3001, 3011, 3019]
        self.LenPrime = 13

    def GenerateRectangles(self, N):
        Rectangles = [0] * N
        for i in range(N):
            Rectangles[i] = RectangleClass(10 * i, 10 * i, 10 * (2 * N - i), 10 * (2 * N - i))
        return Rectangles

    def GeneratePoints(self, N):
        Points = [0] * N
        for i in range(N):
            Points[i] = Point2D((self.Prime[random.randint(0, 12)] * i) ** 31 % (20 * N),
                                (self.Prime[random.randint(0, 12)] * i) ** 31 % (20 * N))
        return Points

    def GeneratePointsRandom(self, N, MinX, MaxX, MinY, MaxY):
        Points = [0] * N
        for i in range(N):
            Points[i] = Point2D(random.randint(MinX, MaxX), random.randint(MinY, MaxY))
        return Points

    def CheckTime(self, N, Interval, M):
        BrutAlgo = BrutForce()
        AlgoMap = MapAlgo()
        AlgoTree = TreeAlgo()

        NumberTests = [i for i in range(0, N + 1, Interval)]
        TestsLen = len(NumberTests)

        TestRectangles = [self.GenerateRectangles(i) for i in tqdm(NumberTests)]
        TestPoints = self.GeneratePoints(M)

        BrutBuildTimes = np.array([]).astype('float64')
        MapBuildTimes = np.array([]).astype('float64')
        TreeBuildTimes = np.array([]).astype('float64')
        BrutAnswTimes = np.array([]).astype('float64')
        MapAnswTimes = np.array([]).astype('float64')
        TreeAnswTimes = np.array([]).astype('float64')

        for i in tqdm(range(TestsLen)):
            BrutBuildTimes = np.append(BrutBuildTimes, BrutAlgo.TimeBuild(TestRectangles[i]))
            BrutAnswTimes = np.append(BrutAnswTimes, BrutAlgo.TimeAnswers(TestPoints))

            MapBuildTimes = np.append(MapBuildTimes, AlgoMap.TimeBuild(TestRectangles[i]))
            MapAnswTimes = np.append(MapAnswTimes, AlgoMap.TimeAnswers(TestPoints))

            TreeBuildTimes = np.append(TreeBuildTimes, AlgoTree.TimeBuild(TestRectangles[i]))
            TreeAnswTimes = np.append(TreeAnswTimes, AlgoTree.TimeAnswers(TestPoints))

        fig = plt.figure()
        ax = fig.add_subplot()
        ax.plot(NumberTests, BrutBuildTimes)
        ax.plot(NumberTests, MapBuildTimes)
        ax.plot(NumberTests, TreeBuildTimes)
        plt.title("Time complexity of building data")
        ax.legend(['BrutForce', 'MapBuilding', "SegmentTree"])
        ax.set_xlabel('Number of rectangles')
        ax.set_ylabel('Time building')
        ax.grid()
        plt.show()

        fig = plt.figure()
        dx = fig.add_subplot()
        dx.plot(NumberTests, BrutAnswTimes)
        dx.plot(NumberTests, MapAnswTimes)
        dx.plot(NumberTests, TreeAnswTimes)
        plt.title("Time complexity of " + str(M) + " answer(s)")
        dx.legend(['BrutForce', 'MapBuilding', "SegmentTree"])
        dx.set_xlabel('Number of rectangles')
        dx.set_ylabel('Time building')
        dx.grid()
        plt.show()

    def CheckCommonTime(self, N):
        BrutAlgo = BrutForce()
        AlgoMap = MapAlgo()
        AlgoTree = TreeAlgo()

        NumberTests = [i for i in range(0, N + 1, 1000)]
        TestsLen = len(NumberTests)

        TestRectangles = [self.GenerateRectangles(i) for i in tqdm(NumberTests)]
        TestPoints = [self.GeneratePoints(i) for i in tqdm(NumberTests)]

        BrutCommonTimes = np.array([]).astype('float64')
        MapCommonTimes = np.array([]).astype('float64')
        TreeCommonTimes = np.array([]).astype('float64')

        for i in tqdm(range(TestsLen)):
            BrutCommonTimes = np.append(BrutCommonTimes, BrutAlgo.TimeBuildAndAnswers(TestRectangles[i], TestPoints[i]))

            MapCommonTimes = np.append(MapCommonTimes, AlgoMap.TimeBuildAndAnswers(TestRectangles[i], TestPoints[i]))

            TreeCommonTimes = np.append(TreeCommonTimes, AlgoTree.TimeBuildAndAnswers(TestRectangles[i], TestPoints[i]))


        fig = plt.figure()
        dx = fig.add_subplot()
        dx.plot(NumberTests, BrutCommonTimes)
        dx.plot(NumberTests, MapCommonTimes)
        dx.plot(NumberTests, TreeCommonTimes)
        plt.title("Time complexity of building and answers")
        dx.legend(['BrutForce', "MapBuilding", "SegmentTree"])
        dx.set_xlabel('Number of rectangles and points')
        dx.set_ylabel('Time building')
        dx.grid()
        plt.show()

    def CheckTimeBuild(self, N):
        BrutAlgo = BrutForce()
        AlgoMap = MapAlgo()
        AlgoTree = TreeAlgo()

        NumberTests = range(0, N + 1, N // 10)
        TestsLen = len(NumberTests)

        TestRectangles = [self.GenerateRectangles(i) for i in tqdm(NumberTests)]

        BrutAlgoTimes = np.array([BrutAlgo.TimeBuild(TestRectangles[i]) for i in tqdm(range(TestsLen))])
        MapAlgoTimes = np.array([AlgoMap.TimeBuild(TestRectangles[i]) for i in tqdm(range(TestsLen))])
        TreeAlgoTimes = np.array([AlgoTree.TimeBuild(TestRectangles[i]) for i in tqdm(range(TestsLen))])

        fig = plt.figure()
        ax = fig.add_subplot()
        ax.plot(NumberTests, BrutAlgoTimes)
        ax.plot(NumberTests, MapAlgoTimes)
        ax.plot(NumberTests, TreeAlgoTimes)
        plt.title("Time complexity of building data")
        ax.legend(['BrutForce', 'MapBuilding', "SegmentTree"])
        ax.set_xlabel('Number of rectangles')
        ax.set_ylabel('Time building')
        ax.grid()
        plt.show()


def GetInputRectangles():
    n = int(input())
    Rectangles = []
    for i in range(n):
        x1, y1, x2, y2 = map(int, input().split())
        Rectangles.append(RectangleClass(x1, y1, x2, y2))
    return Rectangles


def GetInputPoints():
    m = int(input())
    Points = []
    for i in range(m):
        x1, y1 = map(int, input().split())
        Points.append(Point2D(x1, y1))
    return Points


TestCase = Tests()
TestCase.CheckCommonTime(5000)
