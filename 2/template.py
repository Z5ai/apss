#!/usr/bin/env python
from copy import *

import argparse as ap
import math
import heapq as hq
import io
# to start with, we will need matplotlib.pyplot
import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
import random

path = []
paths = dict()
T_max = 100

def load_maze_file(maze_filename):
    '''
    Simply read in the maze as 2-dim array.
    :param maze_filename:
    :return: a two-dim array containing the same characters as in the maze file.
    '''
    maze = []
    starting_node = None
    goal_node = None

    # we find M and C here already as we traverse the file anyway

    with io.open(maze_filename, 'r') as mazefile:
        row_counter = 0
        for row in mazefile:
            if not row.startswith("#"):
                row_list = row.strip().split(sep=',')
                maze.append(row_list)
                if "M" in row_list:
                    starting_node = (row_counter, row_list.index("M"))
                if "C" in row_list:
                    goal_node = (row_counter, row_list.index("C"))
                row_counter += 1

    if starting_node == None:
        print("Could not find Mouse in maze: " + maze_filename)
        exit(1)
    if goal_node == None:
        print("Could not find Cheese in maze: " + maze_filename)
        exit(1)

    return maze, starting_node, goal_node


def find_initial_solution(maze, starting_node, goal_node,val):
    '''
    Considering walls and the outer frame, returns the possible neighbour nodes of a given coordinate.
    :param node: the node as (x,y) tuple/coordinate for which possible neighbours shall be determined
    :param maze: a two-dim array containing the characters as in the maze file.
    :return: list of neighbour coordinate pairs
    '''
    (s_x,s_y)=starting_node
    (g_x,g_y)=goal_node
    global paths
    
    xdir = 1 if (g_x - s_x > 0) else -1
    ydir = 1 if (g_y - s_y > 0) else -1

    n_path = [starting_node]
    loop = True

    while loop:
        (c_x, c_y) = n_path[0]

        opts = []
        if c_x+xdir < len(maze) and c_x+xdir>= 0:
            opts.append((c_x+xdir, c_y))
        
        if c_y+ydir < len(maze) and c_y+ydir>= 0:
            opts.append((c_x, c_y+ydir))
                
        if opts:
            n_path.insert(0,random.choice(opts))
        else: 
            loop = False

    # from timepoint val, n_path contains several solutions
    paths[val] = n_path

def check_U(four_chain):
    # x goes to bottom, y goes to right
    (xs, ys) = four_chain[0]
    (x1, y1) = four_chain[1]
    (x2, y2) = four_chain[2]
    (xe, ye) = four_chain[3]
    # mid_segment is horizontal
    if x2 - x1 == 0:
        if xs == xe and ys == y1 and ye == y2:
            return True
    # mid_segment is vertical
    else:
        if ys == ye and xs == x1 and xe == x2:
            return True
    return False

def check_L(three_chain):
    [s, m, e] = three_chain
    (xs, ys) = s
    (xm, ym) = m
    (xe, ye) = e
    if xs == xm == xe or ys == ym == ye:
        return True

def replace_chain(path, replacement_indexes, replacement_chain):
    start_chain = path[:replacement_indexes[0]]
    end_chain = path[replacement_indexes[-1]+1:]
    return start_chain + replacement_chain + end_chain

def replacement_chain_for_three_chain(three_chain, path):
    [s, m, e] = three_chain
    (xs, ys) = s
    (xe, ye) = e
    m1 = (xs, ye)
    m2 = (xe, ys)
    if m == m1:
        if m2 not in path:
            return [s, m2, e]
    else:
        if m1 not in path:
            return [s, m1, e]
    return [s, m, e]

