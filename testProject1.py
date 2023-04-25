import unittest
from project1 import *


# Unit tests for the DoesFit method, a subroutine of project1

class TestDoesFit(unittest.TestCase):
    def test1(self):
        print("test1")
        b1 = Block(1,2)
        self.assertTrue(doesFit([b1])[0])

    def test2(self):
        print("test2")
        b1 = Block(1,2)
        b2 = Block(1,2)
        self.assertFalse(doesFit([b1, b2])[0])
        
    def test3(self):
        print("test3")
        b2 = Block(1,2)
        b3 = Block(2, 3)
        self.assertTrue(doesFit([b2, b3])[0])

    def test4(self):
        print("test4")
        b2 = Block(1,2)
        b3 = Block(2, 3)
        self.assertTrue(doesFit([b3, b2])[0])

    def test5(self):
        print("test5")
        blocks = []
        for i in range(100):
            blocks.append(Block(i, i + 1))
        self.assertTrue(doesFit(blocks)[0])

    def test6(self):
        print("test6")
        blocks = []
        for i in range(100):
            blocks.append(Block(0, 1, 1000, 1))
        self.assertTrue(doesFit(blocks)[0])
     
    def test7(self):
        print("test7")
        blocks = []
        for i in range(8):
            blocks.append(Block(0, 1, 3, 1))
        self.assertFalse(doesFit(blocks)[0])
    
    def test8(self):
        print("test8")
        blocks = []
        for i in range(100):
            blocks.append(Block(0, 1, 30, 1))
        self.assertFalse(doesFit(blocks, 512)[0])
    
    def test9(self):
        print("test9")
        blocks = [Block(20, 60, 20), Block(31, 90, 10), Block(65, 66, 30)]
        self.assertTrue(doesFit(blocks)[0])

    def test10(self):
        print("test10")
        blocks = [Block(20, 60, 20), Block(31, 90, 10), Block(65, 67, 30)]
        self.assertFalse(doesFit(blocks)[0])


# Unit tests for the Brute Force solution
class TestBruteForce(unittest.TestCase):
    def test1(self):
        print("test1")
        blocks = [Block(1,2,0,1), Block(2,3,0,1), Block(3,4,0,1)]
        fz = []
        [value, solution] = bruteForce(blocks, fz)
        self.assertAlmostEqual(3, value)
        for i in range(3):
            self.assertAlmostEqual(blocks[i].start, solution[i].start)
            self.assertAlmostEqual(blocks[i].end, solution[i].end)
            self.assertAlmostEqual(blocks[i].delta, solution[i].delta)
            self.assertAlmostEqual(blocks[i].W, solution[i].W)
    
    def test2(self):
        print("test2")
        blocks = [Block(1,2,0,1), Block(2,3,0,1), Block(3,4,0,1)]
        fz = [Block(0,4)]
        [value, solution] = bruteForce(blocks, fz)
        self.assertAlmostEqual(0, value)
        self.assertEqual(0, len(solution))

    def test3(self):
        print("test3")
        blocks = [Block(1,2,1,1), Block(2,3,1,1), Block(3,4,1,1)]
        fz = [Block(0,4)]
        [value, solution] = bruteForce(blocks, fz)
        self.assertAlmostEqual(1, value)
        self.assertEqual(1, len(solution))
        for i in range(len(solution)):
            self.assertAlmostEqual(4, solution[i].start)
            self.assertAlmostEqual(5, solution[i].end)
            self.assertAlmostEqual(1, solution[i].delta)
            self.assertAlmostEqual(1, solution[i].W)

    def test4(self):
        print("test4")
        blocks = []
        fz = [Block(0,4)]
        [value, solution] = bruteForce(blocks, fz)
        self.assertAlmostEqual(0, value)
        self.assertEqual(0, len(solution))

    def test5(self):
        print("test5")
        blocks = []
        fz = []
        [value, solution] = bruteForce(blocks, fz)
        self.assertAlmostEqual(0, value)
        self.assertEqual(0, len(solution))

    def test6(self):
        print("test6")
        blocks = [Block(1,2,0,1), Block(1,2,1,1), Block(1,2,0,7)]
        fz = [Block(0,1)]
        [value, solution] = bruteForce(blocks, fz)
        self.assertAlmostEqual(8, value)
        self.assertEqual(2, len(solution))
        self.assertAlmostEqual(1, solution[0].start)
        self.assertAlmostEqual(2, solution[0].end)
        self.assertAlmostEqual(0, solution[0].delta)
        self.assertAlmostEqual(7, solution[0].W)
        self.assertAlmostEqual(2, solution[1].start)
        self.assertAlmostEqual(3, solution[1].end)
        self.assertAlmostEqual(1, solution[1].delta)
        self.assertAlmostEqual(1, solution[1].W)
    
    def test7(self):
        print("test7")
        blocks = [Block(1,2,0,1), Block(1,2,1,1), Block(1,2,0,7)]
        fz = [Block(0,1), Block(0,0.5), Block(0.5, 1), Block(100,127,300,300)]
        [value, solution] = bruteForce(blocks, fz)
        self.assertAlmostEqual(8, value)
        self.assertEqual(2, len(solution))
        self.assertAlmostEqual(1, solution[0].start)
        self.assertAlmostEqual(2, solution[0].end)
        self.assertAlmostEqual(0, solution[0].delta)
        self.assertAlmostEqual(7, solution[0].W)
        self.assertAlmostEqual(2, solution[1].start)
        self.assertAlmostEqual(3, solution[1].end)
        self.assertAlmostEqual(1, solution[1].delta)
        self.assertAlmostEqual(1, solution[1].W)


