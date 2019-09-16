import csv
import itertools
import cv2
import numpy
import torch
import enum
import logging

class Placements(enum.Enum):
    CENTER = 1    
    RIGHT = 2
    UP = 3

    def describe(self):        
        return self.name.lower(), self.value

    def __str__(self):
        n = str.lower(self.name) if self.value != 1 else str("left_down")
        return n

class ImageTypes(enum.Enum):
    COLOR = 1    
    DEPTH = 2
    NORMAL = 3

    def describe(self):        
        return self.name.lower(), self.value

    def __str__(self):
        return str.lower(self.name)        

_dataset_images_order = [
    str.format("{}_{}", str(Placements.CENTER), str(ImageTypes.COLOR)),
    str.format("{}_{}", str(Placements.RIGHT), str(ImageTypes.COLOR)),
    str.format("{}_{}", str(Placements.UP), str(ImageTypes.COLOR)),
    str.format("{}_{}", str(Placements.CENTER), str(ImageTypes.DEPTH)),
    str.format("{}_{}", str(Placements.RIGHT), str(ImageTypes.DEPTH)),
    str.format("{}_{}", str(Placements.UP), str(ImageTypes.DEPTH)),
    str.format("{}_{}", str(Placements.CENTER), str(ImageTypes.NORMAL)),
    str.format("{}_{}", str(Placements.RIGHT), str(ImageTypes.NORMAL)),
    str.format("{}_{}", str(Placements.UP), str(ImageTypes.NORMAL)),

    # "left_down_color",
    # "right_color",
    # "up_color",
    # "left_down_depth",
    # "right_depth",
    # "up_depth",
    # "left_down_normal",
    # "right_normal",
    # "up_normal",
]

_filename_separator = "_path"

def _create_selectors(placements, types):
    return list(map( \
        lambda o: any(str(p) in o for p in placements) and any(str(t) in o for t in types), \
            _dataset_images_order))

def _load_paths(filename, name, placements, image_types):         
    selectors = _create_selectors(placements, image_types)
    with open (filename, 'r') as f:
        rows = [list(itertools.compress(row, selectors)) for row in csv.reader(f, delimiter=' ')]
        return list(map(
            lambda row: dict(list(
                (
                    str(p), dict(list(
                    (                        
                        str(t) + _filename_separator, \
                            next(filter(lambda r: str(p) in r.lower() and str(t) in r.lower(), row))
                    ) for t in image_types
                    ))
                ) for p in placements
            ))
        , [row for row in rows if all(map(lambda r: name in r, row))]
        ))

def _load_color_image(filename, data_type):
    color_img = numpy.array(cv2.imread(filename, cv2.IMREAD_ANYCOLOR))
    color_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2RGB).transpose(2, 0, 1)
    c, h, w = color_img.shape    
    return torch.from_numpy(color_img).reshape(c, h, w).type(data_type) / 255.0

def _load_depth_image(filename, data_type):
    depth_img = numpy.array(cv2.imread(filename, cv2.IMREAD_ANYDEPTH))
    h, w = depth_img.shape
    return torch.from_numpy(depth_img).type(data_type).reshape(1, h, w)

def _load_normal_image(filename, data_type):
    normal_img = numpy.array(cv2.imread(filename, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)).transpose(2, 0, 1)
    c, h, w = normal_img.shape
    return torch.from_numpy(normal_img).reshape(c, h, w).type(data_type)

_image_loaders = {
    "color": lambda *params: _load_color_image(params[0], params[1]),
    "depth": lambda *params: _load_depth_image(params[0], params[1]),
    "normal": lambda *params: _load_normal_image(params[0], params[1]),
}

def _load_image(filename, image_type, data_type=torch.float32):
    return _image_loaders[image_type](filename, data_type)

def extract_image(tensor_dict, placement: Placements, image_type: ImageTypes):
    if not str(placement) in tensor_dict or not str(image_type) in tensor_dict[str(placement)]:
        logging.fatal("Could not extract the requested placement/image (%s/%s) from the given tensor dictionary." % (placement, image_type))
        exit()
    return tensor_dict[str(placement)][str(image_type)]

def extract_path(tensor_dict, placement: Placements, image_type: ImageTypes):
    if not str(placement) in tensor_dict or not str(image_type) + _filename_separator in tensor_dict[str(placement)]:
        logging.fatal("Could not extract the requested placement/image (%s/%s) path from the given tensor dictionary." % (placement, image_type))
        exit()
    return tensor_dict[str(placement)][str(image_type) + _filename_separator]