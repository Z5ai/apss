#!/usr/bin/env python
import argparse as ap
import math
import heapq as hq
import io
import Node


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

################################################### a function that takes two corrdinate pairs and returns an approx. distance
def manhattanheuristic(node_a, node_b):
    (x, y) = node_a
    (u, v) = node_b
    return abs(u-x) + abs(v-y)


###################################################
# maze looks like: [['W', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'C'], ['E', 'W', 'E', 'E', 'E', 'E', 'E', 'E', '
# access maze like: maze[x][y] -> x for row(top to bottom) and y for column(left to right)
def astar_search(maze, heuristic=manhattanheuristic):
    '''
    :param maze: a two-dim array containing the characters as in the maze file.
    :param heuristic: a function that takes two coordinate pairs and returns an approx. distance
    :return: shortest path found ...list of coord. pairs
    '''
    start_coord = (9, 0)
    goal_coord = (0, len(maze[0]) - 1)
    start_g = 0
    start_h = manhattanheuristic(start_coord, goal_coord)
    start_f = start_g + start_h
    start_node = Node.Node(start_coord, start_g, start_f)

    queue = [start_node]
    origins = {}
    visited = []

    while queue:

        n = queue.pop(0)
        n_coord = n.coord
        visited.append(n_coord)

        if n_coord == goal_coord:
            break

        nn_coord_list = neighbors(n_coord, maze)
        for nn_coord in nn_coord_list:
            if nn_coord not in visited:
                origins[nn_coord] = n_coord

                nn_g = n.g + 1
                nn_h = heuristic(nn_coord, goal_coord)
                nn_f = nn_g + nn_h

                # visiting occurs, before node is appended to queue (node should never be put into queue a second time).
                # dass der besuchte node noch von einer anderen Seite aus mit einem niedrigerem g-Wert gefunden wird, ist aufgrund
                # der zulässigen heuristik unmöglich. Somit ist es okay, wenn wir den Node höchstens einmal in die queue aufnehmen.
                visited.append(nn_coord)

                queue.append(Node.Node(nn_coord, nn_g, nn_f))
        queue = sorted(queue)

    return reconstruct_path(origins, goal_coord)








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
