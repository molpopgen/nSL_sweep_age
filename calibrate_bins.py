from collections import namedtuple
import msprime
import libsequence.polytable
import libsequence.summstats
import libsequence.msprime
import numpy as np
import argparse
import pandas as pd

Datum = namedtuple("Datum", ['dafbin', 'mean', 'sd'])


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nsam", type=int, default=100)
    parser.add_argument("--theta", type=float, default=100.)
    parser.add_argument("--nreps", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=-1)
    parser.add_argument("--rho", type=float, default=100.)
    parser.add_argument("--binsize", "-b", type=int, default=-1)
    parser.add_argument("--minfreq", "-m", type=int, default=-1)
    parser.add_argument("--outfile", type=str, default=None)

    return parser


def get_bin_stats(sd, args):
    raw = libsequence.summstats.nSLiHS(sd)

    if args.minfreq > 0:
        raw = [i for i in raw if i[2] >= args.minfreq]
    raw = [i for i in raw if np.isfinite(i[0]) == 1]

    raw_array = np.array(raw)
    bins = np.digitize(raw_array[:, 2], np.arange(0, sd.size(), args.binsize))
    rv = []
    for b in np.unique(bins):
        w = np.where(bins == b)[0]
        stats = raw_array[:, 0][w]
        m = stats.mean()
        sd = stats.std()
        rv.append(Datum(b, m, sd))
    return rv


if __name__ == "__main__":
    p = make_parser()
    args = p.parse_args()

    results = []
    for ts in msprime.simulate(args.nsam, mutation_rate=args.theta/4.,
                               recombination_rate=args.theta/4.,
                               num_replicates=args.nreps,
                               random_seed=args.seed):
        sd = libsequence.msprime.make_SimData(ts)
        bins = get_bin_stats(sd, args)
        results.extend(bins)
    df = pd.DataFrame(results, columns=Datum._fields)
    g = df.groupby(['dafbin']).mean().reset_index()
    with open(args.outfile, 'w') as f:
        g.to_csv(f, sep=' ', index=False)
