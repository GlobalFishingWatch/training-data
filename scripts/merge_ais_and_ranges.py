#! /usr/bin/env python

"""Merge AIS data and merge with ranges


python scripts/merge_ais_and_ranges.py --dest-path data/time-points --point-source-path data/time-points --source-path data/time-ranges/alex_crowd_sourced.csv 

"""
from __future__ import print_function
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tools.merge_ais import merge_ais
import itertools
import logging
import numpy as np
import os
import dateutil.parser
import tempfile

def parse(x):
    dt = dateutil.parser.parse(x)
    return float(dt.strftime("%s"))

if __name__ == "__main__":
    import argparse
    import glob
    import os
    logging.getLogger().setLevel("WARNING")
    parser = argparse.ArgumentParser(description="Merge AIS data and time ranges.\n")
    parser.add_argument(
        '--point-source-path', help='path to directory holding track points')
    parser.add_argument(
        '--source-paths', help='path to csv file holding ranges', nargs="+")
    parser.add_argument('--dest-path', help='path to output directory', required=True)
    args = parser.parse_args()
    #


    def _parse(x):
        dt = dateutil.parser.parse(x)
        return float(dt.strftime("%s"))

    for range_path in args.source_paths:
        name = os.path.splitext(os.path.basename(range_path))[0]
        print("Merging %s..." % (name,))

        ranges = np.recfromcsv(range_path, delimiter=',',filling_values=np.nan, converters={'start_time': _parse, 'end_time': _parse}, dtype='float')

        files = [os.path.join(args.point_source_path, "%s.npz" % int(mmsi))
                 for mmsi in np.unique(ranges['mmsi'])]
        points = [np.load(file)['x']
                  for file in files
                  if os.path.exists(file)]
        points = np.concatenate(points)

        data = merge_ais(points, ranges)

        np.savez(os.path.join(args.dest_path, name + ".npz"), x=data.filled())
