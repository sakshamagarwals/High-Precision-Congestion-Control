import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import math
import sys

EXP = sys.argv[1]
CC = sys.argv[2]
pktsize = 1500
propagation_delay_in_ns = int(sys.argv[4])
link_bandwidth = int(sys.argv[3]) #in Gbps
ov = int(sys.argv[6])
# NUM_FLOWS = int(sys.argv[4])
FILE_NAME = 'experiments/' + EXP + '/' + CC + '/' + 'fct.txt'
slowdownfile = 'experiments/' + EXP + '/' + CC + '/' + 'slowdown.txt'
throughputfile = 'experiments/' + EXP + '/' + CC + '/' + 'throughput.txt'
plotfile = 'experiments/' + EXP + '/' + CC + '/' + 'octbins.eps'
plotfile_png = 'experiments/' + EXP + '/' + CC + '/' + 'octbins.png'
octbinsfile = 'experiments/' + EXP + '/' + CC + '/' + 'octbins.txt'
flowsizebinsfile = 'experiments/' + EXP + '/' + CC + '/' + 'flowsizebins_avg.txt'
flowsizebinsfile_99 = 'experiments/' + EXP + '/' + CC + '/' + 'flowsizebins_99.txt'
plotfile_flowsizes = 'experiments/' + EXP + '/' + CC + '/' + 'flowsizebins.eps'
plotfile_flowsizes_png = 'experiments/' + EXP + '/' + CC + '/' + 'flowsizebins.png'

NUM_HOSTS = int(sys.argv[5])
NUM_AGG = 9
NUM_HOSTS_PER_AGG = NUM_HOSTS / NUM_AGG
slowdowns = []
octs = []
flow_sizes = []
tputs = []
inloads = []
total_data_hosts = [0.0 for i in range(NUM_HOSTS)]
min_start_time_hosts = [1000000.00 for i in range(NUM_HOSTS)]
max_finish_times_hosts = [-1.0 for i in range(NUM_HOSTS)]
max_start_times_hosts = [-1.0 for i in range(NUM_HOSTS)]

def ipToNode(ip):
    return (int(ip, 16)-int('0b000001', 16))/int('00000100', 16)

print(FILE_NAME)
ctr = 0
with open(FILE_NAME) as f1:
    for line in f1:
        line_str = line.split()
        src_ip = line_str[0]
        dst_ip = line_str[1]
        src = ipToNode(src_ip)
        dst = ipToNode(dst_ip)
        flowsize = int(line_str[4])
        flow_sizes.append(flowsize)
        arrival_time = int(line_str[5])/1e9 #in sec
        fct = float(line_str[6])/1e3  #in us
        finish_time = arrival_time + (fct/1000000.0)
        if (fct != -1 and flowsize != 64000): #could be -1 because of the weird way in which the file logs
            max_finish_time = finish_time
            #calculate slowdown
            ctr += 1
            if(src/NUM_HOSTS_PER_AGG == dst/NUM_HOSTS_PER_AGG):
                ideal_data_time = ((flowsize*8.0)/link_bandwidth)/1e3 + 1*(((pktsize*8.0)/link_bandwidth)/1e3) + (2 * propagation_delay_in_ns * 1e-3)
                ideal_header_time = 2.0 * (8.0 * 40 / link_bandwidth)/1e3 + (2 * propagation_delay_in_ns * 1e-3)
            else:
                ideal_data_time = ((flowsize*8.0)/link_bandwidth)/1e3 + 1*(((pktsize*8.0)/link_bandwidth)/1e3) + 2*(((pktsize*8.0)/(4*link_bandwidth / ov))/1e3) + (4 * propagation_delay_in_ns * 1e-3)
                ideal_header_time = 2.0 * (8.0 * 40 / link_bandwidth)/1e3 + 2.0 * (8.0 * 40 / (4 * link_bandwidth / ov))/1e3  + (4 * propagation_delay_in_ns * 1e-3)

            ideal_fct = ideal_header_time + ideal_data_time
            slowdown = fct/ideal_fct

            if (slowdown < 1.0):
                slowdown = 1.0
                assert(False)
            slowdowns.append(slowdown)
            octs.append(ideal_fct)

            total_data_hosts[src] += flowsize
            if(arrival_time < min_start_time_hosts[src]):
                min_start_time_hosts[src] = arrival_time
            if(finish_time > max_finish_times_hosts[src]):
                max_finish_times_hosts[src] = finish_time
            if(arrival_time > max_start_times_hosts[src]):
                max_start_times_hosts[src] = arrival_time

for i in range(NUM_HOSTS):
    tputs.append( (total_data_hosts[i] * 8.0) / (link_bandwidth * 1000000000.0 * (max_finish_times_hosts[i] - min_start_time_hosts[i])) )
    # inloads.append( (total_data_hosts[i] * 8.0) / (link_bandwidth * 1000000000.0 * (max_start_times_hosts[i] - min_start_time_hosts[i])) )
print(max_finish_time)
print(ctr)
np.savetxt(slowdownfile,slowdowns)
np.savetxt(throughputfile,tputs)
# print "Avg slowdown: ", sum(slowdowns)/len(slowdowns)
# print "Avg input load: ", sum(inloads)/len(inloads)
# print "Avg util: ", (sum(tputs)/len(tputs))/(sum(inloads)/len(inloads))
print "Avg tput: ", (sum(tputs)/len(tputs))

INPUT_FILE = slowdownfile
# OUTPUT_FILE = INPUT_FILE + '.result'

