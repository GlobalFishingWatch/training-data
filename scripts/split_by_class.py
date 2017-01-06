#! /usr/bin/env python

from __future__ import print_function
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import tools as trtools
import logging
import numpy as np
import csv


def split_by_vessel_type(points, class_map):
    mmsis = np.unique(points['mmsi'])

    mmsi_map = {}
    for mmsi in mmsis:
        cls = class_map.get(mmsi, "Unknown")
        if cls not in mmsi_map: mmsi_map[cls] = set()
        mmsi_map[cls].add(mmsi)

    for cls, mmsis in mmsi_map.iteritems():
        filter = reduce(
            lambda a, b: a | b,
            (points['mmsi'] == mmsi for mmsi in mmsis))
        yield cls, points[filter]

def clean_format(x):
    for c in "\/ :":
        x = x.replace(c, '_')
    return x

if __name__ == "__main__":
    logging.getLogger().setLevel("INFO")
    import argparse
    parser = argparse.ArgumentParser(
        description='Split vessels as type')
    parser.add_argument(
        'sources', nargs='+', help="source (npz) files")
    parser.add_argument(
        '--classes', required=True, help="path mapping mmsi to vessel type")
    parser.add_argument(
        '--field', default="label", help="field in class file used for mapping. Defaults to `label`")
    parser.add_argument(
        '--output_template', default="./{source}_{cls}.npz", help="template for writing out files (use {cls} for class)")
    args = parser.parse_args()

    with open(args.classes) as f:
        reader =  csv.DictReader(f) 
        class_map = {float(x['mmsi']): x[args.field] for x in reader if x[args.field]}

    for inpth in args.sources:
        logging.info("Loading: %s", inpth)
        points = np.load(inpth)['x']

        for cls, points_for_cls in split_by_vessel_type(points, class_map):
            logging.info("Starting conversion for class: %s", cls)
            outpth = args.output_template.format(source=os.path.splitext(os.path.basename(inpth))[0],
                                                 cls=clean_format(cls))
            sub_points = np.array(list(points_for_cls))
            if len(sub_points):
                logging.info("Writing %s rows to %s", len(sub_points), outpth)
                np.savez_compressed(outpth, x=sub_points)
