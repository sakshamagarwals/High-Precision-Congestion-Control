import sys
import numpy as np

NUM_HOSTS = int(sys.argv[1])
INCAST_DEGREE = int(sys.argv[2])
INCAST_LOAD = float(sys.argv[3])
INPUT_BANDWIDTH = int(sys.argv[4])
RPC_SIZE = int(sys.argv[5])
INPUT_FILE  = sys.argv[6]
input_file = open(INPUT_FILE,'w')

RPC_TRANSMISSION_TIME_US = float(RPC_SIZE) * 1000.0 * 8.0 / (float(INPUT_BANDWIDTH) * 1e9) * 1e6
print(RPC_TRANSMISSION_TIME_US)
T = RPC_TRANSMISSION_TIME_US / INCAST_LOAD
print(T)

NUM_INCAST = int(10000.0/T)
print(NUM_INCAST)
if(NUM_INCAST == 0):
    NUM_INCAST+= 1
input_file.write(str(15 + (INCAST_DEGREE*NUM_INCAST)) + '\n')
#Create 15 permutation flows (128 - 142) of size 1000 packets
# for i in range(15):
#     line_to_write = str(i) + ' ' + str(128 + i) + ' ' + '3'  + ' ' + '21553' + ' ' + '1500000' + ' ' + '1.0'
#     input_file.write(line_to_write + '\n')

#create 40-1 incast  with randomly chosen 40  srcs (but not with the permutation srcs), dst 143, every T microseconds, until 300 microseconds, ideally
possible_srcs = set(range(144))
assert(INCAST_DEGREE <= len(possible_srcs))
incast_time = 1.0
for j in range(500):
    for i in range(NUM_INCAST):
        incast_dest = 16*(j%9) + (j%16)
        possible_srcs.remove(incast_dest)
        incast_srcs = list(np.random.choice(list(possible_srcs), INCAST_DEGREE, replace=False))
        possible_srcs.add(incast_dest)
        for src in incast_srcs:
            line_to_write = str(src) + ' ' + str(incast_dest) + ' ' + '3' + ' ' + '21553' + ' ' + str(RPC_SIZE * 1000) + ' ' + str(incast_time)
            input_file.write(line_to_write + '\n')
        incast_time += T*1e-6