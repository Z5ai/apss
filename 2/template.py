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



def find_neighbor:

def eval(path):
    # for each step -1 as penalty, for each wall -10 as penalty

def g(T,t):



def sim_annealing_search(maze, starting_node, goal_node):
    '''
    :param maze: a two-dim array containing the characters as in the maze file.
    :param heuristic: a function that takes two corrdinate pairs an returns an approx. distance
    :return: shortest path found ...list of coord. pairs
    '''

    T = 100
    find_initial_solution(maze, starting_node, goal_node, 0)

    # contrary to slide 44 leave green iteration out, which is just for, if you want not to decrease T in each iteration
    for t in range(1, 30):
        path_c = paths[t-1]

        while no better neighbour is found, do..., so that we get a improved soltuion for every t.
            path_n = get_neighbor(path_c)
            if eval(path_c) < eval(path_n):
                paths[t] = path_n
            .......
        T = g(T,t)




    viz_maze(maze,30)
    
    
def main():
    # Start from your command line:
    # C:/ProgramData/Anaconda3/python.exe "c:/Users/marcr/Desktop/Master 1/APSS/Exercises/Exercise 1/astar-maze-template.py" hard.maze
    parser = ap.ArgumentParser(description="A Maze Solver based on AStar.")
    parser.add_argument("mazefile", type=str, help="filename of the the maze file to load")
    args = parser.parse_args(args=["medium.maze"])

    # 1. load the maze
    maze, starting_node, goal_node = load_maze_file(args.mazefile)

    print(len(maze), len(maze[0]))
    
    maze = numeric_maze(maze)

    # 2. call simulated annealing
    sim_annealing_search(maze, starting_node, goal_node)


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


