import sys
import math

INPUT_FILE = sys.argv[1]
# OUTPUT_FILE = sys.argv[2]
# outfile = open(OUTPUT_FILE,'w')

pktsize = 1500
link_bandwidth = int(sys.argv[2])
propagation_delay_in_ns = int(sys.argv[3])
NUM_HOSTS_PER_AGG = 16
payload_size = 1000
header_size = 48
flow_size = header_size + payload_size


host_start_id = int(sys.argv[4])
num_hosts_per_tor_switch = int(sys.argv[5])

def ipToNode(ip):
    return (int(ip, 16)-int('0b000001', 16))/int('00000100', 16)

# def idealTime(pktsize, link_bandwidth, NUM_HOSTS_PER_AGG, propagation_delay_in_ns, flowsize, src, dst):
#     # if(src/NUM_HOSTS_PER_AGG == dst/NUM_HOSTS_PER_AGG):
#     if (src-host_start_id) // num_hosts_per_tor_switch == (dst-host_start_id) // num_hosts_per_tor_switch:
#         assert(False)
#         ideal_data_time = ((flowsize*8.0)/link_bandwidth)/1e3 + 1*(((pktsize*8.0)/link_bandwidth)/1e3) + (2 * propagation_delay_in_ns * 1e-3)
#         ideal_header_time = 2.0 * (8.0 * 40 / link_bandwidth)/1e3 + (2 * propagation_delay_in_ns * 1e-3)
#     else:
#         ideal_data_time = ((flowsize*8.0)/link_bandwidth)/1e3 + 1*(((pktsize*8.0)/link_bandwidth)/1e3) + 2*(((pktsize*8.0)/(4*link_bandwidth))/1e3) + (4 * propagation_delay_in_ns * 1e-3)
#         ideal_header_time = 2.0 * (8.0 * 40 / link_bandwidth)/1e3 + 2.0 * (8.0 * 40 / (4 * link_bandwidth))/1e3  + (4 * propagation_delay_in_ns * 1e-3)

#     ideal_fct = ideal_header_time + ideal_data_time
#     # print("\theader: " + str(ideal_header_time*1e3) + "ns, data: " + str(ideal_data_time*1e3)) + "ns"
#     return ideal_fct

def idealTime(link_bandwidth, NUM_HOSTS_PER_AGG, flowsize, src, dst): # res in ns
    # if(src/NUM_HOSTS_PER_AGG == dst/NUM_HOSTS_PER_AGG):
    if (src-host_start_id) // num_hosts_per_tor_switch == (dst-host_start_id) // num_hosts_per_tor_switch:
        num_hops = 2
        assert(False)
    else:
        num_hops = 4
        
    num_packets = math.ceil(float(flowsize) / float(payload_size))
    assert(num_packets >= 1)
    packet_size = payload_size + header_size
    packet_transmission_delay = int(float(packet_size)*8/link_bandwidth)
    header_transmission_delay = int(float(header_size)*8/link_bandwidth) # ack packet only has header
    res = (propagation_delay_in_ns + packet_transmission_delay) * num_hops + (num_packets-1) * packet_transmission_delay + (propagation_delay_in_ns + header_transmission_delay) * num_hops
    res = round(res)
    # print(f"fct: {res} propagation_delay_in_ns: {propagation_delay_in_ns} packet_transmission_delay: {packet_transmission_delay} header_transmission_delay: {header_transmission_delay} num_packets: {num_packets}")
    return res

xput_dict = {}
with open(INPUT_FILE) as f1:
    for line in f1:
        line_str = line.split()
        # src = ipToNode(line_str[0])
        # dst = ipToNode(line_str[1])
        src = int(line_str[0])
        dst = int(line_str[1])
        flowsize = int(line_str[4])
        fct = int(line_str[6])
        ideal_fct = idealTime(link_bandwidth, NUM_HOSTS_PER_AGG, flowsize, src, dst)
        
        xput = float(flowsize*8.0) / float(fct)  
        ideal_xput = float(flowsize*8.0) / float(ideal_fct)
        
        ratio = float(ideal_fct)/float(fct)
        new_line = f"src: {src}, dst: {dst} start: {float(line_str[5])/1e9}, flow_size: {flow_size}, fct: {fct} ({ideal_fct}), xput: {round(xput, 2)} ({round(ideal_xput,2)}), ratio: {round(ratio, 2)}"
        print(new_line)
        
        if src not in xput_dict:
            xput_dict[src] = {}
        if dst not in xput_dict[src]:
            xput_dict[src][dst] = []
        xput_dict[src][dst].append([xput, ideal_xput, ratio])
        
        # outfile.write(new_line + '\n')
        
for src in xput_dict:
    print(f"src: {src}")
    for dst in xput_dict[src]:
        pair_xput = [f[0] for f in xput_dict[src][dst]]
        pair_ideal_xput = [f[1] for f in xput_dict[src][dst]]
        pair_ratio = [f[2] for f in xput_dict[src][dst]]
        print(f"\tdst: {dst} xput: {round(sum(pair_xput),2)} ideal_xput: {round(pair_ideal_xput[0],2)} pair_ratio: {round(sum(pair_ratio)*100)}%")