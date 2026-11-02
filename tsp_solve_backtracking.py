import math
import random

from utils import Tour, SolutionStats, Timer, score_tour, Solver, score_partial_tour
from cuttree import CutTree


def random_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    while True:
        if timer.time_out():
            return stats

        tour = random.sample(list(range(len(edges))), len(edges))
        n_nodes_expanded += 1

        cost = score_tour(tour, edges)
        if math.isinf(cost):
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        if stats and cost > stats[-1].score:
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        stats.append(SolutionStats(
            tour=tour,
            score=cost,
            time=timer.time(),
            max_queue_size=1,
            n_nodes_expanded=n_nodes_expanded,
            n_nodes_pruned=n_nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]


def get_min_index(weights, current, visited):  # time - O(n)
    min_weight = float('inf')
    min_index = len(weights)
    for i, weight in enumerate(weights):  # time = O(n)
        if weight < min_weight and i != current and i not in visited:
            min_weight = weight
            min_index = i
    return min_index


def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:  # time = O(n^3), space = O(n^2)
    solutions = []  # space = O(n^2) - holds up to n solutions each of length n
    best = float('inf')
    for i in range(len(edges)):  # time = O(n) - tries all possible starting positions
        visited = set()  # space = O(n)
        visited.add(i)
        current = i
        solution = [i]  # space = O(n)
        while len(visited) != len(edges):  # time = O(n)
            next_node = get_min_index(edges[current], current, visited)  # time = O(n)
            if next_node == len(edges):  # no neighbors
                break
            current = next_node
            visited.add(current)
            solution.append(current)
        time_out = timer.time_out()
        if time_out:
            return solutions
        else:
            score = score_tour(solution, edges)
            time = timer.time()
            if len(solution) == len(edges) and edges[current][i] != float('inf') and score < best:
                solutions.append(SolutionStats(solution, score, time, 0, 0, 0, 0, 0))
                best = score
    return solutions


def is_solution(current, i, last_node, edges): # time/space = O(1)
    if len(current) + 1 != len(edges):
        return False
    elif edges[last_node][i] == float('inf'):
        return False
    else:
        return True


def dfs(best, timer, edges, is_bssf):
    print(f"time = {timer.time()}")
    solutions = []  # space = O(n^2) - up to n solutions each of size n
    stack = [[0]]  # up to 2^n
    while stack and not timer.time_out():
        current = stack.pop()
        last_node = current[-1]
        visited = set()
        for node in current:  # Time - up to O(n)
            visited.add(node)
        for i in range(1, len(edges)):  # Time - up to O(n)
            if i not in visited:
                if is_solution(current, i, last_node, edges):
                    solution = current.copy()  # space / time = O(n)
                    solution.append(i)
                    score = score_tour(solution, edges)
                    if score < best:
                        best = score
                        time = timer.time()
                        solutions.append(SolutionStats(solution, score, time, 0, 0, 0, 0, 0))
                else:
                    possible_path = current.copy()  # space / time = O(n)
                    possible_path.append(i)
                    if not is_bssf or score_partial_tour(possible_path, edges) < best:
                        stack.append(possible_path)
    return solutions


def backtracking(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    best = float('inf')
    return dfs(best, timer, edges, False)


def backtracking_bssf(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    solutions = greedy_tour(edges, timer)
    best = float('inf')
    for solution in solutions:
        if solution.score < best:
            best = solution.score
    solutions.extend(dfs(best, timer, edges, True))
    return solutions



