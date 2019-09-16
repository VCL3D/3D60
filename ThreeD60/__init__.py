from .matterport3d import *
from .stanford2d3d import *
from .suncg import *
from .common import Placements, ImageTypes, extract_image, extract_path

from torch.utils.data import ConcatDataset

_dataset_generators = {
    "suncg": lambda *params: SunCG(params[0], params[1], params[2]),
    "m3d": lambda *params: Matterport3D(params[0], params[1], params[2]),
    "s2d3d": lambda *params: Stanford2D3D(params[0], params[1], params[2])
}

def get_datasets(filename, datasets=["suncg", "s2d3d", "m3d"], \
        placements=[Placements.CENTER, Placements.RIGHT, Placements.UP], \
        image_types=[ImageTypes.COLOR, ImageTypes.DEPTH, ImageTypes.NORMAL]):
    return ConcatDataset(list(map(\
        lambda d: _dataset_generators[d](filename, placements, image_types), datasets)))