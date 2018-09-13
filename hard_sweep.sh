#!/bin/bash

echo "tau mean_z" > hard_sweeps_tau_z.txt
for tau in 0 0.0001 0.001 0.01 0.02 0.03 0.04 0.05 0.075 0.1 0.15 0.20
do
~/src/discoal/discoal 100 1000 1000 -ws $tau-x 0.5 -theta 100 -rho 100 -alpha 2000 | python3 calc_from_ms.py --binsize 10 \
--minfreq 3 --binfile b10t100r100.txt --outfile outfiles/hard_b10t100r100.$tau.txt --outfile2 outfiles/hard_b10t100r100_meanz.$tau.txt
x=`cat outfiles/hard_b10t100r100_meanz.$tau.txt`
echo $tau $x
done >> hard_sweeps_tau_z.txt

