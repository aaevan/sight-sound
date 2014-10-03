import numpy as np
from math import sqrt

MIN_VAL_PAN = -2
MAX_VAL_PAN = 2
NUM_V_CHANNELS = 12
ORIGIN = (0, 0)
LEFT_EAR = (-1, 0)
RIGHT_EAR = (1, 0)
CIRC_DIAMETER = 2

def circ(x, diameter = 1):
    return abs(sqrt(diameter**2 - x**2))

def init_x_coords():
    return np.linspace(MIN_VAL_PAN, MAX_VAL_PAN, NUM_V_CHANNELS)

def init_y_coords():
    return [circ(y, CIRC_DIAMETER) for y in init_x_coords()]

def init_ear_dists():
    """
    initializes the distance tables for each ear.
    """
    x_coords = init_x_coords()
    y_coords = init_y_coords()
    print("x_coords:", x_coords)
    print("y_coords:", y_coords)
    left_dists = []
    right_dists = []
    for i in range(len(x_coords)):
        left_dists.append(euclid_2d_dist(*LEFT_EAR + (x_coords[i], y_coords[i])))
    for j in range(len(x_coords)):
        right_dists.append(euclid_2d_dist(*RIGHT_EAR + (x_coords[j], y_coords[j])))
    return left_dists, right_dists

def inverse_square_law(lin_distance):
    """
    returns a scaling factor based on the inverse of the square of the distance.
    """
    return (1/(lin_distance**2))
    pass

def map_intensities_to_dists(dist_list):
    """
    apply the inverse square law to each item in a list
    """
    return [inverse_square_law(i) for i in dist_list]
    pass

def map_intensities_to_ear_lists():
    left, right = init_ear_dists()
    return map_intensities_to_dists(left), map_intensities_to_dists(right)
    

def euclid_2d_dist(x1, y1, x2, y2):
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

def main():
    left_intensities, right_intensities = map_intensities_to_ear_lists()
    print(left_intensities)
    print(right_intensities)

if __name__ == '__main__':
    main()
