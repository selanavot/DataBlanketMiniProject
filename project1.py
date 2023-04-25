''' Solution to Data Blanket Candidate Mini Project 1 '''

import copy
import sys
import random
import math
from typing import List, Tuple
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


# --------------------------------------------------------------------------------
# ----------------------------- Helper Classes -----------------------------------
# --------------------------------------------------------------------------------

class Block:
    '''
    Each block t is an open interval of length (t.end - t.start) whose left endpoint
    can be placed somewhere between t.start - t.delta and t.start + t.delta, inclusively.
    The left endpoint must be strictly less then the right endpoint, and delta may not
    be negative. It has weight (t.W), which may not be negative.
    '''
    def __init__(self, start : float, end : float, delta : float = 0, W : float = 0):
        ''' Constructor, nothing fancy '''
        self.start = start
        self.end = end
        self.W = W
        self.delta = delta

    def __str__(self):
        ''' A string representation of itself: (start, end, delta, W) '''
        output = "(" + str(self.start) + ", " + str(self.end) + ", " + \
                str(self.delta) + ", "  + str(self.W) + ")"
        return output

    def __repr__(self):
        ''' A representation representation of itself: (start, end, delta, W) '''
        output = "(" + str(self.start) + ", " + str(self.end) + ", " + \
                str(self.delta) + ", "  + str(self.W) + ")"
        return output


# --------------------------------------------------------------------------------
# ------------------ Solution 1 - Brute Force (for tiny inputs) ------------------
# --------------------------------------------------------------------------------

