sizes = set()
for flow in open('experiments/flow.txt', 'r').readlines()[1:]:
    sizes.add(int(flow.split()[4]))

max_size = 2107
with open('experiments/test/oracle.txt', 'w') as f:
    f.write(str(max_size*2)+'\n')
    second = 1
    for i in range(max_size):
        f.write("{0} {1} 3 100 {2} {3}\n".format(
            1, 2, (i+1)*1000, second))
        second += 0.0005
        f.write("{0} {1} 3 100 {2} {3}\n".format(
            1, 100, (i+1)*1000, second))
        second += 0.0005
