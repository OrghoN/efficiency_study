#!/bin/bash

#Argument 1 sets number of processes. Default is 1.
if [[ $1 != "" ]]; then
    noOfProcesses=$1
else
    noOfProcesses=1
fi

#Argument 2 sets seed offset. Default is 0.
if [[ $2 != "" ]]; then
    seedOffset=$2
else
    seedOffset=0
fi



for i in $(eval echo {1..$noOfProcesses})      
do
    seed=$(($i + $seedOffset))
    cp beamParametersTemplate.cmnd cmnd/beamParameters$seed.cmnd
    sed -i "s/Random:seed = 0/Random:seed = $seed/" cmnd/beamParameters$seed.cmnd
    (time python3 mymain04.py $seed ) 2>&1 | tee logs/pythiaStats$i.log & # 
done