class testApproximation (unittest.TestCase):
    def test1(self):
        print("test1")
        blocks = [Block(1,2,0,1), Block(2,3,0,1), Block(3,4,0,1)]
        fz = []
        [value, solution] = approximateSolution(blocks, fz, temprature = 0)
        self.assertAlmostEqual(3, value)
        for i in range(3):
            self.assertAlmostEqual(blocks[i].start, solution[i].start)
            self.assertAlmostEqual(blocks[i].end, solution[i].end)
            self.assertAlmostEqual(blocks[i].delta, solution[i].delta)
            self.assertAlmostEqual(blocks[i].W, solution[i].W)

    def test2(self):
        print("test2")
        blocks = [Block(1,2,0,1), Block(2,3,0,1), Block(3,4,0,1)]
        fz = []
        [value, solution] = approximateSolution(blocks, fz, temprature = 10)
        self.assertAlmostEqual(3, value)
        for i in range(3):
            self.assertAlmostEqual(blocks[i].start, solution[i].start)
            self.assertAlmostEqual(blocks[i].end, solution[i].end)
            self.assertAlmostEqual(blocks[i].delta, solution[i].delta)
            self.assertAlmostEqual(blocks[i].W, solution[i].W)

    def test3(self):
        print("test3")
        blocks = [Block(1,2,1,1), Block(2,3,1,1), Block(3,4,1,1)]
        fz = [Block(0,4)]
        [value, solution] = approximateSolution(blocks, fz)
        self.assertAlmostEqual(1, value)
        self.assertEqual(1, len(solution))
        for i in range(len(solution)):
            self.assertAlmostEqual(4, solution[i].start)
            self.assertAlmostEqual(5, solution[i].end)
            self.assertAlmostEqual(1, solution[i].delta)
            self.assertAlmostEqual(1, solution[i].W)

    def test4(self):
        print("test4")
        blocks = []
        fz = [Block(0,4)]
        [value, solution] = approximateSolution(blocks, fz)
        self.assertAlmostEqual(0, value)
        self.assertEqual(0, len(solution))

    def test5(self):
        print("test5")
        blocks = []
        fz = []
        [value, solution] = approximateSolution(blocks, fz)
        self.assertAlmostEqual(0, value)
        self.assertEqual(0, len(solution))
    
    def test6(self):
        print("test6")
        blocks = [Block(1,2,0,1), Block(2,3,0,1), Block(3,4,0,1)]
        fz = [Block(0,4)]
        [value, solution] = approximateSolution(blocks, fz, num_iteration = 100)
        self.assertAlmostEqual(0, value)
        self.assertEqual(0, len(solution))

    def test7(self):
        print("test7")
        blocks = []
        for i in range(100):
            blocks.append(Block(i, i+1, 1, 1))
        [value, solution] = approximateSolution(blocks, [], num_iteration = 1000, iter_per_subset = 10)
        print("Test 7: Value " + str(value))

    def test8(self):
        print("test8")
        blocks = []
        for i in range(50):
            blocks.append(Block(i, i+1, 1, 1))
        for i in range(50):
            blocks.append(Block(i, i+1, 1, 20))
        [value, solution] = approximateSolution(blocks, [], num_iteration = 2000, iter_per_subset = 10)
        print("Test 8: Value " + str(value))

    def test9(self):
        print("test9")
        blocks = []
        for i in range(50):
            blocks.append(Block(i, i+1, 1, 1))
        for i in range(50):
            blocks.append(Block(i, i+1, 1, 20))
        [value, solution] = approximateSolution(blocks, [], num_iteration = 5000, iter_per_subset = 10)
        print("Test 9: Value " + str(value))
        


if __name__ == '__main__':
    unittest.main()
