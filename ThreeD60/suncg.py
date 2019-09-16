import os
import copy

from torch.utils.data import Dataset

from .common import _load_paths, _load_image, _filename_separator

class SunCG(Dataset):
    def __init__(self, filename, placements, image_types):
        assert(os.path.exists(filename))
        super(SunCG, self).__init__()
        self.entries = _load_paths(filename, type(self).__name__, placements, image_types)

    def __len__(self):
        return len(self.entries)

    def __getitem__(self, index):
        entries = copy.deepcopy(self.entries[index])
        for placement, type_map in self.entries[index].items():
            for typed_path, filename in type_map.items():
                image_type = typed_path.replace(_filename_separator, "")
                entries[placement][image_type] = _load_image(filename, image_type)
        return entries