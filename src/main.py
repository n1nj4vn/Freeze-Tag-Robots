"""
file: main.py
description:
    Application for evaluating and visualizing different algorithms for the freeze tag robots problem!
    This application assumes collinear points can lie on the convex hull.
language: python3.8
author: jxt5551@rit.edu, bxm8164@rit.edu, bcm7897@rit.edu
"""


import getopt
import random as r
import sys
import datetime
import matplotlib.pyplot as plt
import math
import copy
from sklearn.cluster import KMeans
import numpy as np

from jarvis_march import JarvisMarch
from visualizer import plotInitial
from visualizer import plotPoints

test_input_sizes = [10, 100, 1000, 10000, 100000, 1000000, 10000000]


def construct_point_list(input_file):
    """
        Iterate through the input list and construct a list of tuples representing points
    """
    points = list()
    file = open(input_file, "r")
    for line in file.readlines()[1:]:
        split_line = line.split()
        point = (int(split_line[0]), int(split_line[1]))
        points.append(point)
    return points


def randomly_generate_points(size):
    """
        Randomly generate points and save to a file to be inputted to the program
    """
    filename = "input_test_" + str(size) + ".txt"
    file = open(filename, "w")
    file.write(str(size) + "\n")
    for x in range(size):
        point_one = r.randint(-size, size)
        point_two = r.randint(-size, size)
        file.write(str(point_one) + " " + str(point_two) + "\n")
    file.close()


def sort_points_list(points_list):
    """
        Sort the points leftmost point first then by angle of slope to the leftmost point
    """
    def rise_run(point_two):
        point_one = points_list[0]
        y = point_one[1] - point_two[1]
        x = point_one[0] - point_two[0]
        if x == 0:
            return 0
        return y / x

    points_list.sort()  # Leftmost first
    points_list = points_list[:1] + sorted(points_list[1:], key=rise_run)   # Next by angle of slope to leftmost point
    return points_list


