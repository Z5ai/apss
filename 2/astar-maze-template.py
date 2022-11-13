#!/usr/bin/env python
import argparse as ap
import math
import heapq as hq
import io
from enum import Enum

import Node


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

def load_maze_file(maze_filename):
    '''
    Simply read in the maze as 2-dim array.
    :param maze_filename:
    :return: a two-dim array containing the same characters as in the maze file.
    '''
    maze = []

    with io.open(maze_filename, 'r') as mazefile:
        for row in mazefile:
            if not row.startswith("#"):
                maze.append(row.strip().split(sep=','))

    return maze






def neighbors(node, maze):
    '''
    Considering walls and the outer frame, returns the possible neighbor nodes of a given coordinate.
    :param node: the node as (x,y) tuple/coordinate for which possible neighbors shall be determined
    :param maze: a two-dim array containing the characters as in the maze file.
    :return: list of neighbor coordinate pairs
    '''
    (x, y) = node
    neighbor_pos = []

    if x > 0 and maze[x-1][y] != 'W':
        neighbor_pos.append((x-1, y))
    if y > 0 and maze[x][y-1] != 'W':
        neighbor_pos.append((x, y-1))
    if 0 <= x < len(maze)-1 and maze[x+1][y] != 'W':
        neighbor_pos.append((x+1, y))
    if 0 <= y < len(maze)-1 and maze[x][y+1] != 'W':
        neighbor_pos.append((x, y+1))

    return neighbor_pos


def reconstruct_path(origins, node):
    '''
    Starting from node, reconstruct the chosen path
    :param origins: a dict that stores for each node, the node from which it has been reached
    :param node: the node from which the path shall be reconstructed (endnode)
    '''
    path = [node]

    while node in origins.keys():
        node = origins[node]
        path.append(node)

    path.reverse()

    return path



def dfs(maze):
    start_coord = (len(maze)-1, 0)
    goal_coord = (0, len(maze[0]) - 1)

    queue = [start_coord]
    visited = [start_coord]
    origins = {}

    while queue:
        n = queue.pop()
        if n == goal_coord:
            return reconstruct_path(origins, goal_coord)
        nn_list = neighbors(n, maze)
        for nn in nn_list:
            if nn not in visited:
                visited.append(nn)
                origins[nn] = n
                queue.append(nn)


def get_direction(coord_old, coord):
    (x, y) = coord_old
    (x2, y2) = coord

    if x2 - x == 1:
        return Direction.DOWN
    elif x2 - x == -1:
        return Direction.UP
    elif y2 - y == 1:
        return Direction.RIGHT
    elif y2 - y == -1:
        return Direction.LEFT


def reduce_path_to_corner_coord(path):
    n_old = path.pop(0)
    path_corner_coord = [n_old]
    n = path.pop(0)
    direction_old = get_direction(n_old, n)
    n_old = n   # direction_old is now the direction to n_old

    while len(path) != 1:
        n = path.pop(0)
        direction = get_direction(n_old, n)  # direction is now the direction to n

        if direction != direction_old:
            path_corner_coord.append(n_old)

        direction_old = direction
        n_old = n                           # direction_old is now the direction to n_old

    path_corner_coord.append(path[0])
    return path_corner_coord


def improve(initial_path):



###################################################
# maze looks like: [['W', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'C'], ['E', 'W', 'E', 'E', 'E', 'E', 'E', 'E', '
# access maze like: maze[x][y] -> x for row(top to bottom) and y for column(left to right)
def simulated_annealing(maze):
    '''
    :param maze: a two-dim array containing the characters as in the maze file.
    :return: shortest path found ...list of coord. pairs
    '''
    initial_path = dfs(maze)
    return improve(initial_path)










def main():
    parser = ap.ArgumentParser(description="A Maze Solver based on AStar.")
    parser.add_argument("mazefile", type=str, help="filename of the the maze file to load")
    args = parser.parse_args(args=["medium.maze"])   #################### if you do not anotate a default value, you can probably enter the exact value in the terminal

    # 1. load the maze
    maze = load_maze_file(args.mazefile)
    # 2. call AStar with different heuristics to see the effects ;)
    shortest_path = astar_search(maze, heuristic=manhattanheuristic)
    print("Path:")
    print(shortest_path)

    print_maze(maze, shortest_path)

def print_maze(maze, path=None):
    out = ""
    for i in range(0, len(maze)):
        for j in range(0, len(maze[i])):
            if path:
                if (i,j) in path:
                    out += " X "
                else:
                    out += " " + str(maze[i][j]) + " "
            else:
                out += " " + str(maze[i][j]) + " "
        out += "\n"
    print(out)

if __name__ == "__main__":
    main()
