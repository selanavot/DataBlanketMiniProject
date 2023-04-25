import unittest
from project2 import *

# --------------------------------------------------------------
# --------- unit tests for the contains method -----------------
# --------------------------------------------------------------
class TestZone(unittest.TestCase):
    def test_zoneContains(self):
        zone1 = Zone(Polygon([Point(0, 0), Point(0,1), Point(1,1), Point(1,0)]), 0, 1)
        self.assertTrue(zone1.contains(Point(0.5, 0.5, 0.5)))
        self.assertTrue(zone1.contains(Point(0.99999, 0.11111, 0.42)))
        self.assertFalse(zone1.contains(Point(-1, 0.5, 0.5)))
        self.assertFalse(zone1.contains(Point(2, 0.5, 0.5)))
        self.assertFalse(zone1.contains(Point(0.5, -1, 0.5)))
        self.assertFalse(zone1.contains(Point(0.5, 2, 0.5)))
        self.assertFalse(zone1.contains(Point(0.5, 0.5, 2)))
        self.assertFalse(zone1.contains(Point(0.5, 0.5, -1)))
        self.assertTrue(zone1.contains(Point(0, 0.5, 0.5)))
        self.assertTrue(zone1.contains(Point(0.5, 0, 0.5)))
        self.assertTrue(zone1.contains(Point(0, 0.5, 0)))
        self.assertTrue(zone1.contains(Point(0, 0.5, 1)))

    def test_intersects(self):
        z = Zone(Polygon([Point(0, 0), Point(0,1), Point(1,1), Point(1,0)]), 0, 1)
        self.assertTrue(z.intersects(Zone(Polygon([Point(0, 0), Point(0,1), Point(1,1), Point(1,0)]), 0, 1)))
        self.assertTrue(z.intersects(Zone(Polygon([Point(0, 0), Point(0,1), Point(1,1), Point(1,0)]), 0.9, 1.9)))
        self.assertTrue(z.intersects(Zone(Polygon([Point(0, 0.5), Point(0,1.5), Point(1,1.5), Point(1,0.5)]), 0, 1)))
        self.assertTrue(z.intersects(Zone(Polygon([Point(0.1, 0.1), Point(0.9,0.9), Point(0.3,0.3)]), 0, 1)))
        self.assertTrue(z.intersects(Zone(Polygon([Point(-10,-10), Point(10, 10), Point(100, 90)]), -10, 110)))
        self.assertTrue(z.intersects(Zone(Polygon([Point(1,0), Point(1,1), Point(3,3)]), 0, 1)))
        self.assertTrue(z.intersects(Zone(Polygon([Point(0, 0), Point(0,1), Point(1,1), Point(1,0)]), 1, 2)))
        self.assertFalse(z.intersects(Zone(Polygon([Point(3,3), Point(3,6), Point(6,6), Point(6,3)]), 0, 1)))

# --------------------------------------------------------------------------------------------
# ------------------ Unit tests for helper methods -------------------------------------------
# --------------------------------------------------------------------------------------------
class TestHelperMethods(unittest.TestCase):
    def test_neighbors(self):
        point = Point(100, 100, 100)
        nbrs = neighbors(point)
        self.assertTrue(Point(101, 100, 100) in nbrs)
        self.assertTrue(Point(100, 101, 100) in nbrs)
        self.assertTrue(Point(100, 100, 101) in nbrs)
        self.assertTrue(Point(99, 100, 100) in nbrs)
        self.assertTrue(Point(100, 99, 100) in nbrs)
        self.assertTrue(Point(100, 100, 99) in nbrs)

    def test_actualBlock(self):
        zone = actualBlock(Point(100, 100, 100), 10, Point(3, -3, 1))
        self.assertTrue(zone.contains(Point(135, 75, 111)))
        self.assertFalse(zone.contains(Point(100, 100, 100)))

    def test_manhattanDistance(self):
        self.assertEqual(40, manhattanDistance(Point(10, 10, 10), Point(0, 20, -10)))
        self.assertEqual(40, manhattanDistance(Point(10, 10, 10), Point(20, 0, -10)))
        self.assertEqual(20, manhattanDistance(Point(10, 10, 10), Point(10, -10, 10)))
        self.assertEqual(0, manhattanDistance(Point(10, -10, 10), Point(10, -10, 10)))

