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

from jarvis_march import JarvisMarch

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
