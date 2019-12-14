import sys
import os

experiment = sys.argv[1]
ccs = {'hpcc', 'dcqcn', 'dctcp', 'timely'}

os.system('mkdir experiments/{0}'.format(experiment))
for cc in ccs:
    os.system('mkdir experiments/{0}/{1}'.format(experiment, cc))
    os.system('cp experiments/aditya/{0}/config.txt experiments/{1}/{0}/config.txt'.format(cc,experiment))
    os.system("sed -i '' 's/aditya/{0}/g' experiments/{0}/{1}/config.txt".format(experiment,cc))
