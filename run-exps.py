import subprocess
import time

processes = []
for i in [2]:
    for j in [1,2,3,4,5]:
        exp_name = 'fg-0.' + str(i) + '-bg-0.' + str(j)
        print("Running exp: ",exp_name)
        p = subprocess.Popen(['./run-me.sh' + ' ' + exp_name],shell=True)
        processes.append(p)
        print("PID: ",p.pid)
        time.sleep(5)

exit_codes = [p.wait() for p in processes]
print(exit_codes)