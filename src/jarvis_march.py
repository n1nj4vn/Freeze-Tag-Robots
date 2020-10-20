"""
file: jarvis_march.py
description:
    Algorithm for evaluating and visualizing modified jarvis_march algorithms for the freeze tag robots problem!
    This application assumes collinear points can lie on the convex hull.
language: python3.8
author: jxt5551@rit.edu
"""


def orientation(point_one, point_two, point_three):
    """
        Orientation test to find next vertex on the hull in counter-clockwise order
        Eliminates need to compute angles!
    """
    a = point_two[1] - point_one[1]
    b = point_three[0] - point_two[0]
    c = point_two[0] - point_one[0]
    d = point_three[1] - point_two[1]
    return a * b - c * d


class JarvisMarch(object):
    """
        Class holding operations required to perform Jarvis March convex hull search
    """
    def __init__(self, point_list):
        self.point_list = point_list

    def run_jarvis_march_convex_hull(self):
        """
            Run the Jarvis March algorithm on a list of points; point represented as a tuple(x, y)
        """
        hull = list()   # Track point indexes
        hull_points = list()    # Track point(x, y) on hull
        point_one = 0   # Input list is sorted leftmost point first, so index 0 is guaranteed to be on the hull

        while True:
            if point_one not in hull:
                hull.append(point_one)  # Save first / current point
                hull_points.append(self.point_list[point_one])

            point_two = (point_one + 1) % len(self.point_list)  # Index of next point

            for current_point in range(len(self.point_list)):
                if orientation(self.point_list[point_one], self.point_list[current_point], self.point_list[point_two]) < 0:
                    point_two = current_point

            point_one = point_two   # Set next point in hull

            if point_one == 0:  # Break once we return to the first point
                break

        return hull_points
