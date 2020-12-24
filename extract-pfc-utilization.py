import sys

L_B = float(sys.argv[1])
T_I = 500
INCAST_DEGREE = 60
L_I = float(sys.argv[2])

FLOW_FILE = sys.argv[3]
FCT_FILE = sys.argv[4]

#calculate the end time
# (L_B + INCAST_DEGREE * L_I)*T_I + (L_B)*T_B = (T_I + T_B)
# T_I*(L_B + INCAST_DEGREE * L_I - 1) = T_B*(1 - L_B)
T_B = (L_B + INCAST_DEGREE * L_I - 1) * T_I / (1 - L_B)
print("T_B: ",T_B)

T_END = 1e9 + (T_B + T_I)*1e3
print("T_END: ",T_END)

bytes_sent = [0 for i in range(15)]
bytes_received = [0 for i in range(15)]
utils = [0.0 for i in range(15)]
#calculate the number of packets needed to be sent to each receiver
ctr = 0
with open(FLOW_FILE) as f1:
    f1.readline()
    for line in f1:
        line_str = line.split()
        if(len(line_str) >= 6):
            sender = int(line_str[0])
            receiver = int(line_str[1])
            bytes_flow = int(line_str[4])
            arrival_time = float(line_str[5])
            if(arrival_time*1e9 < T_END):
                if(receiver >= 128 and receiver < 143):
                    ctr+=1
                    bytes_sent[receiver - 128] += bytes_flow

print(ctr)
#calculate the number of packets received at each receiver
def node_to_id(ip):
    return (int(ip, 16)-int('0b000001', 16))/int('00000100', 16)

prev_time = 0
with open(FCT_FILE) as f1:
    for line in f1:
        line_str = line.split()
        if(len(line_str) >= 7):
            sender = node_to_id(line_str[0])
            receiver = node_to_id(line_str[1])
            bytes_flow_rx = int(line_str[4])
            arrival_time = float(line_str[5])
            finish_time = float(line_str[6])
            cur_time = arrival_time + finish_time
            assert(cur_time >= prev_time)
            prev_time = cur_time
            if(arrival_time + finish_time < (T_END+6.7e-6)):
                if(receiver >= 128 and receiver < 143):
                    bytes_received[receiver - 128] += bytes_flow_rx

for i in range(15):
    utils[i] = float(bytes_received[i])/float(bytes_sent[i])

# print("sent: ",bytes_sent)
# print("recvd: ",bytes_received)
print("utils: ",utils)
print("Avg util: ",sum(utils)/len(utils))



