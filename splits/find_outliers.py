import random
import sys
import os
import argparse
import itertools
import csv

import numpy
import torch
import cv2
import torchvision

def parse_arguments(args):
    desc = (
        "3D60 dataset outliers generator."
    )
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--action', type=str, \
        default='calc', help='The action that will be run with \'calc\' used to find the outliers and \'save\' used to save them as tiled images.')
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
    parser.add_argument("--outliers_path", type=str,\
        default=".\\splits\\", \
        help="The path where the generated outliers files will be saved at.")
    # thresholds
    parser.add_argument("--lower_threshold", type=float,\
        default=0.5, help="Near (i.e. lower) distance value threshold.")
    parser.add_argument("--upper_threshold", type=float,\
        default=8.0, help="Far (i.e. upper) distance value threshold.")
    parser.add_argument("--m3d_lower_bound", type=float,\
        default=0.05, help="Near pixel percentage threshold for images that will be rejected as bad renders for Matterport3D.")
    parser.add_argument("--m3d_upper_bound", type=float,\
        default=0.25, help="Far pixel percentage threshold for images that will be rejected as bad renders for Matterport3D.")
    parser.add_argument("--s2d3d_lower_bound", type=float,\
        default=0.05, help="Near pixel percentage threshold for images that will be rejected as bad renders for Stanford2D3D.")
    parser.add_argument("--s2d3d_upper_bound", type=float,\
        default=0.2, help="Far pixel percentage threshold for images that will be rejected as bad renders for Stanford2D3D.")
    parser.add_argument("--suncg_lower_bound", type=float,\
        default=0.1, help="Near pixel percentage threshold for images that will be rejected as bad renders for SunCG.")
    parser.add_argument("--suncg_upper_bound", type=float,\
        default=0.2, help="Far pixel percentage threshold for images that will be rejected as bad renders for SunCG.")

    return parser.parse_known_args(args)

def load_image(filename, data_type=torch.float32):
    color_img = numpy.array(cv2.imread(filename, cv2.IMREAD_ANYCOLOR))
    h, w, c = color_img.shape
    color_data = color_img.astype(numpy.float32).transpose(2, 0, 1)
    return torch.from_numpy(
        color_data.reshape(1, c, h, w)        
    ).type(data_type) / 255.0

def load_depth(filename, data_type=torch.float32):
    dtmp = numpy.array(cv2.imread(filename, cv2.IMREAD_ANYDEPTH))
    depth = torch.from_numpy(dtmp).type(data_type)
    return depth.reshape(1, 1, depth.shape[0], depth.shape[1])

def find_outliers(folder, lower_threshold, upper_threshold, 
    lower_bound, upper_bound):
    outliers = []
    depth_files = [f for f in os.listdir(folder) if ".exr" in f and "_depth_" in f]    
    for depth_file in depth_files:
        filename = os.path.join(folder, depth_file)        
        depth = load_depth(filename)
        b, c, h, w = depth.size()        
        over = torch.sum(depth > upper_threshold).float()
        under = torch.sum(depth < lower_threshold).float()        
        over_perc = over / (h * w)
        under_perc = under / (h * w)
        if over_perc > upper_bound or under_perc > lower_bound:
            outliers.append(depth_file)
    return outliers

def create_m3d_outliers(m3d_path, lower_threshold, upper_threshold, 
    lower_bound, upper_bound):
    result = {}
    result['m3d'] = list()
    result['m3d'].extend(find_outliers(m3d_path, lower_threshold, upper_threshold, \
        lower_bound, upper_bound))
    return result

def create_s2d3d_outliers(s2d3d_path, lower_threshold, upper_threshold, 
    lower_bound, upper_bound):
    result = {}
    result['s2d3d'] = list()
    for area in os.listdir(s2d3d_path):
        result['s2d3d'].extend(find_outliers(os.path.join(s2d3d_path, area), \
            lower_threshold, upper_threshold, lower_bound, upper_bound))
    return result

def create_suncg_outliers(suncg_path, lower_threshold, upper_threshold, 
    lower_bound, upper_bound):
    result = {}
    result['scg'] = list()
    result['scg'].extend(find_outliers(suncg_path, lower_threshold, upper_threshold, \
        lower_bound, upper_bound))
    return result

