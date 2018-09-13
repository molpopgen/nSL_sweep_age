#!/bin/bash

for f0 in 0.01 0.05 0.10
do
    F=`echo "$f0*100"|bc|sed 's/\.0//g'`
    echo $F
     ~/src/discoal/discoal 100 100 1000 -ws 0 -f $f0 -x 0.5 -theta 100 -rho 100 -alpha 2000 | python3 calc_from_ms.py --binsize 5 \
     --minfreq 3 --binfile b5t100r100.txt --outfile soft_f0$F"b5t100r100.txt" \
     --outfile2 soft_f0$F"b5t100r100_meanz.txt"
done


