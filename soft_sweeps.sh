#!/bin/bash

echo "f0 tau mean_z" > soft_sweeps_tau_z.txt
for f0 in 0.001 0.01 0.05 0.10
do
    for tau in 0 0.0001 0.001 0.01 0.02 0.03 0.04 0.05 0.075 0.1 0.15 0.20
    do
         OF=outfiles/soft_f$f0"_tau$tau""_b10t100r100_meanz.txt"
         ~/src/discoal/discoal 100 100 1000 -ws $tau -f $f0 -x 0.5 -theta 100 -rho 100 -alpha 2000 | python3 calc_from_ms.py --binsize 10 \
         --minfreq 3 --binfile b10t100r100.txt --outfile outfiles/soft_f$fo"_tau$tau""_b10t100r100.txt" \
         --outfile2 outfiles/soft_f$f0"_tau$tau""_b10t100r100_meanz.txt"
         
         x=`cat $OF`
         
         echo $f0 $tau $x
    done
done >> soft_sweeps_tau_z.txt