def main(argv):
    """
        Driver method
    """
    input_file = ""
    output_file_jm = ""
    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        print("main.py -i <input_file>")
        sys.exit(0)

    for opt, arg in opts:
        if opt == "-h":
            print("main.py -i <input_file>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
            output_file_jm = input_file.split(".")[0] + "_jarvis_results.txt"

    if input_file == "":
        print("main.py -i <input_file>")
        sys.exit(0)
    else:
        print("Input file is " + input_file)

        # Uncomment the following lines to generate new test files!
        # for x in test_input_sizes:
        #     randomly_generate_points(x)

        print("Points from Input File:")
        point_list = construct_point_list(input_file)
        print(point_list)

        # uncomment this line for evaluation
        # evaluatejarvismarch(point_list, output_file_jm)
        # evaluatebruteforce(copy.deepcopy(point_list))
        # visualizejarvismarchsequential(point_list)
        # visualizejarvismarchparallel(point_list)
        # evaluatejarvismarchparallel(copy.deepcopy(point_list))
        # evaluatejarvismarchsequential(copy.deepcopy(point_list))
        evaluatekmeansclustering(copy.deepcopy(point_list))

def evaluatebruteforce(point_list):
    totaldist = 0
    previouspoint = [0 , 0]
    for p in point_list:
        totaldist += math.sqrt(((previouspoint[0]-p[0])**2)+((previouspoint[1]-p[1])**2))
        previouspoint = p
    print("Total distance traveled Brute Force: " + str(totaldist))

def evaluatekmeansclustering(point_list):
    kmeans = KMeans(n_clusters=4, random_state=0).fit(point_list)
    print("hi")

def evaluatejarvismarchsequential(point_list):
    subhullflat = []
    totaldist = 0
    while (len(point_list) > 6):
        sorted_points = sort_points_list(point_list)
        jm = JarvisMarch(sorted_points)
        jm_point_list = jm.run_jarvis_march_convex_hull()
        for p in jm_point_list:
            point_list.remove(p)
            subhullflat.append(p)
    for p in point_list:
        subhullflat.append(p)
    for i in range(len(subhullflat) - 1):
        totaldist += math.sqrt(((subhullflat[i][0] - subhullflat[i + 1][0]) ** 2) + ((subhullflat[i][1] - subhullflat[i + 1][1]) ** 2))
    print("Total distance traveled Jarvis March Sequential: " + str(totaldist))

def evaluatejarvismarchparallel(point_list):
    availablerobots = [(0, 0)]
    subhulls = []
    activeSubHulls = []
    subhulldist = []
    totaldist = 0
    while (len(point_list) > 6):
        sorted_points = sort_points_list(point_list)
        jm = JarvisMarch(sorted_points)
        jm_point_list = jm.run_jarvis_march_convex_hull()
        subhulls.append(jm_point_list)
        for p in jm_point_list:
            point_list.remove(p)
    subhulls.append(point_list)
    subhullcopy = copy.deepcopy(subhulls)
    while len(subhulls) != len(subhulldist):
        for hull in activeSubHulls:
            if len(hull) == 0:
                activeSubHulls.remove(hull)
                continue
            availablerobots.append(hull[0])
            hull.remove(hull[0])
        for robot in availablerobots:
            if len(subhullcopy) > 0:
                tmp = copy.deepcopy(subhullcopy[0])
                tmp.insert(0, robot)
                subhulldist.append(tmp)
                activeSubHulls.append(subhullcopy[0])
                subhullcopy.remove(subhullcopy[0])
                availablerobots.remove(robot)
            else:
                break
    for hull in subhulldist:
        for i in range(len(hull) - 1):
            totaldist += math.sqrt(((hull[i][0] - hull[i + 1][0]) ** 2) + ((hull[i][1] - hull[i + 1][1]) ** 2))
    print("Total distance traveled Jarvis March Parallel: " + str(totaldist))

def visualizejarvismarchparallel(point_list):
    subhulls = []
    plotInitial(point_list)
    while (len(point_list) > 6):
        sorted_points = sort_points_list(point_list)
        jm = JarvisMarch(sorted_points)
        jm_point_list = jm.run_jarvis_march_convex_hull()
        subhulls.append(jm_point_list)
        for p in jm_point_list:
            point_list.remove(p)
    subhulls.append(point_list)
    activeSubHulls = []
    while len(subhulls) > 0 or len(activeSubHulls) > 0:
        plotTimeStep = []
        if len(subhulls) > 0:
            activeSubHulls.append(subhulls[0])
            subhulls.remove(subhulls[0])
        for subhull in activeSubHulls:
            if len(subhull) == 0:
                activeSubHulls.remove(subhull)
                continue
            plotTimeStep.append(subhull[0])
            subhull.remove(subhull[0])
        plotPoints(plotTimeStep)
        plt.pause(0.5)
    plt.show()

def visualizejarvismarchsequential(point_list):
    plotInitial(point_list)
    # KMEans cluster with running subhull algorithm on clusters
    #evaluate all subhulls, make list of the subhulls, in each iteration of the loop create new robot, decremetn from each subhull based on number of available agents

    while(len(point_list) > 6):
        sorted_points = sort_points_list(point_list)
        jm = JarvisMarch(sorted_points)
        jm_point_list = jm.run_jarvis_march_convex_hull()
        plotPoints(jm_point_list)
        for p in jm_point_list:
            point_list.remove(p)


    plotPoints(point_list)

def evaluatejarvismarch(point_list, output_file_jm):
    print("Running Jarvis March Convex Hull")
    # Sort points and find point guaranteed to be on hull (leftmost point)
    start_time = datetime.datetime.now()

    sorted_points = sort_points_list(point_list)
    jm = JarvisMarch(sorted_points)
    jm_point_list = jm.run_jarvis_march_convex_hull()

    end_time = datetime.datetime.now()
    delta = end_time - start_time
    milliseconds = int(delta.total_seconds() * 1000)
    print("Time elapsed (ms): " + str(milliseconds))

    print("Jarvis March Results (saved to " + output_file_jm + ")")
    print(jm_point_list)
    output_jm = open(output_file_jm, "w")
    output_jm.write(str(len(jm_point_list)) + "\n")
    for point in jm_point_list:
        output_jm.write(str(point[0]) + " " + str(point[1]) + "\n")


if __name__ == "__main__":
    main(sys.argv[1:])
