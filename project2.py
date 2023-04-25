''' Solution to Data Blanket Candidate Mini Project 2 '''

import copy
import math
import heapq
from dataclasses import dataclass, field
from typing import List, Any
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


# --------------------------------------------------------------------------------
# ------------------ Helper Classes ----------------------------------------------
# --------------------------------------------------------------------------------

class Zone:
    '''
    A zone is a polygon (2 dimensional), with a minimum and a maximum height (top
    and bottom).
    '''

    def __init__(self, polygon : Polygon, bottom : float, top : float):
        self.polygon = polygon
        self.top = top
        self.bottom = bottom

    def __str__(self):
        ''' A string representation of itself: (polygon, bottom, top) '''
        output = "(" + str(self.polygon) + ", " + str(self.bottom) + ", " + \
                 str(self.top) + ")"
        return output

    def __repr__(self):
        ''' A string representation of itself: (polygon, bottom, top) '''
        output = "(" + str(self.polygon) + ", " + str(self.bottom) + ", " + \
                 str(self.top) + ")"
        return output

    def contains(self, point : Point) -> bool:
        ''' 
        Checks whether a 3 dimentional point is contained in this zone. Returns
        true for points inside the polygon or on the edge
        '''
        if point.z < self.bottom or point.z > self.top:
            return False
        if self.polygon.contains(Point(point.x, point.y)):
            return True
        return self.polygon.touches(point)

    def intersects(self, other):
        ''' 
        Checks whether two zones intersect. Returns true if they intersect, even if just on
        an edge or vertex, and false otherwise.
        '''
        # If they are in disjoint heights, they do not intersect
        if self.bottom > other.top or self.top < other.bottom:
            return False

        # Their height intersects.
        # thus they intersect iff the interior of their polygons intersect
        return (self.polygon.intersects(other.polygon))
                #and not self.polygon.touches(other.polygon))


@dataclass(order=True)
class PrioritizedItem:
    ''' 
    This is an ugly solution to allow adding items of the sort (precedence, item) to priority
    queues, even if item is not comparable.
    '''
    num: int
    item: Any=field(compare=False)

    def __init__(self, priority, field):
        self.num = priority
        self.item = field




# --------------------------------------------------------------------------------
# ------------------ The route finding algorithm ---------------------------------
# --------------------------------------------------------------------------------

class FlightZone:
    '''
    The solution class.
    The constructor creates the space (fly zone and no-fly zones). The findPath method
    returns a path between two points. Given a path, plotSolution can draw it.
    '''
    def __init__(self, fly_zone : Zone,
                 no_fly_zones : List[Zone],
                 grid_size = -1):
        '''
        Creates a FlightZone instance given a fly zone and a list of no fly zones.
        To make calculations, the FlightZone will be divided into a grid where each
        block in the grid (i.e. unit cube) will be considered part of the fly zone if
        it intersects the fly zone, and part of a no-fly zone if it intersects a no-fly
        zone. The grid_size parameter controls the size of each grid block, and will be
        automatically set to 1/30 times the hight of the fly zone if not parameter is
        given.
        '''
        self.fly_zone = fly_zone
        self.no_fly_zones = copy.deepcopy(no_fly_zones)
        self.grid_size = grid_size

        # If we did not get a grid_size parameter, we set it to something reasonable
        if grid_size < 0:
            self.grid_size = (fly_zone.top - fly_zone.bottom) / 30


    def findPath(self, start : Point, end: Point) -> List[Point]:
        ''' 
        Uses the A* algorithm to find a path from start to end, that is contained within the
        flight zone and does not intersect a no-fly zone. There is no guarentee as to which
        path will be chosen, but the returned path will only follow grid coordinates or
        diagonals of cubes (i.e. "45 degree diagonals"), except very close to the end point.
        The path will be attempts to approximate of the shortest path that follows those
        restrictions.
        Parameters:
            start: the starting point (a three dimensional Point)
            end:   the endingo point (a three dimensional Point)
        Returns: A list of points (p_1, p_2, ..., p_n) such that the union of the straight
                 lines from point p_i to p_(i+1) creates a path from start to end (i.e.
                 "connecting the dots" forms a path).
                 Returns None if no path exists
        '''

        # If the start point or end point is outside the fly zone, or is contained in
        # a no-fly zone, there does not exist a path
        if not self.fly_zone.contains(start) or not self.fly_zone.contains(end):
            return None
        for nfz in self.no_fly_zones:
            if nfz.contains(start) or nfz.contains(end):
                return None

        # Initialize the data structures we need. Note that we never actually create
        # the full graph, we only create the nodes that we need.

        # elements in the closed list are of the form (point -> [predecessor])
        closed_list = {}

        # elements in the open list are of the form [precedence, point, value, predecessor]
        open_list = [PrioritizedItem(0, [Point(0,0,0), 0, None])]

        # As long as there are places disjoint from us that we did not yet exampine:
        while len(open_list) > 0:
            # We will examine the next, highest priority grid point and check if it has
            # been examined
            current = heapq.heappop(open_list)
            if current.item[0] in closed_list:
                continue

            # Mark our current grid point as seen
            closed_list[current.item[0]] = current.item[2]

            if actualBlock(start, self.grid_size, current.item[0]).contains(end):
                # We found the endpoint! Now, let's retrace the path we took to get here
                reverse_output = [end, actualPoint(start, self.grid_size, current.item[0])]
                cur_point = current.item[0]
                while closed_list[cur_point] is not None:
                    reverse_output.append(actualPoint(start,
                                                      self.grid_size,
                                                      closed_list[cur_point]))
                    cur_point = closed_list[cur_point]
                reverse_output.reverse()
                return reverse_output

            # We're not yet at the end point. Thus, we'll add all neighbors to priority queue
            for nbr in neighbors(current.item[0]):
                if not nbr in closed_list:
                    # If we haven't examined the neighbor:

                    # check if it intersects a forbidden zone or is outside the flight zone,
                    # and if so mark it as seen and ignore it
                    actual_block = actualBlock(start, self.grid_size, nbr)
                    can_fly = True
                    #if not self.fly_zone.intersects(actual_block):
                    if not self.fly_zone.contains(actualPoint(start, self.grid_size, nbr)):
                        can_fly = False
                    else:
                        for fz in self.no_fly_zones:
                            if actual_block.intersects(fz):
                                can_fly = False
                                break
                    if not can_fly:
                        closed_list[nbr] = None
                        continue

                    # Use some matric to choose the priority of this block.
                    # This is somewhat arbitrary, and different metrics produce different
                    # result. This one balances runtime vs. choosing a diagonal looking
                    # path pretty well.
                    distance_left = (eucledeanDistance(actualPoint(start, self.grid_size, nbr), end)
                                     / self.grid_size)
                    distance_to_here = current.item[1] + eucledeanDistance(current.item[0], nbr)
                    precedence = 2 * distance_left + distance_to_here

                    # add it to the priority queue if its not already in it
                    heapq.heappush(open_list,
                        PrioritizedItem(precedence,
                                        [nbr, current.item[1] + 1,
                                            current.item[0]])
                    )
                # END IF
            # End FOR
        # END WHILE

        # If we made it this far there does not exist a path.
        return None


