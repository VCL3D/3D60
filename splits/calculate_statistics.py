import argparse
import sys
import os
import argparse
import csv
import itertools

import cv2
import numpy
import torch

def parse_arguments(args):
    desc = (
        "3D60 dataset statistics calculation."
    )
    parser = argparse.ArgumentParser(description=desc)    
    # paths
    parser.add_argument("--suncg_path", type=str,\
        default=argparse.SUPPRESS,\
        help="Path to the rendered data of SunCG")
    parser.add_argument("--s2d3d_path", type=str,\
        default=argparse.SUPPRESS,\
        help="Path to the rendered data of Stanford2D3D")
    parser.add_argument("--m3d_path", type=str,\
        default=argparse.SUPPRESS,\
        help="Path to the rendered data of Matterport3D")
    parser.add_argument("--stats_path", type=str,\
        default=".\\splits\\", \
        help="Output path where the calculate dataset statistics files will be saved at.")
    parser.add_argument("--max_depth", type=float,\
        default=10, help="Max valid depth value for the statistics calculations")
    
    return parser.parse_known_args(args)

def load_depth(filename, data_type=torch.float32):
    dtmp = numpy.array(cv2.imread(filename, cv2.IMREAD_ANYDEPTH))
    depth = torch.from_numpy(dtmp).type(data_type)
    return depth.reshape(1, 1, depth.shape[0], depth.shape[1])

def calc_stats(name, folder, max_depth_meters=10.0):
    depth_files = [f for f in os.listdir(folder) if ".exr" in f and "_depth_" in f]
    total = torch.zeros(int(max_depth_meters * 2))
    perc = torch.zeros(int(max_depth_meters * 2))
    less_than_half_meter = 0.0
    over_five_meters = 0.0
    count = 0
    for depth_file in depth_files:
        filename = os.path.join(folder, depth_file)        
        depth = load_depth(filename)
        b, c, h, w = depth.size()
        depth = depth.reshape(h * w)
        hist = torch.histc(depth, bins=int(2 * max_depth_meters), \
            min=0, max=max_depth_meters)
        total += hist
        invalid = torch.sum(torch.isnan(depth)) + torch.sum(torch.isinf(depth)) \
            + torch.sum(depth > max_depth_meters)
        valid = depth.size()[0] - invalid
        if valid > 0:
            perc += hist / valid
            less_than_half_meter += torch.sum(depth < 0.5).float() / float(valid)
            over_five_meters += torch.sum(depth > 5.0).float() / float(valid)
            count += 1
    return {
        "name": name,
        "total": total,
        "perc": perc / count * 100,
        'less0.5': less_than_half_meter / count * 100,
        'over5': over_five_meters / count * 100
    }

def calc_m3d_stats(m3d_path, max_depth_meters=10.0):
    print("Calculating M3D stats...")
    return calc_stats("M3D", m3d_path)
    

def calc_s2d3d_stats(s2d3d_path, max_depth_meters=10.0):
    print("Calculating S2D3D stats...")
    stats = []
    count = 0
    total = torch.zeros(int(2 * max_depth_meters))
    perc = torch.zeros(int(2 * max_depth_meters))
    less_than_half_meter = 0
    over_five_meters = 0
    for area in os.listdir(s2d3d_path):
        stats.append(calc_stats("S2D3D", os.path.join(s2d3d_path, area)))    
    for area_stats in stats:
        total += area_stats['total']
        perc += area_stats['perc']
        less_than_half_meter += area_stats['less0.5']
        over_five_meters += area_stats['over5']
    count = len(stats)
    return {
        "name" : "S2D3D",
        "total": total,
        "perc": perc / count,
        'less0.5': less_than_half_meter / count,
        'over5': over_five_meters / count
    }

def calc_suncg_stats(suncg_path, max_depth_meters=10.0):
    print("Calculating SunCG stats...")
    return calc_stats("SCG", suncg_path)

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

def dump_stats(stats, args):
    print("Dumping stats...")
    for stat in stats:        
        with open(os.path.join(args.stats_path, '{}_stats.csv'.format(stat['name'])), mode='w') as csv_file:
            stats_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            headers = ["{}-{}".format(p[0] / 2.0, p[1] / 2.0) for p in pairwise(range(0, 1 + 2 * int(args.max_depth)))]
            headers += ["<0.5", ">5"]
            stats_writer.writerow(headers)
            stats_writer.writerow([str(float(v)) for v in stat['total']])
            stats_writer.writerow([str(float(v) / 100.0) for v in stat['perc']] \
                + [float(stat['less0.5']) / 100.0, float(stat['over5']) / 100.0])

if __name__ == "__main__":
    args, unknown = parse_arguments(sys.argv)
    stats = []
    ''' Matterport3D '''
    if 'm3d_path' in args:
        m3d_stats = calc_m3d_stats(args.m3d_path, args.max_depth)
        stats.append(m3d_stats)
    ''' Stanford2D3D '''
    if 's2d3d_path' in args:
        s2d3d_stats = calc_s2d3d_stats(args.s2d3d_path, args.max_depth)
        stats.append(s2d3d_stats)
    ''' SunCG '''
    if 'suncg_path' in args:
        suncg_stats = calc_suncg_stats(args.suncg_path, args.max_depth)
        stats.append(suncg_stats)
    dump_stats(stats, args)
    print("Done.")