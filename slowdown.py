import argparse
import numpy as np
from matplotlib import pyplot

bd1 = 40
bd2 = 160
latency = 200


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--input')
    args = parser.parse_args()

    slowdowns = []
    with open(args.input, 'r') as f:
        for line in f.readlines():
            tokens = line.split()
            slowdowns.append(
                int(tokens[6])/oracle(tokens[0], tokens[1], tokens[4]))

    slowdowns = np.array(slowdowns)

    slowdowns.sort()

    s = 0
    i = 0
    dx = 0.01
    X = np.arange(1, 100, dx)
    Y = []
    for s in X:
        while i < len(slowdowns) and slowdowns[i] < s:
            i += 1
        Y.append(i)

    Y = np.array(Y)
    Y = Y/len(slowdowns)
    pyplot.plot(X, Y)
    pyplot.xscale('log')
    pyplot.show()


def ipToNode(ip):
    return (int(ip, 16)-int('0b000001', 16))/int('00000100', 16)


# i,j are hex ip, size is in bytes
def oracle(i, j, size):
    size = int(size)*8
    if ipToNode(i)/16 == ipToNode(j)/16:
        return size/bd1+2*latency
    return size/bd1+4*latency


if __name__ == '__main__':
    main()