# --------------------------------------------------------------------------------------
# ----------------------------  Helper Methods -----------------------------------------
# --------------------------------------------------------------------------------------

def plotSolution(points : List[Point]):
    '''
    Plots a solution (list of points) so its easy to visualize
    '''
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = []
    y = []
    z = []

    for point in points:
        x.append(point.x)
        y.append(point.y)
        z.append(point.z)

    # Plot the 3D plot
    ax.plot(x, y, z, 'gray')

    # Add the start and end points
    ax.scatter(points[0].x, points[0].y, points[0].z, label = 'start')
    ax.scatter(points[-1].x, points[-1].y, points[-1].z, label = 'end')
    ax.legend()

    # Set the plot title and axis labels
    ax.set_title('Plot of Solution')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Display the plot
    plt.show()


def neighbors(point: Point) -> List[Point]:
    ''' Return the 6 points that differ by at most 1 in each coordinate from
        parameter point '''
    output = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            for k in [-1, 0, 1]:
                output.append(Point(point.x + i, point.y + j, point.z + k))
    return output

def actualBlock(origin : Point, grid_size : float, coordinates : Point):
    '''
    Returns the actual block represented by the coordinates w.r.t the origin and grid_size
    '''
    return Zone(Polygon([
                    Point(origin.x + coordinates.x * grid_size,
                          origin.y + coordinates.y * grid_size),
                    Point(origin.x + (coordinates.x + 1) * grid_size,
                          origin.y + coordinates.y * grid_size),
                    Point(origin.x + (coordinates.x + 1) * grid_size,
                          origin.y + (coordinates.y + 1) * grid_size),
                    Point(origin.x + coordinates.x * grid_size,
                          origin.y + (coordinates.y + 1) * grid_size)
                ]),
                origin.z + coordinates.z * grid_size,
                origin.z + (coordinates.z + 1) * grid_size
    )

def actualPoint(origin : Point, grid_size : float, coordinates : Point):
    '''
    Returns the actual block represented by the coordinates w.r.t the origin and grid_size
    '''
    return Point(origin.x + coordinates.x * grid_size,
                 origin.y + coordinates.y * grid_size,
                 origin.z + coordinates.z * grid_size)

def manhattanDistance(p1 : Point, p2 : Point):
    ''' Returns the Manhattan Distance (L1 distance) between two 3d points '''
    return abs(p1.x - p2.x) + abs(p1.y - p2.y) + abs(p1.z - p2.z)

def eucledeanDistance(p1 : Point, p2 : Point):
    ''' Returns the Eucledean Distance (L2 distance) between two 3d points '''
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)

def divide(point : Point, num : float):
    ''' Returns 1/num * Point '''
    return Point(point.x / num, point.y / num, point.z / num)
