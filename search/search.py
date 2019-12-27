# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from collections import deque
import util
import sys
import node

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """ 

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    n=node.Node(problem.getStartState(), None, None, 0)
    if problem.isGoalState(n.state): 
        return n.total_path()
    fringe = util.Stack()
    fringe.push(n)
    generated = {}
    generated[n.state] = [n,'F']
    while True:
        if fringe.isEmpty():
            print "No solution"
            sys.exit()
        n = fringe.pop()
        generated[n.state] = [n,'E']
        for state, action, cost in problem.getSuccessors(n.state):
            ns = node.Node(state, n, action, cost)
            if ns.state not in generated:
                if problem.isGoalState(ns.state):
                    return ns.total_path()
                fringe.push(ns)
                generated[ns.state] = [ns, 'F']

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    n=node.Node(problem.getStartState(), None, None, 0)
    if problem.isGoalState(n.state): 
        return n.total_path()
    fringe = util.Queue()
    fringe.push(n)
    generated = {}
    generated[n.state] = [n,'F']
    while True:
        if fringe.isEmpty():
            print "No solution"
            sys.exit()
        n = fringe.pop()
        generated[n.state] = [n,'E']
        for state, action, cost in problem.getSuccessors(n.state):
            ns = node.Node(state, n, action, cost)
            if ns.state not in generated:
                if problem.isGoalState(ns.state):
                    return ns.total_path()
                fringe.push(ns)
                generated[ns.state] = [ns, 'F']

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    n=node.Node(problem.getStartState(), None, None, 0)
    fringe = util.PriorityQueue()
    fringe.push(n, n.cost)
    generated = {}
    generated[n.state] = [n, 'F']
    while True:
        if fringe.isEmpty():
            print "No solution"
            sys.exit()
        n = fringe.pop()
        if generated.get(n.state, None)[0] == n:
            if problem.isGoalState(n.state):
                return n.total_path()
            generated[n.state] = [n, 'E']
            for state, action, cost in problem.getSuccessors(n.state):
                ns = node.Node(state, n, action, cost)
                if ns.state not in generated:
                    fringe.push(ns, ns.cost)
                    generated[ns.state] = [ns, 'F']
                else:
                    nx = generated.get(ns.state, None)[0]
                    if ns.cost < nx.cost:
                        fringe.push(ns, ns.cost)
                        generated[ns.state] = [ns, 'F']
    util.raiseNotDefined()

def iterativeDeepeningSearch(problem):
    while True:
        (path, cut) = depthLimitSearch(problem, 1)
        if cut == True:
            sys.exit(1)
        return path

def depthLimitedSearch(problem, k):
    while True:
        (path, cut) = depthLimitSearch(problem, k)
        if cut== True:
            sys.exit(1)
        return path

def depthLimitSearch(problem, k):

    n=node.Node(problem.getStartState(), None, None, 0, 1)
    if problem.isGoalState(n.state): 
        return (n.total_path(), False)
    fringe = util.Stack()
    fringe.push(n)
    generated = {}
    generated[n.state] = [n,'F']
    cut = False
    while True:
        if fringe.isEmpty():
            print "No solution"
            return ([], False)
        n = fringe.pop()
        if n.depth == k:
            cut = True
        else:
            generated[n.state] = [n,'E']
            for state, action, cost in problem.getSuccessors(n.state):
                ns = node.Node(state, n, action, cost, n.depth +1)
                if ns.state not in generated:
                    if problem.isGoalState(ns.state):
                        return (ns.total_path(), cut)
                    fringe.push(ns)
                    generated[ns.state] = [ns, 'F']

    util.raiseNotDefined()

def nullHeuristic(state=None, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def bestFirstSearch(problem, heuristic=nullHeuristic()):

    n=node.Node(problem.getStartState(), None, None, 0)
    fringe = util.PriorityQueue()
    fringe.push(n, heuristic(n.state, problem))
    generated = {}
    generated[n.state] = [n, 'F']
    while True:
        if fringe.isEmpty():
            print "No solution"
            sys.exit()
        n = fringe.pop()
        if generated.get(n.state, None)[0] == n: 
            if problem.isGoalState(n.state):
                return n.total_path()
            generated[n.state] = [n, 'E']
            for state, action, cost in problem.getSuccessors(n.state):
                ns = node.Node(state, n, action, cost)
                if ns.state not in generated:
                    fringe.push(ns, heuristic(ns.state, problem))
                    generated[ns.state] = [ns, 'F']
                else:
                    nx = generated.get(ns.state, None)[0]
                    if ns.cost < nx.cost:
                        fringe.push(ns, heuristic(ns.state, problem))
                        generated[ns.state] = [ns, 'F']
                
    util.raiseNotDefined()

def aStarSearch(problem, heuristic=nullHeuristic()):
    """Search the node that has the lowest combined cost and heuristic first."""
    n=node.Node(problem.getStartState(), None, None, 0)
    fringe = util.PriorityQueue()
    fringe.push(n, n.cost + heuristic(n.state, problem))
    generated = {}
    generated[n.state] = [n, 'F']
    while True:
        if fringe.isEmpty():
            print "No solution"
            sys.exit()
        n = fringe.pop()
        if generated.get(n.state, None)[0] == n: 
            if problem.isGoalState(n.state):
                return n.total_path()
            generated[n.state] = [n, 'E']
            for state, action, cost in problem.getSuccessors(n.state):
                ns = node.Node(state, n, action, cost)
                if ns.state not in generated:
                    fringe.push(ns, ns.cost + heuristic(ns.state, problem))
                    generated[ns.state] = [ns, 'F']
                else:
                    nx = generated.get(ns.state, None)[0]
                    if ns.cost < nx.cost:
                        fringe.push(ns, ns.cost + heuristic(ns.state, problem))
                        generated[ns.state] = [ns, 'F']

    util.raiseNotDefined()

def bidirectionalSearch(problem):
    
    ni=node.Node(problem.getStartState(), None, None, 0)
    nf=node.Node(problem.goal, None, None, 0)
    if ni.state == nf.state:
        return ni.total_path()
    fringe_initial = util.Queue()
    fringe_final = util.Queue()
    fringe_initial.push(ni)
    fringe_final.push(nf)
    generated = {}
    generated[ni.state] = [ni,'F','i']
    generated[nf.state] = [nf,'F','f']
    while True:
        if fringe_initial.isEmpty() and fringe_final.isEmpty():
            print "No solution"
            sys.exit()
        ni = fringe_initial.pop()
        nf = fringe_final.pop()
        generated[ni.state] = [ni,'E','i']
        generated[nf.state] = [nf,'F','f']
        for state, action, cost in problem.getSuccessors(ni.state):
            nsi = node.Node(state, ni, action, cost)
            if nsi.state not in generated:
                fringe_initial.push(nsi)
                generated[nsi.state] = [nsi, 'F','i']
            elif generated.get(nsi.state)[2] == 'f':
                return nsi.total_path() + generated.get(nsi.state)[0].total_path()[::-1]  #Suma la lista inicial con la lista inversa del final
        for state, action, cost in problem.getSuccessors(nf.state):
            nsf = node.Node(state, nf, action, cost)
            if nsf.state not in generated:
                fringe_initial.push(nsf)
                generated[nsf.state] = [nsf, 'F','f']
            elif generated.get(nsf.state)[2] == 'i':
                return generated.get(nsf.state)[0].total_path() + nsf.total_path()[::-1]  #Suma la lista inicial con la lista inversa final
                
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
dls = depthLimitedSearch
bfsh = bestFirstSearch
ids = iterativeDeepeningSearch
bds = bidirectionalSearch