class TestFindPath(unittest.TestCase):
    def test_1(self):
        map = FlightZone(Zone(Polygon([Point(0,0), Point(0,3), Point(3,3), Point(3,0)]), 0, 3), [], 1)
        print("test1")
        output = map.findPath(Point(0.5, 0.5, 0.5), Point(2.5, 2.5, 2.5))
        plotSolution(output)
    
    def test_2(self):
        map = FlightZone(Zone(Polygon([Point(0,0), Point(0,3), Point(3,3), Point(3,0)]), 0, 3), [])
        print("test2")
        output = map.findPath(Point(0.5, 0.5, 0.5), Point(2.5, 2.5, 2.5))
        plotSolution(output)

    def test_3(self):
        map = FlightZone(Zone(Polygon([Point(0,0), Point(0,100), Point(100,100), Point(100,0)]), 0, 100), [])
        print("test3")
        output = map.findPath(Point(0, 0, 0), Point(75, 30, 99))
        plotSolution(output)


    def test_4(self):
        map = FlightZone(Zone(Polygon([Point(0,0), Point(0,100), Point(100,100), Point(100,0)]), 0, 100),
                         [Zone(Polygon([Point(10,10), Point(10,90), Point(90,90), Point(90,0)]), 10, 90)])
        print("test4")
        output = map.findPath(Point(0, 0, 0), Point(99, 99, 99))
        plotSolution(output)

    
    # def test_5(self):
    #     # This test checks whether we detect that no path exists. It may take a long time
    #     print("test5")
    #     map = FlightZone(Zone(Polygon([Point(0,0), Point(0,100), Point(100,100), Point(100,0)]), 0, 100),
    #                      [Zone(Polygon([Point(0,0), Point(0,100), Point(100,100), Point(100,0)]), 10, 90)])
    #     solution = map.findPath(Point(0, 0, 0), Point(99, 99, 99))
    #     self.assertEqual(solution, None)

    # def test_6(self):
    #     # The path in this test is hard to find - this test may take a long time
    #     print("test6")
    #     map = FlightZone(Zone(Polygon([Point(0,0), Point(0,100), Point(100,100), Point(100,0)]), 0, 100),
    #                      [Zone(Polygon([Point(0,0), Point(0,100), Point(70,100), Point(70,0)]), 10, 20),
    #                       Zone(Polygon([Point(30,0), Point(30,100), Point(100,100), Point(100,0)]), 80, 90)])
    #     output = map.findPath(Point(0, 0, 0), Point(99, 99, 99))
    #     plotSolution(output)

    def test_7(self):
        print("test7")
        map = FlightZone(Zone(Polygon([Point(0,0), Point(0,100), Point(100,100), Point(100,0)]), 0, 100), [], 30)
        output = map.findPath(Point(97, 97, 97), Point(10, 10, 10))
        plotSolution(output)

    def test_8(self):
        print("test8")
        map = FlightZone(Zone(Polygon([Point(0,0), Point(0,100), Point(100,100), Point(100,0)]), 0, 100), [])
        self.assertTrue(map.findPath(Point(200, 200, 100), Point(0, 0, 0)) is None)

    def test_9(self):
        print("test9")
        map = FlightZone(Zone(Polygon([Point(0,0), Point(0,100), Point(100,100), Point(100,0)]), 0, 100), [])
        self.assertTrue(map.findPath(Point(30, 1, 89), Point(-1, 0, 0)) is None)

    def test_71(self):
        print("test7.1")
        map = FlightZone(Zone(Polygon([Point(0,0), Point(0,100), Point(100,100), Point(100,0)]), 0, 100), [])
        output = map.findPath(Point(97, 97, 97), Point(10, 97, 97))
        plotSolution(output)

    def test_72(self):
        print("test7.2")
        map = FlightZone(Zone(Polygon([Point(0,0), Point(0,100), Point(100,100), Point(100,0)]), 0, 100), [])
        output = map.findPath(Point(97, 97, 97), Point(97, 10, 97))
        plotSolution(output)
    
    def test_73(self):
        print("test7.3")
        map = FlightZone(Zone(Polygon([Point(0,0), Point(0,100), Point(100,100), Point(100,0)]), 0, 100), [])
        output = map.findPath(Point(97, 97, 97), Point(97, 97, 10))
        plotSolution(output)
    
    def test_74(self):
        print("test7.4")
        map = FlightZone(Zone(Polygon([Point(0,0), Point(0,100), Point(100,100), Point(100,0)]), 0, 100), [])
        output = map.findPath(Point(97, 10, 97), Point(97, 97, 97))
        plotSolution(output)

    def test_8(self):
        map = FlightZone(Zone(Polygon([Point(0,0), Point(0,100), Point(100,100), Point(100,0)]), 0, 100), [])
        print("test8")
        output = map.findPath(Point(0, 0, 0), Point(100, 100, 100))
        plotSolution(output)


if __name__ == '__main__':
    unittest.main()