def bruteForce(blocks : List[Block], forbidden_zones: List[Block]) \
                                                      -> Tuple[float, List[Block]]:
    '''
    A brute force approach, only to be used for very small inputs since the runtime is
    super-exponential. We did not attempt minor optimizations of this method.

    Parameters:
        blocks (const): a list of blocks, each one with a start point, end point,
                        flexibility (delta), and a value W.
        forbidden_zones (const): a list of blocks that cannot be intersected by any of
                                the other blocks. Each block in this list will be treted
                                as if it has delta = W = 0

    Returns: The maximum sum Σ(Wi) and the list of blocks that obtain this maximum (with
            the adjusted start and end points). See the explanation file for complete
            specs of the problem.

    Constraints: W may not be negative, and the start point may not be greater than the
                endpoint for any block or forbidden zone. The input numbers must not be
                too small or too large, as we will not deal with overflow or rounding
                errors.
    '''
    # Handle the empty case
    if len(blocks) == 0:
        return [0, []]

    # disjointify the forbidden zones (our algorithm does not work if forbidden
    # zones are not disjoint)
    disjoint_fz = disjointify(forbidden_zones)

    # We will iterate over all subsets of blocks and see which one is legal, and
    # provides the maximum value.
    # To iterate over all subsets, we use the fact that each integer from 0 to
    # (2^len(blocks) - 1) corresponds to a unique subset of the blocks using the
    # natural bijection: if blocks = [B_0, B_1, ..., B_{n-1}] and x is an integer
    # in [0, 2^n - 1], we define
    #                f(x) = {B_i: the i'th binary digit of x is 1}
    # Thus, by iterating over all the x's we can iterate over all the subsets.
    maxValue = 0
    maxSubset = []
    for i in range(2 ** len(blocks)):
        # constructs the subset f(i) and calculate the sum of its values
        currentSubset = []
        currentValue = 0
        for j in range(len(blocks)):
            if (i // (2**j) % 2) == 1:
                currentSubset.append(blocks[j])
                currentValue += blocks[j].W

        # Checks if this subset can fit, while not intersecting forbidden zones
        [does, currentSubset] = doesFit(currentSubset + disjoint_fz)

        # if it fits, check if it is the best so far and if so update the maximum
        if does:
            if currentValue > maxValue:
                maxValue = currentValue
                # remove all the sets with value zero from the current subset
                # - they don't contribute, and this way we get rid of the forbidden
                # zones
                maxSubset = []
                for block in currentSubset:
                    if block.W > 0:
                        maxSubset.append(block)

    return [maxValue, maxSubset]


# --------------------------------------------------------------------------------
# ---------------------- Solution 2 - Monte-Carlo method -------------------------
# --------------------------------------------------------------------------------

def approximateSolution(blocks : List[Block],
                        forbidden_zones: List[Block],
                        num_iteration : int = 1024,
                        iter_per_subset: int = 64,
                        temprature : float = -1) -> Tuple[float, List[Block]]:
    '''
    A Monte-Carlo method to estimate the solution efficiently. See the explanation file
    for an explanation of how the algorithm works.

    Parameters:
        blocks (const): a list of blocks, each one with a start point, end point,
                        flexibility (delta), and a value W.
        forbidden_zones (const): a list of blocks that cannot be intersected by any of
                                the other blocks. Each block in this list will be treted
                                as if it has delta = W = 0
        num_iteration: how many subsets we try (more -> more accurate solution)
        iter_per_subset: how hard we try to make subsets work (more -> more accurate)
        temprature: an parameter that controls the "exploration vs. exploitation"
                    tradeoff. (higher T -> more exploration)
    Returns: The sum Σ(Wi), which we estimate is close to the maximum, and a list of
            blocks that obtain this sum (with the adjusted start and end points).
            See the explanation file for complete specs of the problem.
    Constraints: W may not be negative, and the start point may not be greater than the
                endpoint for any block or forbidden zone. The input numbers must not be
                too small or too large, as we will not deal with overflow or rounding
                errors. Temprature, num_iterations, and iter_per_subset may not be less
                then 0.
    '''
    # Handle the empty case
    if len(blocks) == 0:
        return [0, []]

    # If we were not provided with a temperature parameter, we'll choose one
    #  that is proportional to the mean of the values
    if temprature < 0:
        runningSum  = 0
        for block in blocks:
            runningSum += block.W
        temprature = 0.07 * runningSum / len(blocks)
        # Remark: the 0.07 is arbitrary, but it appears to work well. It'd be
        #         interesting to work out what's the optimal temperature, my
        #         guess is that it would not be a linear function of the mean


    # disjointify the forbidden zones (our algorithm does not work if forbidden
    # zones are not disjoint), and make sure they have delta = 0 (by specs,
    # forbidden zones can't move)
    disjoint_fz = disjointify(forbidden_zones)

    # The approximation:
    curSet = np.zeros(len(blocks))  # The current set at each iteration
    newSet = []                      # Proposed new set at each iteration
    newBlocks = []                   # the list of blocks that each new set includes
    bestBlocks = []                  # the best (adjusted) subset of blocks so far
    bestSum = 0                      # optimal value so far
    newSum = 0                       # value of new proposed set
    curSum = 0                       # value of current set

    for i in range(num_iteration):
        # we are going to take, or discard, a random block and put the result
        # in new-set
        randIndex = random.randint(0, len(blocks) - 1)

        newSet = copy.deepcopy(curSet)
        if curSet[randIndex] == 0:
            newSet[randIndex] = 1
            newSum = curSum + blocks[randIndex].W
        else:
            newSet[randIndex] = 0
            newSum = curSum - blocks[randIndex].W

        # check if the new set of intervals can fit
        newBlocks = []
        for j in range(len(blocks)):
            if newSet[j] == 1:
                newBlocks.append(copy.deepcopy(blocks[j]))

        # We check whether the new subset works. If it does and it has better value,
        # we switch to is. If it does but does not have a better value, we switch to
        # it with a certain probability, which is dependent on the temprature and how
        # much we loose by switching.
        if (newSum >= curSum or
               (temprature > 0 and random.random() < math.exp((newSum - curSum) / temprature))):
            [does, newBlocks] = doesFit(newBlocks + disjoint_fz, iter_per_subset)
            if does:
                curSet = newSet
                curSum = newSum

                # If we found a better subset than the best known, we update bestBlocks
                if newSum > bestSum:
                    bestSum = newSum
                    bestBlocks = []
                    for block in newBlocks:
                        # Only include blocks with non-zero value, so we don't add
                        # forbidden zones
                        if block.W > 0:
                            bestBlocks.append(block)

    return [bestSum, bestBlocks]


# --------------------------------------------------------------------------------
# ------------------------------ helper methods ----------------------------------
# --------------------------------------------------------------------------------

def doesFitInOrder(blocks : List[Block]) -> bool:
    '''
    Checks whether an ordered list of blocks can fit without intersecting, in the order
    that they're listed. If so, it returns True and modifies the input so the blocks
    fit. Returns False otherwise, and the input may be modified.
    This is an efficient function, running in O(len(blocks))
    This methods alters the input.
    '''
    # If the list is empty, the blocks can fit!
    if len(blocks) == 0:
        return True

    # currentLocation keeps track on the highest occupied point so far.
    currentLocation : float

    # put first block as early as possible - from (start - delta) to (end - delta)
    currentLocation = blocks[0].end - blocks[0].delta
    blocks[0].start -= blocks[0].delta
    blocks[0].end -= blocks[0].delta

    for i in range(1, len(blocks)):
        # If there is a point occupied further left than the latest possible start
        # point of blocks[i], there is no solution. Otherwise, place blocks[i] as
        # far left as possible.
        if blocks[i].start + blocks[i].delta < currentLocation:
            return False
        length = blocks[i].end - blocks[i].start
        currentLocation = max(currentLocation, blocks[i].start - blocks[i].delta) \
                            + length
        blocks[i].end = currentLocation
        blocks[i].start = currentLocation - length
    # If we have made it this far, all the blocks fit :)
    return True


def doesFit(blocks : List[Block], max_num_iterations : int = sys.maxsize)\
                                                        -> Tuple[bool, List[Block]]:
    '''
    Checks whether there exist an order in which a list of blocks can fit without
    intersecting. If so, it returns [True, list_of_modified_blocks_that_fit]. Returns
    [False, []] otherwise.

    With bad input, this method may take a very long time. Thus, one can limit the number
    of iterations via the max_num_iterations parameter. In this case the method may have
    a false negative (but never a false positive).

    How it works: We build a directed graph (DAG) where each node corresponds to a block,
    and has an edge from B1 to B2 if B1 must come before B2 in a possible ordering of the
    blocks. Thus, the ordering in any fitting must be a topological sort of the graph. We
    will iterate through all topological sorts of the graph to see if one works.
    
    Note that if there are few topological sorts (e.g. if all the deltas are small compared
    to the distance between the intervals). If there are many topological sorts and there
    exists one that works, it is likely that many topological sorts work and we'll find
    one within a reasonable number of iterations.
    '''
    # Handle the empty case
    if len(blocks) == 0:
        return [True, []]

    # Build the directed graph. We use the networkx library.
    G = nx.DiGraph()

    # Add the nodes corresponding to each block (block name is the index of the block)
    for i in range(len(blocks)):
        G.add_node(i)

    # If we add the edges (k,l) then block k must be before block l
    for k in range(len(blocks)):
        for l in range(k + 1, len(blocks)):
            # if the earliest possible end time of l is later than the latest possible
            # start time of k, then we add the edge (k, l), and vice versa
            if blocks[l].end - blocks[l].delta > blocks[k].start + blocks[k].delta:
                G.add_edge(k, l)
            if blocks[k].end - blocks[k].delta > blocks[l].start + blocks[l].delta:
                G.add_edge(l,k)

    # If G is cyclic, there does not exist a topological sort so the intervals don't fit
    if not nx.is_directed_acyclic_graph(G):
        return [False, List[Block]]

    # Otherwise, iterate through all topological sorts of G and check if one works, or
    # until the number of iterations reaches max_num_iterations
    counter = 0
    for topo_sort in nx.algorithms.dag.all_topological_sorts(G):
        if counter >= max_num_iterations:
            break

        current_vertices = []

        for i in topo_sort:
            current_vertices.append(copy.deepcopy(blocks[i]))

        if doesFitInOrder(current_vertices):
            return [True, current_vertices]

        counter += 1

    # If we made it this far, no topological sort works so the blocks don't fit :(
    return [False, []]


def disjointify(intervals: List[Block]) -> list[Block]:
    '''
    Given a set of blocks (open intervals), returns a set of interval that are disjoint
    This function sets W = delta = 0 for each block (prior information will be ignored).
    The returned list will be sorted by start point.
    Does not modify the input.
    Used to disjointify the forbidden zones.
    '''

    # Take care of empty inputs
    if len(intervals) == 0:
        return []

    # Make a sorted copy of the input so we do not change the input
    sortedList = copy.deepcopy(intervals)
    sortedList.sort(key = lambda x: x.start)

    # Put all the intervals into output, merging the ones that intersect
    output = []
    output.append(sortedList[0])
    for i in range(1, len(sortedList)):
        if output[-1].end > sortedList[i].start:
            output[-1] = Block(output[-1].start, max(output[-1].end, sortedList[i].end))
        else:
            output.append(Block(sortedList[i].start, sortedList[i].end))

    return output