def dump_outliers(splits, args):
    for outlier in outliers:
        for k, v in outlier.items():
            with open(os.path.join(args.outliers_path, '{}_outliers.csv'.format(k)), mode='w') as csv_file:
                outlier_writer = csv.writer(csv_file, delimiter=',', \
                    lineterminator='\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                outlier_writer.writerow(['Outliers'])
                for o in v:
                    outlier_writer.writerow([o])

def save_outliers(args):
    paths, outliers_files, names = [], [], []
    if 'suncg_path' in args:
        paths.append(args.suncg_path)
        outliers_files.append(os.path.join(args.outliers_path, "scg_outliers.csv"))
        names.append('suncg')
    if 'm3d_path' in args:
        paths.append(args.m3d_path)
        outliers_files.append(os.path.join(args.outliers_path, "m3d_outliers.csv"))
        names.append('m3d')
    if 's2d3d_path' in args:
        paths.append(os.path.join(args.s2d3d_path, 'area1'))
        paths.append(os.path.join(args.s2d3d_path, 'area2'))
        paths.append(os.path.join(args.s2d3d_path, 'area3'))
        paths.append(os.path.join(args.s2d3d_path, 'area4'))
        paths.append(os.path.join(args.s2d3d_path, 'area5a'))
        paths.append(os.path.join(args.s2d3d_path, 'area5b'))
        paths.append(os.path.join(args.s2d3d_path, 'area6'))
        outliers_files.append(os.path.join(args.outliers_path, "s2d3d_outliers.csv"))
        outliers_files.append(os.path.join(args.outliers_path, "s2d3d_outliers.csv"))
        outliers_files.append(os.path.join(args.outliers_path, "s2d3d_outliers.csv"))
        outliers_files.append(os.path.join(args.outliers_path, "s2d3d_outliers.csv"))
        outliers_files.append(os.path.join(args.outliers_path, "s2d3d_outliers.csv"))
        outliers_files.append(os.path.join(args.outliers_path, "s2d3d_outliers.csv"))
        outliers_files.append(os.path.join(args.outliers_path, "s2d3d_outliers.csv"))
        names.append('s2d3d_a1')
        names.append('s2d3d_a2')
        names.append('s2d3d_a3')
        names.append('s2d3d_a4')
        names.append('s2d3d_a5a')
        names.append('s2d3d_a5b')
        names.append('s2d3d_a6')

    for o, n, p in zip(outliers_files, names, paths):
        with open(o, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            line_count = 0
            viz_count = 0
            saved_images = 0
            tiles_per_image = 64
            tensor = torch.zeros([tiles_per_image, 3, 256, 512])
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    filename = os.path.join(p, row[0].replace('depth', 'color').replace('exr', 'png'))
                    if os.path.exists(filename) and '90.0' not in filename \
                            and '180.0' not in filename and '270.0' not in filename \
                            and 'Up' not in filename and 'Right' not in filename:
                        img = load_image(filename)
                        viz_count += 1
                        tensor[viz_count % tiles_per_image, :, :, :] = img
                    line_count += 1
                    if viz_count % tiles_per_image == 0 and viz_count != 0:
                        torchvision.utils.save_image(tensor, \
                            os.path.join(args.outliers_path, '{}_outliers_{}.png'.format(n, saved_images)))
                        tensor = torch.zeros([tiles_per_image, 3, 256, 512])
                        viz_count = 0
                        saved_images += 1
            if viz_count < tiles_per_image:
                torchvision.utils.save_image(tensor, \
                        os.path.join(args.outliers_path, '{}_outliers_{}.png'.format(n, saved_images)))
            print(f'Processed {line_count} lines for {n}.')

if __name__ == "__main__":
    args, unknown = parse_arguments(sys.argv)
    if args.action == 'calc':
        outliers = list()
        ''' Matterport3D '''
        if 'm3d_path' in args:
            m3d_outliers = create_m3d_outliers(args.m3d_path, \
                args.lower_threshold, args.upper_threshold, \
                args.m3d_lower_bound, args.m3d_upper_bound)
            outliers.append(m3d_outliers)
        ''' Stanford2D3D '''
        if 's2d3d_path' in args:
            s2d3d_outliers = create_s2d3d_outliers(args.s2d3d_path, \
                args.lower_threshold, args.upper_threshold, \
                args.s2d3d_lower_bound, args.s2d3d_upper_bound)
            outliers.append(s2d3d_outliers)
        ''' SunCG '''
        if 'suncg_path' in args:
            suncg_outliers = create_suncg_outliers(args.suncg_path, \
                args.lower_threshold, args.upper_threshold, \
                args.suncg_lower_bound, args.suncg_upper_bound)
            outliers.append(suncg_outliers)
        dump_outliers(outliers, args)
    elif args.action == 'save':
        save_outliers(args)
    else:
        print("Erroneous action selection, can only be one of calc/save.")