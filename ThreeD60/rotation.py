from torch.utils.data import Dataset
from .common import _rotate_image, _rotate_normal_image, ImageTypes
import random

class RotationDataset(Dataset):
    def __init__(self, SuperDataset):
        super(RotationDataset, self).__init__()
        self.Super = SuperDataset
        
    def __len__(self):
        return self.Super.__len__()

    def __getitem__(self, index):
        entries = self.Super.__getitem__(index)
        width = entries['left_down']['color'].shape[2]
        idx = random.randint(0, width - 1)
        for placement, type_map in entries.items():
            if 'color' in type_map:
                entries[placement]['color'] = _rotate_image(entries[placement]['color'], idx)
            if 'depth' in type_map:
                entries[placement]['depth'] = _rotate_image(entries[placement]['depth'], idx)
            if 'normal' in type_map:
                entries[placement]['normal'] = _rotate_normal_image(entries[placement]['normal'], idx)
        return entries

    
