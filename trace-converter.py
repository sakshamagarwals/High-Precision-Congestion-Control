import sys

INPUT_FILE = sys.argv[1]
print(INPUT_FILE)
OUTPUT_FILE = sys.argv[1] + '.hpcc'
outfile = open(OUTPUT_FILE,'w')

linenum = 0
with open(INPUT_FILE) as f1:
    line_to_write = f1.readline()
    max_line_lim = int(line_to_write[:-1])
    print(max_line_lim)
    outfile.write(line_to_write)
    for line in f1:
        linenum+=1
        if(linenum > max_line_lim):
            break
        line_str = line.split()
        if(len(line_str) != 6):
            print("LINERROR: ",len(line_str), ' ',linenum)
            assert(False)
        else:
            line_to_write = line_str[0] + ' ' + line_str[1] + ' ' + '3' + ' ' + '21553' + ' ' + str(int(line_str[3])*1500) + ' ' + line_str[4]
            outfile.write(line_to_write + '\n')
