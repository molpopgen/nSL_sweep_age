from collections import namedtuple
import libsequence.polytable
import libsequence.summstats
import numpy as np
import argparse
import pandas as pd


BinRecord = namedtuple("BinRecord", ['dafbin', 'meanz', 'meanstat','nmuts'])


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--binfile", type=str, default=None)
    parser.add_argument("--outfile", type=str, default=None)
    parser.add_argument("--outfile2", type=str, default=None)
    parser.add_argument("--binsize", "-b", type=int, default=-1)
    parser.add_argument("--minfreq", "-m", type=int, default=-1)

    return parser


def get_stats(sd, neutral_bins, args):
    raw = libsequence.summstats.nSLiHS(sd)

    if args.minfreq > 0:
        raw = [i for i in raw if i[2] >= args.minfreq]
    raw = [i for i in raw if np.isfinite(i[0]) == 1]

    raw_array = np.array(raw)
    if len(raw_array) == 0:
        return None, None
    bins = np.digitize(raw_array[:, 2], np.arange(0, sd.size(), args.binsize))

    rv = []
    zscores = []
    for b in np.unique(bins):
        w = np.where(bins == b)[0]
        stats = raw_array[:, 0][w]
        m = neutral_bins['mean'][b]
        sd = neutral_bins['sd'][b]
        z = (stats-m)/sd
        zscores.extend(z.tolist())
        rv.append(BinRecord(b, z.mean(), stats.mean(), len(w)))

    m=0.0
    ttl=0
    for i in rv:
        ttl += i.nmuts
    for i in rv:
        m += i.meanz*float(i.nmuts)/float(ttl)
    assert ttl == len(zscores), "number of observations error"
    return rv, np.array(zscores).mean()


if __name__ == "__main__":
    p = make_parser()
    args = p.parse_args()

    with open(args.binfile, 'r') as f:
        neutral_bins = pd.read_csv(f, sep=' ', header=0, index_col=0)

    sd = libsequence.polytable.SimData()
    success = sd.from_stdin()
    stats_per_daf_bin = []
    mean_zscores = []
    while success is True:
        bins, mz = get_stats(sd, neutral_bins, args)
        if mz is not None:
            mean_zscores.append(mz)
        if bins is not None:
            stats_per_daf_bin.extend(bins)
        success = sd.from_stdin()
    df = pd.DataFrame(stats_per_daf_bin, columns=BinRecord._fields)
    df.dropna(inplace=True)
    dfg = df.groupby(['dafbin']).mean().reset_index()
    with open(args.outfile, 'w') as f:
        dfg.to_csv(f, sep=" ", index=False)
    with open(args.outfile2, 'w') as f:
        f.write("Mean overall z-score is {}\n".format(np.array(mean_zscores).mean()))
