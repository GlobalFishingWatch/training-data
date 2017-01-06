#! /bin/bash

mkdir data/merged
scripts/merge_ais_and_ranges.py \
  --source-paths data/time-ranges/*.csv \
  --point-source-path data/tracks \
  --dest-path data/merged

mkdir data/labeled
scripts/split_by_class.py \
  --classes data/mmsis.csv \
  --output_template data/merged/{source}_{cls}.npz \
  data/merged/*.npz
