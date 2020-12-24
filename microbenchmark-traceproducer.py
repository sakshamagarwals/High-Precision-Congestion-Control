import sys

OUTPUT_FILE = sys.argv[1]
INPUT_LOAD = float(sys.argv[2])
SHORT_FLOW_SIZE = int(sys.argv[3])
LONG_FLOW_SIZE = int(sys.argv[4])
BW = int(sys.argv[5])
out_file = open(OUTPUT_FILE,'w')

# 2 9 3 21553 34500 1.000828

short_flow_tx_time = float(SHORT_FLOW_SIZE) * 8.0 / (float(BW) * 1e9)
long_flow_tx_time = float(LONG_FLOW_SIZE) * 8.0 / (float(BW) * 1e9)
# flows from 2 -- 5 (green)

cur_time = 1.0
line_to_write = '0 12 3 21553 ' + str(LONG_FLOW_SIZE) + ' ' + str(cur_time)
out_file.write(line_to_write + '\n')
line_to_write = '1 13 3 21553 ' + str(LONG_FLOW_SIZE) + ' ' + str(cur_time)
out_file.write(line_to_write + '\n')
cur_time = 1.0
while(cur_time < 1.0 + (long_flow_tx_time * 1.5)):
    line_to_write = '2 5 3 21553 ' + str(SHORT_FLOW_SIZE) + ' ' + str(cur_time)
    cur_time = cur_time + (short_flow_tx_time / INPUT_LOAD)
    out_file.write(line_to_write + '\n')

# flows from 3 -- 9 (pink)
cur_time = 1.0
while(cur_time < 1.0 + (long_flow_tx_time * 1.5)):
    line_to_write = '3 9 3 21553 ' + str(SHORT_FLOW_SIZE) + ' ' + str(cur_time)
    cur_time = cur_time + (short_flow_tx_time / INPUT_LOAD)
    out_file.write(line_to_write + '\n')


# flows from 6 -- 12 (blue)
cur_time = 1.0
while(cur_time < 1.0 + (long_flow_tx_time * 1.5)):
    line_to_write = '6 12 3 21553 ' + str(SHORT_FLOW_SIZE) + ' ' + str(cur_time)
    cur_time = cur_time + (short_flow_tx_time / INPUT_LOAD)
    out_file.write(line_to_write + '\n')


# flows from 11 -- 13 (brown)
cur_time = 1.0
while(cur_time < 1.0 + (long_flow_tx_time * 1.5)):
    line_to_write = '11 13 3 21553 ' + str(SHORT_FLOW_SIZE) + ' ' + str(cur_time)
    cur_time = cur_time + (short_flow_tx_time / INPUT_LOAD)
    out_file.write(line_to_write + '\n')