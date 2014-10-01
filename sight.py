# merged socketthing2 and opencvcamtest.py

import socket
#from random import randint
from random import random
from time import sleep
import cv2
import numpy
from numpy import zeros
from itertools import product

V_DIVS = 12
HOST = '127.0.0.1'
PORT = 1119

def get_2d_list_slice(matrix, start_row, end_row, start_col, end_col):
    return [row[start_col:end_col] for row in matrix[start_row:end_row]]



#a_list = [40, 40, 45, 45]
#b_list = [50, 53, 53, 45, 45]
#c_list = [47, 47, 27, 27, 25, 25, 27]
#d_list = [45, 47, 36, 27, 66, 25, 25, 25]

def random_list(length):
    return [[round(random()) for i in range(length)] for i in range(length)]

def init_channel_vals(v_divs, DEBUG = 0): 
    left_channel_vals = [round((1.0/v_divs)*i, 3) for i in range(1, v_divs+1)]
    right_channel_vals = [round((1.0/v_divs)*i, 3) for i in range(1, v_divs+1)][::-1]
    if DEBUG:
        print left_channel_vals
        print len(left_channel_vals)
        print right_channel_vals
        print len(right_channel_vals)
    return left_channel_vals, right_channel_vals

def v_bar_index_list_init(v_divs):
    v_bar_index_list = [0] + [i for i in range(0, v_divs)] + [i for i in range(v_divs)][::-1]
    return v_bar_index_list


def main():
    # Sockets init:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    # OpenCV init:
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)

    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False
    height = len(frame)
    width = len(frame[0])

    #frame slicing init:
    hdivs = 12
    vdivs = 12
    windows_horiz = [width/hdivs*i for i in range(hdivs+1)]
    horiz_tuples = [(j, windows_horiz[i+1]) for i, j in enumerate(windows_horiz[:-1])]

    #vertical window init
    windows_vert = [height/vdivs*i for i in range(vdivs+1)]
    vert_tuples = [(j, windows_vert[i+1]) for i, j in enumerate(windows_vert[:-1])]
    hv_tuple_products = [i for i in product(vert_tuples, horiz_tuples)]

    #Puredata and sound channels init
    left_channel_vals, right_channel_vals = init_channel_vals(V_DIVS)
    vertical_bar_num = 0
    v_bar_index_list = v_bar_index_list_init(V_DIVS)
    randlist = random_list(V_DIVS) 

    while(rval):
        #opencv get frame/keygrabbing:
        cv2.imshow("preview", frame)
        rval, frame = vc.read()
        key = cv2.waitKey(5)
        if key == 27:
            break
        #clearing out/initializing old values:
        val_grid = zeros((12, 12))
        y = 0
        x = 0
        for tuple_pair in hv_tuple_products:
            start_row, end_row = tuple_pair[0]
            start_col, end_col = tuple_pair[1]
            list_slice_2d = get_2d_list_slice(frame, start_row, end_row, start_col, end_col)
            val_grid[y][x] = int(numpy.asarray(list_slice_2d).mean()) * 10 / 255
            x += 1
            if x % hdivs == 0:
                x = 0
                y += 1
                if y >= vdivs:
                    break
        print val_grid
        #begin Puredata connection code:
        print "******************************************"
        tsr = ''
        for index, val in enumerate(val_grid[v_bar_index_list[vertical_bar_num]]):
            tsr += ('a' + str(index) + ' ' + str(val) + '; ')
        tsr += ('lcv ' + str(left_channel_vals[v_bar_index_list[vertical_bar_num]]) + '; ')
        tsr += ('rcv ' + str(right_channel_vals[v_bar_index_list[vertical_bar_num]]) + '; ')
        tsr += ('nc ' + str(6) + '; ')
        s.send(tsr.encode())
        print tsr
        print "vertical_bar_num: ", vertical_bar_num
        print "v_bar_index_list[vertical_bar_num]: ", v_bar_index_list[vertical_bar_num]
        sleep(.05)
        vertical_bar_num += 1
        if vertical_bar_num >= len(v_bar_index_list)-1:
            vertical_bar_num = 0

        #vertical_bar_num %= V_DIVS
    #kill Sockets and Opencv
    cv2.destroyWindow("preview")
    s.shutdown(0)
    s.close()

if __name__ == '__main__':
    main()