input_data = np.loadtxt(INPUT_FILE)
input_data_mean = input_data.mean()
# input_data_median = np.percentile(input_data,50)
# input_data_90_ptile = np.percentile(input_data,90)
input_data_99_ptile = np.percentile(input_data,99)

print "Avg slowdown: ", sum(slowdowns)/len(slowdowns)
# print "Median slowdown: ", input_data_median
print "99 slowdown: ", input_data_99_ptile

# outfile = open(OUTPUT_FILE,'w')
# outfile.write(str(input_data_mean) + '\n')
# outfile.write(str(input_data_median) + '\n')
# outfile.write(str(input_data_90_ptile) + '\n')
# outfile.write(str(input_data_99_ptile) + '\n')
# outfile.close()


# INPUT_FILE = throughputfile
# OUTPUT_FILE = INPUT_FILE + '.result'

# input_data = np.loadtxt(INPUT_FILE)
# input_data_mean = input_data.mean()
# input_data_median = np.percentile(input_data,50)
# input_data_90_ptile = np.percentile(input_data,90)
# input_data_99_ptile = np.percentile(input_data,99)

# print "Avg throughput: ", input_data_mean
# print "Median througput: ", input_data_median
# print "99 throughput: ", input_data_99_ptile

# outfile = open(OUTPUT_FILE,'w')
# outfile.write(str(input_data_mean) + '\n')
# outfile.write(str(input_data_median) + '\n')
# outfile.write(str(input_data_90_ptile) + '\n')
# outfile.write(str(input_data_99_ptile) + '\n')
# outfile.close()



# max_oct = max(octs)
# oct_bin_slowdown_dict = {}
# for i in range(int(math.floor(math.log(max_oct,2)))+1):
#     oct_bin_slowdown_dict[i] = []

# for i in range(len(slowdowns)):
#     oct_bin_slowdown_dict[int(math.floor(math.log(octs[i],2)))].append(slowdowns[i])

# for i in range(int(math.floor(math.log(max_oct,2)))+1):
#     if(len(oct_bin_slowdown_dict[i]) == 0):
#         oct_bin_slowdown_dict[i].append(0)

# bins = range(int(math.floor(math.log(max_oct,2)))+1)
# avg_octs = [sum(oct_bin_slowdown_dict[i])/len(oct_bin_slowdown_dict[i]) for i in range(int(math.floor(math.log(max_oct,2)))+1)]
# avg_octs_ninety = [np.percentile(oct_bin_slowdown_dict[i],90) for i in range(int(math.floor(math.log(max_oct,2)))+1)]
# avg_octs_ninetynine = [np.percentile(oct_bin_slowdown_dict[i],99) for i in range(int(math.floor(math.log(max_oct,2)))+1)]

# np.savetxt(octbinsfile,avg_octs)

# plt.figure(1)
# plt.plot(bins,avg_octs,color='red',label='mean',linewidth=3)
# plt.plot(bins,avg_octs_ninetynine,color='blue',label='99',linewidth=3)
# # plt.xscale('log')
# plt.yscale('log')
# plt.grid(True, which='both')
# plt.xlabel('Flows binned by size', fontsize=20)
# plt.ylabel('Slowdown', fontsize=20)
# plt.title('Binned Slowdown')
# plt.legend(fontsize=8)
# plt.tight_layout()
# plt.tick_params(axis='both', which='major', labelsize=18)
# plt.savefig(plotfile, format = 'eps', dpi = 1000)
# plt.savefig(plotfile_png, format = 'png')


# max_flow_size = max(flow_sizes)
# flowsize_bin_slowdown_dict = {}
# for i in range(int(math.floor(math.log(max_flow_size,10)))+1):
#     flowsize_bin_slowdown_dict[i] = []

# for i in range(len(slowdowns)):
#     flowsize_bin_slowdown_dict[int(math.floor(math.log(flow_sizes[i],10)))].append(slowdowns[i])

# for i in range(int(math.floor(math.log(max_flow_size,10)))+1):
#     if(len(flowsize_bin_slowdown_dict[i]) == 0):
#         flowsize_bin_slowdown_dict[i].append(0)

# bins = range(int(math.floor(math.log(max_flow_size,10)))+1)
# avg_flow_sizes = [sum(flowsize_bin_slowdown_dict[i])/len(flowsize_bin_slowdown_dict[i]) for i in range(int(math.floor(math.log(max_flow_size,10)))+1)]
# avg_flow_sizes_ninety = [np.percentile(flowsize_bin_slowdown_dict[i],90) for i in range(int(math.floor(math.log(max_flow_size,10)))+1)]
# avg_flow_sizes_ninetynine = [np.percentile(flowsize_bin_slowdown_dict[i],99) for i in range(int(math.floor(math.log(max_flow_size,10)))+1)]

# np.savetxt(flowsizebinsfile,avg_flow_sizes)
# np.savetxt(flowsizebinsfile_99,avg_flow_sizes_ninetynine)

# plt.figure(2)
# plt.plot(bins[3:],avg_flow_sizes[3:],color='red',label='mean',linewidth=3)
# plt.plot(bins[3:],avg_flow_sizes_ninetynine[3:],color='blue',label='99',linewidth=3)
# # plt.xscale('log')
# plt.yscale('log')
# plt.grid(True, which='both')
# plt.xlabel('Flows binned by size', fontsize=20)
# plt.ylabel('Slowdown', fontsize=20)
# plt.title('Binned Slowdown')
# plt.legend(fontsize=8)
# plt.tight_layout()
# plt.tick_params(axis='both', which='major', labelsize=18)
# plt.savefig(plotfile_flowsizes, format = 'eps', dpi = 1000)
# plt.savefig(plotfile_flowsizes_png, format = 'png')
