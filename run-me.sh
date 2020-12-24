EXP_NAME=$1

echo python run.py --exp ${EXP_NAME} --topo topology-650ns-100Gbps --bw 100
python run.py --exp ${EXP_NAME} --topo topology-650ns-100Gbps --bw 100
echo python run.py --exp ${EXP_NAME} --topo topology-650ns-100Gbps --bw 100 --run 1 > experiments/${EXP_NAME}/hpcc/temp.log
python run.py --exp ${EXP_NAME} --topo topology-650ns-100Gbps --bw 100 --run 1 > experiments/${EXP_NAME}/hpcc/temp.log