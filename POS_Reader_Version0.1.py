#!/usr/bin/env python
# coding: utf-8

import struct
little_endian = (struct.unpack('<I', struct.pack('=I', 1))[0] == 1)
print("Is Little Endian set? \n" + str(little_endian))

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import struct
import random
import time
import numpy as np

filename = "file.pos"
# IMPORTANT: Choose how many rows to read. Do NOT change the value
#            for columns as it depends on the .POS file architecture
# CAREFUL:   Use int(len(f_input.read())/4) to read complete file
rows =  100000
columns = 4

# Ion data n/m will be stored in data[4] if you wish to access it, 
# though there is no Visualization implemented yet!

# Routine to plot data in a 3d scatter plot:
def plot(data):
    '''
    Creates a 3D-scatter plot using an xyz-array by [row,column]-notation
    '''
    fig = plt.figure(figsize=(4,3))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the values
    ax.scatter(data[:,0], data[:,1], data[:,2], c = 'r', marker='+')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    
    plt.tight_layout()
    plt.show()
    # If you wish to save uncomment the following line:
    fig.savefig('3D-Scatterplot.png', dpi=300)
    
# Part_size is fixed as .POS file uses 4 Bytes for floating point
# scientific number representation by IEEE 754 standard
# (CAREFUL: Big Endian is used!)
part_size = 4
start = time.time()

# Reading data from POS file
with open(filename, 'rb') as f_input:    
    data = np.empty((rows, columns), dtype=float)
    block_size = rows * part_size * columns

    while True:
        block = f_input.read(block_size)
        
        # Counter for Bytes sequence and Column / Row for
        # Data storage in numpy-2d array as table
        counter = 0
        column = 0
        row = 0
        
        # Unpacking Bytes sequence
        float_number = struct.unpack('>'+
                                     str(rows * columns)+
                                     'f'.format(part_size), 
                                     block)
                                        
        for counter in range(columns*rows):
            # Data is stored as follows:
            data[row, column] = float_number[counter]
            
            # If max(column) is reached jump into next row and start again
            if (column >= 3):
                column = 0
                row += 1
            
            # Else just go to next column to store data
            else:
                column +=1
        
        # Condition to stop IO_Buffer from reading File
        # CAREFUL: If you want to read the whole file, be sure that 
        #           your memory can handle the file size!
        if (len(block) <= block_size):
            break

# Output: Data plotting - Benchmarking
print("\nTime taken to read filechunk: {:.2f}".format(time.time() - start))

start = time.time()
# -1 to ignore n/m data:
plot(data[:,:-1])
print("\nTime taken to plot data: {:.2f}".format(time.time() - start))

print("\nDatapoints: {}".format(columns * rows))
