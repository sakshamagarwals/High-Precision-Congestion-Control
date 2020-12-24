for i in {1..5}
do
    for j in {1..9}
    do
        echo fg-0.$i-bg-0.$j
        mkdir fg-0.$i-bg-0.$j
        echo ../../workloadgen/b-100-a-0.0-fg-128kb-bg-dctcp-3x/fg-0.$i-bg-0.$j.txt.hpcc fg-0.$i-bg-0.$j/flow.txt
        cp ../../workloadgen/b-100-a-0.0-fg-128kb-bg-dctcp-3x/fg-0.$i-bg-0.$j.txt.hpcc fg-0.$i-bg-0.$j/flow.txt
    done
done