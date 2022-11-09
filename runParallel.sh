#!/bin/bash

for i in $(eval echo {1..$1})	 
do
    (time python3 mymain04.py $i ) 2>&1 | tee logs/pythiaStats$i.log &
done
