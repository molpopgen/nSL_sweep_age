#!/bin/bash

~/src/discoal/discoal 100 100 1000 -ws 0.02 -x 0.5 -theta 100 -rho 100 -alpha 2000 | python3 calc_from_ms.py --binsize 10 \
--minfreq 3 --binfile b5t100r100.txt --outfile hard_b5t100r100.txt --outfile2 hard_b5t100r100_meanz.txt