def replacement_chain_for_two_chain(two_chain, path, maze_size):
    coin = random.randint(0, 1)
    (x0, y0) = two_chain[0]
    (x1, y1) = two_chain[1]

    # segment is horizontal
    if x1 - x0 == 0:

        if x0 == 0:
            if x0+1 not in path and x1+1 not in path:
                return [two_chain[0], (x0+1,y0), (x1+1,y1),two_chain[1]]
            else:
                return two_chain

        elif x0 == maze_size['x']-1:
            if x0-1 not in path and x1-1 not in path:
                return [two_chain[0], (x0-1,y0), (x1-1,y1),two_chain[1]]
            else:
                return two_chain

        else:
            match coin:
                case 0:
                    if x0+1 not in path and x1+1 not in path:
                        return [two_chain[0], (x0 + 1, y0), (x1 + 1, y1), two_chain[1]]
                    elif x0-1 not in path and x1-1 not in path:
                        return [two_chain[0], (x0 - 1, y0), (x1 - 1, y1), two_chain[1]]
                    else:
                        return two_chain
                case 1:
                    if x0-1 not in path and x1-1 not in path:
                        return [two_chain[0], (x0-1, y0), (x1-1, y1), two_chain[1]]
                    elif x0+1 not in path and x1+1 not in path:
                        return [two_chain[0], (x0+1, y0), (x1+1, y1), two_chain[1]]
                    else:
                        return two_chain

    # segment is vertical
    else:

        if y0 == 0:
            if y0+1 not in path and y1+1 not in path:
                return [two_chain[0], (x0, y0+1), (x1, y1+1), two_chain[1]]
            else:
                return two_chain

        elif y0 == maze_size['y'] - 1:
            if y0 - 1 not in path and y1 - 1 not in path:
                return [two_chain[0], (x0, y0-1), (x1, y1-1), two_chain[1]]
            else:
                return two_chain

        else:
            match coin:
                case 0:
                    if y0+1 not in path and y1+1 not in path:
                        return [two_chain[0], (x0, y0+1), (x1, y1+1), two_chain[1]]
                    elif y0-1 not in path and y1-1 not in path:
                        return [two_chain[0], (x0, y0-1), (x1, y1-1), two_chain[1]]
                    else:
                        return two_chain
                case 1:
                    if y0-1 not in path and y1-1 not in path:
                        return [two_chain[0], (x0, y0-1), (x1, y1-1), two_chain[1]]
                    elif y0+1 not in path and y1+1 not in path:
                        return [two_chain[0], (x0, y0+1), (x1, y1+1), two_chain[1]]
                    else:
                        return two_chain

def find_neighbor(path, maze_size):
    last_index = len(path) - 1

    # 1. investigate four_chain
    index_first_four_chain = random.randint(0, last_index-3)
    replacement_indexes = [i for i in range(index_first_four_chain, index_first_four_chain + 4)]
    four_chain = [path[index] for index in replacement_indexes]
    if check_U(four_chain):
        # no boundary checking required at all
        replacement_chain = four_chain[1:3]
        return replace_chain(path, replacement_indexes, replacement_chain)

    # 2. investigate three_chain
    index_first_three_chain = index_first_four_chain + random.randint(0, 1)
    replacement_indexes = [i for i in range(index_first_three_chain, index_first_three_chain + 3)]
    three_chain = [path[index] for index in replacement_indexes]
    if check_L(three_chain) == True:
        # boundary checking in replacement_chain_for_three_chain() done
        replacement_chain = replacement_chain_for_three_chain(three_chain, path)
        return replace_chain(path, replacement_indexes, replacement_chain)

    # 3. investigate two_chain
    index_first_two_chain = index_first_four_chain + random.randint(0, 2)
    replacement_indexes = [i for i in range(index_first_two_chain, index_first_two_chain + 2)]
    two_chain = [path[index] for index in replacement_indexes]
    # boundary checking in replacement_chain_for_two_chain() required
    replacement_chain = replacement_chain_for_two_chain(two_chain, path, maze_size)
    return replace_chain(path, replacement_indexes, replacement_chain)

def eval(path, maze):
    # for each step -1 as penalty, for each wall -10 as penalty
    penalty = 0
    for node in path:
        (x, y) = node
        if maze[x][y] == 1:
            penalty -= 10
        else:
            penalty -= 1
    return penalty


def g(t):
    return T_max * math.exp(-t)


