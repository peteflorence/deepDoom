__author__ = 'tj_florence'

import sys
import struct
import binascii
import numpy as np


def read_lmp_file(fname):
    # open lmp file
    f = open(fname, 'rb')

    # all of our lmps were recorded with a doomv1.9 engine;
    # header file will be 13 bytes, so read it out
    rawdata = f.read(13)
    data = binascii.hexlify(rawdata)

    header = data
    gp = int(header[19:20], 16)
    ip = int(header[21:22], 16)
    bp = int(header[23:24], 16)
    rp = int(header[25:26], 16)

    num_players = gp+ip+bp+rp
    print(num_players)

    p0_data = np.zeros((1, 5), dtype=np.int)
    p1_data = np.zeros((1, 5), dtype=np.int)

    frame_num = 0

    # read in first line - (player 0)
    data = f.read(4)
    data = binascii.hexlify(data)


    while data:

    # format of lmp input lines:
    # [go][strafe][turn][use]
    # go, strafe, turn are int16, -127-127
    # use is byte, with bits [SA [weapon id 6-3] WpnChange UB FB]
    # file ends with stop byte = 128, so break when we get there

    # we want to write to 2 numpy arrays (1/player) of dim nxm
    # where n = num ticks
    # m = [go strafe turn ub fp] = 5


        go = int(data[0:2], 16)

        # go = 128 is stop byte
        if go == 128:
            print('file done')
            break

        strafe = int(data[3:4], 16)
        turn = int(data[5:6], 16)

        usebyte = data[7:8]

        usebits = bin(int(usebyte, 16))[2:].zfill(8)

        FB = usebits[-1]
        UB = usebits[-2]

        ext_data_array = np.array([go, strafe, turn, FB, UB], dtype=np.int)

        if frame_num == 0:
            p0_data([:])


        frame_num += 1
        data = f.read(4)
        data = binascii.hexlify(data)
