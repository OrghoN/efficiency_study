#!/bin/bash





for i in $(eval echo {1..$1})	
do
    seed=$(($i + $2))
    cp beamParametersTemplate.cmnd cmnd/beamParameters$seed.cmnd
    sed -i "s/Random:seed = 0/Random:seed = $seed/" cmnd/beamParameters$seed.cmnd
    (time python3 mymain04.py $seed ) 2>&1 | tee logs/pythiaStats$i.log & # 
done
