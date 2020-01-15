import numpy as np 
import matplotlib.pyplot as plt 
plt.switch_backend('agg')

FILE1 = 'experiments/aditya-l-0.5-100K-test/hpcc/flowsizebins_avg.txt'
FILE2 = 'experiments/aditya-l-0.5-100K-uniform/hpcc/flowsizebins_avg.txt'

FILE3 = 'experiments/aditya-l-0.5-100K-test/hpcc/flowsizebins_99.txt'
FILE4 = 'experiments/aditya-l-0.5-100K-uniform/hpcc/flowsizebins_99.txt'

l1 = np.loadtxt(FILE1)
l2 = np.loadtxt(FILE2)
l3 = np.loadtxt(FILE3)
l4 = np.loadtxt(FILE4)

plt.plot(l1[3:],color='red',label='mean, bundled',linewidth=3)
plt.plot(l2[3:],'--',color='red',label='mean, unbunbled',linewidth=3)
plt.plot(l3[3:],color='blue',label='tail, bundled',linewidth=3)
plt.plot(l4[3:],'--',color='blue',label='tail, unbunbled',linewidth=3)
# plt.xscale('log')
# plt.yscale('log')
plt.grid(True, which='both')
plt.xlabel('Flows binned by size', fontsize=20)
plt.ylabel('Slowdown', fontsize=20)
plt.title('Binned Slowdown')
plt.legend(fontsize=8)
plt.tight_layout()
plt.tick_params(axis='both', which='major', labelsize=18)
plt.savefig('plot-unbundled-aditya-l-0.5-40Gbps.eps', format = 'eps', dpi = 1000)
plt.savefig('plot-unbundled-aditya-l-0.5-40Gbps.png', format = 'png')
