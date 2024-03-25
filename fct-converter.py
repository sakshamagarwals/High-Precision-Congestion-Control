import sys

INPUT_FILE = sys.argv[1]
# OUTPUT_FILE = sys.argv[2]
# outfile = open(OUTPUT_FILE,'w')

pktsize = 1500
link_bandwidth = int(sys.argv[2])
NUM_HOSTS_PER_AGG = 16
propagation_delay_in_ns = 200

def ipToNode(ip):
    return (int(ip, 16)-int('0b000001', 16))/int('00000100', 16)

def idealTime(pktsize, link_bandwidth, NUM_HOSTS_PER_AGG, propagation_delay_in_ns, flowsize, src, dst):
    if(src/NUM_HOSTS_PER_AGG == dst/NUM_HOSTS_PER_AGG):
        ideal_data_time = ((flowsize*8.0)/link_bandwidth)/1e3 + 1*(((pktsize*8.0)/link_bandwidth)/1e3) + (2 * propagation_delay_in_ns * 1e-3)
        ideal_header_time = 2.0 * (8.0 * 40 / link_bandwidth)/1e3 + (2 * propagation_delay_in_ns * 1e-3)
    else:
        ideal_data_time = ((flowsize*8.0)/link_bandwidth)/1e3 + 1*(((pktsize*8.0)/link_bandwidth)/1e3) + 2*(((pktsize*8.0)/(4*link_bandwidth))/1e3) + (4 * propagation_delay_in_ns * 1e-3)
        ideal_header_time = 2.0 * (8.0 * 40 / link_bandwidth)/1e3 + 2.0 * (8.0 * 40 / (4 * link_bandwidth))/1e3  + (4 * propagation_delay_in_ns * 1e-3)

    ideal_fct = ideal_header_time + ideal_data_time
    # print("\theader: " + str(ideal_header_time*1e3) + "ns, data: " + str(ideal_data_time*1e3)) + "ns"
    return ideal_fct

xput_all = []
with open(INPUT_FILE) as f1:
    for line in f1:
        line_str = line.split()
        src = ipToNode(line_str[0])
        dst = ipToNode(line_str[1])
        flowsize = int(line_str[4])
        fct = float(line_str[6])/1e3
        ideal_fct = idealTime(pktsize, link_bandwidth, NUM_HOSTS_PER_AGG, propagation_delay_in_ns, flowsize, src, dst)
        
        xput = (flowsize*8.0) / fct / 1e3
        xput_all.append(xput)
        ideal_xput = (flowsize*8.0) / ideal_fct / 1e3
        
        new_line = "sender: " + str(src) + ', receiver: ' + str(dst) + ', start time(s): ' + str(float(line_str[5])/1e9) + ', flowsize: ' + str(flowsize) + ' fct: ' + str(fct*1e3) + 'ns, ideal fct: ' + str(ideal_fct*1e3) + "ns, actual/ideal: " + str(fct/ideal_fct) + " xput: " + str(xput) + " ideal xput: " + str(ideal_xput)
        print(new_line)
        # outfile.write(new_line + '\n')
print("avg xput: " + str(sum(xput_all)/len(xput_all)))