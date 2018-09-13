#!/bin/bash

for final in 0.05 0.1 0.5 0.9
do
    F=`echo "$final*100"|bc` #|sed 's/\.0//g'`
    echo $F
     ~/src/discoal/discoal 100 100 1000 -ws 0 -c $final -x 0.5 -theta 100 -rho 100 -alpha 2000 | python3 calc_from_ms.py \
     --binsize 10 \
     --minfreq 3 --binfile b5t100r100.txt --outfile incomplete_F$F"b5t100r100.txt" \
     --outfile2 incomplete_F$F"b5t100r100_meanz.txt"
done