def sim_annealing_search(maze, starting_node, goal_node):
    '''
    :param maze: a two-dim array containing the characters as in the maze file.
    :param heuristic: a function that takes two corrdinate pairs and returns an approx. distance
    :return: shortest path found ...list of coord. pairs
    '''
    maze_size = {'x':len(maze), 'y':len(maze[0])}


    find_initial_solution(maze, starting_node, goal_node, 0)
    path_c = paths[0]
    # contrary to slide 44 leave green iteration out, which is just for, if you want not to decrease T in each iteration
    for t in range(1, 30):
        T = g(t)
        path_n = find_neighbor(path_c, maze_size)
        if eval(path_c, maze) < eval(path_n, maze):
            path_c = path_n
        elif random.random() < math.exp((eval(path_n, maze)-eval(path_c, maze))/T):
            path_c = path_n
        paths[t] = path_c
    viz_maze(maze,30)
    
def main():
    # Start from your command line:
    # C:/ProgramData/Anaconda3/python.exe "c:/Users/marcr/Desktop/Master 1/APSS/Exercises/Exercise 1/astar-maze-template.py" hard.maze
    parser = ap.ArgumentParser(description="A Maze Solver based on AStar.")
    parser.add_argument("mazefile", type=str, help="filename of the the maze file to load")
    args = parser.parse_args(args=["hard.maze"])

    # 1. load the maze
    maze, starting_node, goal_node = load_maze_file(args.mazefile)

    print(len(maze), len(maze[0]))
    
    maze = numeric_maze(maze)

    # 2. call simulated annealing
    sim_annealing_search(maze, starting_node, goal_node)
    pass


### Encodes the maze in numeric values for display
def numeric_maze(maze):
    '''
    :param maze: a two-dim array containing the numbers encoding the maze
    '''
    mazeviz = maze.copy()
    for row in range(len(mazeviz)):
        for cell in range(len(mazeviz[row])):
            if mazeviz[row][cell] == "E":
                mazeviz[row][cell] = 0
            if mazeviz[row][cell] == "W":
                mazeviz[row][cell] = 1
            if mazeviz[row][cell] == "M":
                mazeviz[row][cell] = 2
            if mazeviz[row][cell] == "C":
                mazeviz[row][cell] = 3
    return mazeviz

### Combines a maze with a the path in the val position
def maze_with_path(maze,path_key):
    '''
    :param maze: a two-dim array containing the numbers encoding the maze
    :param path_key: the key of the desired path in the global paths variable
    '''
    mazeviz = maze.copy()    
    ## reset maze
    for row in range(len(mazeviz)):
        for cell in range(len(mazeviz[row])):
            if mazeviz[row][cell] == 4:
                mazeviz[row][cell] = 0
            if mazeviz[row][cell] == 5:
                mazeviz[row][cell] = 1

    ## print current path
    for row in range(len(mazeviz)):
        for cell in range(len(mazeviz[row])):
            if mazeviz[row][cell] == 0:
                if paths[path_key]:
                    if (row,cell) in paths[path_key]:
                        mazeviz[row][cell] = 4
            if mazeviz[row][cell] == 1:
                if paths[path_key] and (row,cell) in paths[path_key]:
                    mazeviz[row][cell] = 5
    return mazeviz


### Visualizes the global paths on the maze
def viz_maze(maze,size):
    '''
    :param maze: a two-dim array containing the numbers encoding the maze
    :param size: the number of iterations to display
    '''
   
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()
    img = ax.imshow(numeric_maze(maze))

    
    axcolor = 'yellow'
    ax_slider = plt.axes([0.20, 0.01, 0.65, 0.03], facecolor=axcolor)
    slider = Slider(ax_slider, 'Slide->', 1, size, valstep=1)

    def generate_path(val):
        mazeviz = maze_with_path(maze,val)
        ax.imshow(mazeviz)
        fig.canvas.draw_idle()
    slider.on_changed(generate_path)
    plt.show()


if __name__ == "__main__":
    main()


# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# import time

# fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)

# def animate(i):
#     pullData = open("sampleText.txt","r").read()
#     dataArray = pullData.split('\n')
#     xar = []
#     yar = []
#     for eachLine in dataArray:
#         if len(eachLine)>1:
#             x,y = eachLine.split(',')
#             xar.append(int(x))
#             yar.append(int(y))
#     ax1.clear()
#     ax1.plot(xar,yar)
# ani = animation.FuncAnimation(fig, animate, interval=1000)
# plt.show()


