import dateutil.parser
import numpy as np
import numpy.lib.recfunctions

def merge_ais(points, ranges):
    points.sort(order=["mmsi", "timestamp"])
    points = numpy.lib.recfunctions.append_fields(points, 'is_fishing', [], dtypes='<f4')
    points['is_fishing'] = -1

    mmsi_ranges = {}

    def get_slice(data, col, low, high):
        startidx = numpy.searchsorted(data[col], low, 'left')
        endidx = startidx + numpy.searchsorted(data[col][startidx:], high, 'right')
        return {'start': startidx, 'end': endidx}

    def get_mmsi_slice(mmsi):
        if mmsi not in mmsi_ranges:
            mmsi_ranges['mmsi'] = get_slice(points, 'mmsi', mmsi, mmsi)
        return mmsi_ranges['mmsi']

    for range in ranges:
        mmsi_slice = get_mmsi_slice(range['mmsi'])
        slice = get_slice(points[mmsi_slice['start']:mmsi_slice['end']], 'timestamp', range['start_time'], range['end_time'])
        slice['start'] += mmsi_slice['start']
        slice['end'] += mmsi_slice['start']
        points['is_fishing'][slice['start']:slice['end']] = range['is_fishing']
    return points

