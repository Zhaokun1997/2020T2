# searchGeneric.py - Generic Searcher, including depth-first and A*
# AIFCA Python3 code Version 0.8.1 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from display import Displayable, visualize


class Searcher(Displayable):
    """returns a searcher for a problem.
    Paths can be found by repeatedly calling search().
    This does depth-first search unless overridden
    """

    def __init__(self, problem):
        """creates a searcher from a problem
        """
        self.problem = problem
        self.initialize_frontier()
        self.num_expanded = 0
        self.add_to_frontier(Path(problem.start_node()))
        super().__init__()

    def initialize_frontier(self):
        self.frontier = []

    def empty_frontier(self):
        return self.frontier == []

    def add_to_frontier(self, path):
        self.frontier.append(path)

    @visualize
    def search(self):
        """returns (next) path from the problem's start node
        to a goal node. 
        Returns None if no path exists.
        """
        while not self.empty_frontier():
            path = self.frontier.pop()
            self.display(2, "Expanding:", path, "(cost:", path.cost, ")")
            self.num_expanded += 1
            if self.problem.is_goal(path.end()):  # solution found
                self.display(1, self.num_expanded, "paths have been expanded and",
                             len(self.frontier), "paths remain in the frontier")
                self.solution = path  # store the solution found
                return path
            else:
                neighs = self.problem.neighbors(path.end())
                # neighs = sorted(neighs, key=lambda x: (x.from_node, x.to_node))
                self.display(3, "Neighbors are", neighs)
                for arc in reversed(list(neighs)):
                    self.add_to_frontier(Path(path, arc))
                self.display(3, "Frontier:", self.frontier)
        self.display(1, "No (more) solutions. Total of",
                     self.num_expanded, "paths expanded.")


class BFSearcher(Searcher):
    def __init__(self, problem):
        super().__init__(problem)
        self.frontier_city = []
        self.expanded_city = []
        self.add_to_frontier_city(Path(problem.start_node()).end())

    def add_to_frontier_city(self, city):
        self.frontier_city.append(city)

    def add_to_expanded_city(self, city):
        self.expanded_city.append(city)

    @visualize
    def search(self):
        path = Path(None)
        while not self.empty_frontier():
            path = self.frontier.pop(0)
            self.add_to_expanded_city(path.end())

            self.frontier_city.remove(path.end())
            self.display(2, "Expanding:", path, "(cost:", path.cost, ")")
            self.num_expanded += 1

            neighbors = self.problem.neighbors(path.end())
            self.display(3, "Neighbors are", neighbors)

            for arc in neighbors:
                if (arc.to_node not in self.expanded_city) or (arc.to_node in self.frontier_city):
                    self.add_to_frontier(Path(path, arc))
                    self.frontier_city.append(Path(path, arc).end())
                    self.display(3, "Frontier:", self.frontier)
                    if self.problem.is_goal(arc.to_node):  # solution found
                        self.display(1, self.num_expanded, "paths have been expanded and",
                                     len(self.frontier), "paths remain in the frontier")
                        self.solution = Path(path, arc)
                        return Path(path, arc)


import heapq  # part of the Python standard library
from searchProblem import Path


class FrontierPQ(object):
    """A frontier consists of a priority queue (heap), frontierpq, of
        (value, index, path) triples, where
    * value is the value we want to minimize (e.g., path cost + h).
    * index is a unique index for each element
    * path is the path on the queue
    Note that the priority queue always returns the smallest element.
    """

    def __init__(self):
        """constructs the frontier, initially an empty priority queue 
        """
        self.frontier_index = 0  # the number of items ever added to the frontier
        self.frontierpq = []  # the frontier priority queue

    def empty(self):
        """is True if the priority queue is empty"""
        return self.frontierpq == []

    def add(self, path, value):
        """add a path to the priority queue
        value is the value to be minimized"""
        self.frontier_index += 1  # get a new unique index
        heapq.heappush(self.frontierpq, (value, -self.frontier_index, path))

    def pop(self):
        """returns and removes the path of the frontier with minimum value.
        """
        (_, _, path) = heapq.heappop(self.frontierpq)
        return path

    def count(self, val):
        """returns the number of elements of the frontier with value=val"""
        return sum(1 for e in self.frontierpq if e[0] == val)

    def __repr__(self):
        """string representation of the frontier"""
        return str([(n, c, str(p)) for (n, c, p) in self.frontierpq])

    def __len__(self):
        """length of the frontier"""
        return len(self.frontierpq)

    def __iter__(self):
        """iterate through the paths in the frontier"""
        for (_, _, path) in self.frontierpq:
            yield path


class AStarSearcher(Searcher):
    """returns a searcher for a problem.
    Paths can be found by repeatedly calling search().
    """

    def __init__(self, problem):
        super().__init__(problem)

    def initialize_frontier(self):
        self.frontier = FrontierPQ()

    def empty_frontier(self):
        return self.frontier.empty()

    def add_to_frontier(self, path):
        """add path to the frontier with the appropriate cost"""
        # value = path.cost + self.problem.heuristic(path.end())
        value = self.problem.heuristic(path.end())
        self.frontier.add(path, value)


import searchProblem as searchProblem


def test(SearchClass, problem=searchProblem.problem1, solution=['g', 'd', 'c', 'b', 'a']):
    """Unit test for aipython searching algorithms.
    SearchClass is a class that takes a problemm and implements search()
    problem is a search problem
    solution is the unique (optimal) solution. 
    """
    print("Testing problem 1:")
    schr1 = SearchClass(problem)
    path1 = schr1.search()
    print("Path found:", path1)
    assert path1 is not None, "No path is found in problem1"
    assert list(path1.nodes()) == solution, "Shortest path not found in problem1"
    print("Passed unit test")


if __name__ == "__main__":
    # test(Searcher)
    test(AStarSearcher)

# example queries:
# searcher1 = Searcher(searchProblem.acyclic_delivery_problem)   # DFS
# searcher1.search()  # find first path
# searcher1.search()  # find next path
# searcher2 = AStarSearcher(searchProblem.acyclic_delivery_problem)   # A*
# searcher2.search()  # find first path
# searcher2.search()  # find next path
# searcher3 = Searcher(searchProblem.cyclic_delivery_problem)   # DFS
# searcher3.search()  # find first path with DFS. What do you expect to happen?
# searcher4 = AStarSearcher(searchProblem.cyclic_delivery_problem)    # A*
# searcher4.search()  # find first path
