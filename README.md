Below are instructions on how to use my solution to task 1 and 2:

----------------------------------------------------------------------
Task 1:

project1.py contains two solutions to task 1: brute force and approximation. It contains helper methods and the definition of the Block class, which is part of the input format for the solutions.

Each solution takes two lists of Block objects as inputs: blocks and forbidden zones. To initialize a block, one must use the block constructor which takes parameters start, end, delta (default 0), and value (default 0). Note that the delta and value of forbidden zones will be ignored. The tests file testProject1.py demonstrates some of the behavior of the solution function, and examples of how to call the solution function, though it is messy and was primarily used for debugging.

It is possible to use the solutions and the Block class in any script contained in the same folder by adding the statement "from project1 import *" at the top. 

See the Project1.pdf for the statement of the problem we were trying to solve, assumptions we have made, and an explanation of the algorithms we used.

----------------------------------------------------------------------
Task 2

We used a veriation of the A-star algorithm to solve this problem. The solution, as well as helper classes and methods, are contained in project2.py. The file testProject2.py contains examples on how to use the solution.

Before finding any paths, users must create a "map", represented as an instance of the FlightZone class. To construct one, simply call its constructor, which takes a Fly-Zone and a list of No-Fly-Zones for parameters, as well as an optional grid_size parameter. Each zone parameter must be an instance of the Zone class, which can be constructed using the Zone(polygon : shapely.geometry.Polygon, bottom : float, top : float). See https://shapely.readthedocs.io/en/stable/reference/shapely.Polygon.html for information on how to construct a Shapley Polygon. All information of the map will be pixelated, and the grid_size parameter controls the pixelation resolution.

After a FlightZone has been constructed, users can call the FlightZone.findPath method to find a path between two points. The function returns a list of point representing a path, if it exists, and None otherwise. The plotSolution function provides an easy way to plot a path between two points.

See Project1.pdf for an overview of the problem and our solution