import sys

NUM_NODES = int(sys.argv[1])
assert(NUM_NODES%144 == 0)
OUTPUT_FILE = sys.argv[2]
outfile = open(OUTPUT_FILE,'w')
ACCESS_LINK_BW = int(sys.argv[3])
PROP_DELAY = int(sys.argv[4])

NUM_AGG = 9
NUM_NODES_PER_AGG = NUM_NODES / NUM_AGG
NUM_CORE = NUM_NODES_PER_AGG
NUM_LINKS = (NUM_AGG * NUM_NODES_PER_AGG) + (NUM_AGG * NUM_CORE)
NUM_SWITCHES = NUM_AGG + NUM_CORE

LINE1 = str(NUM_NODES + NUM_AGG + NUM_CORE) + ' ' + str(NUM_AGG + NUM_CORE) + ' ' + str(NUM_LINKS)
outfile.write(LINE1 + '\n')
LINE2 = ''
for i in range(NUM_SWITCHES):
    LINE2 += str(NUM_NODES + i) + ' '
outfile.write(LINE2 + '\n')
#agg-core links
for i in range(NUM_AGG):
    for j in range(NUM_CORE):
        LINE = str(NUM_NODES + i) + ' ' + str(NUM_NODES + NUM_AGG + j) + ' ' + str(ACCESS_LINK_BW) + 'Gbps' + ' ' + str(PROP_DELAY) + 'ns' + ' ' + str(0)
        outfile.write(LINE + '\n')

#endhost-agg links
for i in range(NUM_AGG):
    for j in range(NUM_NODES_PER_AGG):
        LINE = str(i*NUM_NODES_PER_AGG + j) + ' ' + str(NUM_NODES + i) + ' ' + str(ACCESS_LINK_BW) + 'Gbps' + ' ' + str(PROP_DELAY) + 'ns' + ' ' + str(0)
        outfile.write(LINE + '\n')