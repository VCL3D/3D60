import random
import sys
import os
import argparse
import itertools
import csv
from easydict import EasyDict as edict

S2D3D_Area2Split =\
    {
        "area1": "train",
        "area2": "train",
        "area4": "train",
        "area6": "train",
        "area3": "val",
        "area5a": "test",
        "area5b": "test",        
    }

M3D_Hash2Split =\
    {    
        "ed1e790a785e4b74b895e41682b2ae88":	"test",
        "2797de2c1a00404faa63b1c722809d0c":	"test",
        "a48996e5b4d64ddca7ebae1e8058bb75":	"test",
        "3086b4adcdf0410380493d08fa18185d":	"test",
        "0151156dd8254b07a241a2ffaf0451d4":	"test",
        "95d83883728b4cf089a7338117dafda0":	"test",
        "ef0f394cf59549f2a46b3df2a8ba4620":	"test",
        "d4f8bb56230e4695860deffe751adf20":	"test",
        "e440fec9930c40f780cc2dc1bae19799":	"test",
        "3e02d80e4b4048abb1befdf84ede89d6":	"test",
        "331000ad2a204322916c92f197fbe6cb":	"test",
        "3f6062eeed474a6691e1116032b09fc7":	"test",
        "6cbebf6c7e6647edabb53546e5200c5c":	"test",
        "0b724f78b3c04feeb3e744945517073d":	"test",
        "0b217f59904d4bdf85d35da2cab96347":	"test",
        "380914818d0f4dfa88035fe57f994130":	"test",
        "fa5f164b48f043c6b2b0bb9e8631a482":	"test",
        "72e0512c082d4895b68c82b35884ff98":	"test",
        "bed1a77d92d64f5cbbaaae4feed64ec1":	"train",
        "b94039b4eb8947bdb9ff5719d9173eae":	"train",
        "2e84c97e728d46babd3270f4e1a0ae3a":	"train",
        "04eb2788768d40a38d35d876a02e9624":	"train",
        "0c334eaabb844eaaad049cbbb2e0a4f2":	"train",
        "9c6b166997ae486f96d011c1de0b3427":	"train",
        "d7a2911178dd48e89d6a23afb09cbc11":	"train",
        "da8b0a1818094c3590080b6fbcc5d161":	"train",
        "f04f5cfeb7f34d03a05e6a62fe5bd572":	"train",
        "2fe17a1527c5496ba74a942d442147ab":	"train",
        "caef338e1683434ba3a471ead89008cc":	"train",
        "85cef4a4c3c244479c56e56d9a723ad2":	"train",
        "0b414c5246f64cc3a1f71251e28eb07d":	"train",
        "9f4011217225489ead8fff22ff0b1e15":	"train",
        "e996abcc45ad411fa7f406025fcf2a63":	"train",
        "1bfc8a70a5a048b28425bdc93f15539c":	"train",
        "387b4cca2ac3488da561a13d0b2561f2":	"train",
        "ead4af2db2b44bc08477dee83ce9b1e1":	"train",
        "698437e8ee11434d86a39226e4bd97b7":	"train",
        "7b285021f3114c4cb66675cbd139cd17":	"train",
        "a1c9e2f1618b46bf9c6d9ffee64ad5da":	"train",
        "22ea79f774cd4381b6fd9700495e7162":	"train",
        "80997e9c2f234974bc7227adcceec83d":	"train",
        "a253d4a0a2af436e848e57af525a6133":	"train",
        "6c53b7897e774853845a0086306880d7":	"train",
        "7e39d733f3134410949894d49d072a39":	"train",
        "ef342b3b24fb413b97bff722de0acb23":	"train",
        "b9116f2d4e0a44178d14fe804de4e518":	"train",
        "04d3f2105168491db767ad1fe7bc39df":	"train",
        "2e7560fb87394e69bfe7462470cff2cd":	"train",
        "579e0103ce5b4823a6276f2a943e0576":	"train",
        "886ece56bf7e436e8d5365cbfec29a44":	"train",
        "8caaade0a587493ca329937a41be44fc":	"train",
        "ce4dcbb88c474cc1a0d1a3768062ec5d":	"train",
        "a74d64d3f8d94500816467e5d936db10":	"train",
        "e399b36ee7c94d8886179197335aebb0":	"train",
        "c391c42c70d84a7abe10263925a03acc":	"train",
        "8d41b897141546e5a209d39bd7fbd449":	"train",
        "65a6bb9bce044fa8bc0c1865820930be":	"train",
        "1f638a3819a544669350d1d56688aad3":	"train",
        "f46e2dd75698487ba7838224d9acf3a1":	"train",
        "fbf6d32ff0e044e88355076d502e160b":	"train",
        "e2ed48cedbd04eb1b33b935df4d78911":	"train",
        "975b8a35009841e6aaec4a0124a3e2ff":	"train",
        "cc84e75d262344ed8ade6f0e086cc6a0":	"train",
        "0656f1bc96024777a6247e601a2131ed":	"train",
        "cd658a17893f455198018c3f37b3b4a9":	"train",
        "eb00de2714da4edba8fcd867924c2a27":	"train",
        "edb61af9bebd428aa21a59c4b2597b20":	"train",
        "ae48a43f548144fb8e82c32d4b64148e":	"train",
        "bdf5a25b5dc14e85ba3c70b3cb0635eb":	"train",
        "022cea327b744abe87758faf883425da":	"train",
        "ec72ed7d211541abbdf96faee1d049e3":	"train",
        "b24264da8ac84505872a0cbebdc0ea0d":	"train",
        "d2974dbf53904bb0a907b4b1de0c177b":	"train",
        "b2f1bf0a0de54856b1d9c8816633c0bb":	"train",
        "ef3600fd356e4df3afe10e6e382e5f18":	"train",
        "59e3dc4b2b5848b6a55eb9bc98a42f43":	"train",
        "602971d3594745e6b1ae71d0a1c6fde6":	"train",
        "b693ef1b45de41a6a51bdbf5ee631907":	"train",
        "e9510fcbae554d6cb8136a7274521ff3":	"train",
        "7812e14df5e746388ff6cfe8b043950a":	"val",
        "9266ab00ab6744348efa7afe13b3db9f":	"val",
        "f9aeabd92a05469badd3c6324dc35a55":	"val",
        "0685d2c5313948bd94e920b5b9e1a7b2":	"val",
        "9f2deaf4cf954d7aa43ce5dc70e7abbe":	"val",
        "e0166dba74ee42fd80fccc26fe3f02c8":	"val",
        "a2577698031844e7a5982c8ee0fecdeb":	"val",
        "bd8722e710f14c949259a02ae1a51dee":	"val",
        "eef1d4cc7acb4e2db42b22a2177e7236":	"val",
        "2aa12c3747f948b8bf9df281ec784627":	"val",
        "a641c3f4647545a2a4f5c50f5f5fbb57":	"val",
    }

def parse_arguments(args):
    desc = (
        "3D60 dataset splits generator."
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
    parser.add_argument("--outliers_path", type=str,\
        default=".\\splits\\", \
        help="The path where the outliers files will be read from.")
    # model
    parser.add_argument("--name", type=str, default="3D60",\
        help="Output file name that will be prefixed to the saved files (with corresponding _train, _test and _val suffix).")
    return parser.parse_known_args(args)

def create_m3d_splits(m3d_path):
    m3d_splits = edict({    
        'train': {},
        'val': {},
        'test': {},
    })
    for k, v in M3D_Hash2Split.items():        
        m3d_splits[v][k] = edict()
    for rendered_image in os.listdir(m3d_path):
        for k in M3D_Hash2Split.keys():
            if k in rendered_image:
                pose_id = rendered_image.split("_")[0]
                if pose_id not in  m3d_splits[M3D_Hash2Split[k]][k]:
                    m3d_splits[M3D_Hash2Split[k]][k][pose_id] = list()
                m3d_splits[M3D_Hash2Split[k]][k][pose_id].append(\
                    os.path.join(m3d_path, rendered_image))
                break
    return m3d_splits

def create_s2d3d_splits(s2d3d_path):
    s2d3d_splits = edict({
        'train': {},
        'val': {},
        'test': {},
    })
    for k, v in S2D3D_Area2Split.items():        
        s2d3d_splits[v][k] = edict()
    for area in os.listdir(s2d3d_path):
        for rendered_image in os.listdir(os.path.join(s2d3d_path, area)):
            pose_id = rendered_image.split("_")[0]
            if pose_id not in s2d3d_splits[S2D3D_Area2Split[area]][area]:
                s2d3d_splits[S2D3D_Area2Split[area]][area][pose_id] = list()
            s2d3d_splits[S2D3D_Area2Split[area]][area][pose_id].append(
                os.path.join(s2d3d_path, area, rendered_image))
    return s2d3d_splits

def create_suncg_splits(suncg_path):
    suncg_splits = edict({
        'train': {},
        'val': {},
        'test': {},
    })
    train_percentage = 0.7
    validation_percentage = 0.1
    test_percentage = 0.2
    for rendered_image in os.listdir(suncg_path):
        scene_id = rendered_image.split("_")[0]
        if scene_id not in suncg_splits['train']\
            and scene_id not in suncg_splits['test']\
            and scene_id not in suncg_splits['val']:
            rng = random.random()        
            if rng <= train_percentage:
                if scene_id not in suncg_splits['train']:
                    suncg_splits['train'][scene_id] = edict()
                    suncg_splits['train'][scene_id]['0'] = list()
                suncg_splits['train'][scene_id]['0'].append(
                    os.path.join(suncg_path, rendered_image)
                )
            elif rng >= (1-test_percentage):
                if scene_id not in suncg_splits['test']:
                    suncg_splits['test'][scene_id] = edict()
                    suncg_splits['test'][scene_id]['0'] = list()
                suncg_splits['test'][scene_id]['0'].append(
                    os.path.join(suncg_path, rendered_image)
                )
            else:
                if scene_id not in suncg_splits['val']:
                    suncg_splits['val'][scene_id] = edict()
                    suncg_splits['val'][scene_id]['0'] = list()
                suncg_splits['val'][scene_id]['0'].append(
                    os.path.join(suncg_path, rendered_image)
                )
        else:
            if scene_id in suncg_splits['train']:
                suncg_splits['train'][scene_id]['0'].append(
                    os.path.join(suncg_path, rendered_image)
                )
            elif scene_id in suncg_splits['test']:
                suncg_splits['test'][scene_id]['0'].append(
                    os.path.join(suncg_path, rendered_image)
                )
            elif scene_id in suncg_splits['val']:
                suncg_splits['val'][scene_id]['0'].append(
                    os.path.join(suncg_path, rendered_image)
                )
            else:
                print("An error has occured with SunCG scene id: {}".format(scene_id))
    return suncg_splits

def dump_splits(splits, args, outliers):
    split_names = ['train', 'test', 'val']
    for name in split_names:
        with open(os.path.join(args.outliers_path, "{}_{}.txt".format(args.name, name)), 'w') as out:
            for split in splits:
                for scene_key, scene_list in split[name].items():
                    for pose_key, pose_files in scene_list.items():
                            sorted_split = sorted(pose_files)
                            filenames_sorted_split = [os.path.basename(s) for s in sorted_split]

                            if outliers.isdisjoint(filenames_sorted_split):
                                line = " ".join(sorted_split)
                                out.writelines([line, "\n"])
 
def create_outliers_list(outliers_files_list):
    outliers = []
    for of in outliers_files_list:    
        with open(of, mode='r') as outlier_file:
            csv_reader = csv.reader(outlier_file)
            next(csv_reader, None)  # skip the headers
            for row in csv_reader:
                outliers.extend([row[0]])
    return set(outliers)

if __name__ == "__main__":
    args, unknown = parse_arguments(sys.argv)
    splits = list()
    ''' Matterport3D '''
    if 'm3d_path' in args:
        m3d_splits = create_m3d_splits(args.m3d_path)
        splits.append(m3d_splits)
    ''' Stanford2D3D '''
    if 's2d3d_path' in args:
        s2d3d_splits = create_s2d3d_splits(args.s2d3d_path)
        splits.append(s2d3d_splits)
    ''' SunCG '''
    if 'suncg_path' in args:
        suncg_splits = create_suncg_splits(args.suncg_path)
        splits.append(suncg_splits)
    outliers = create_outliers_list([
        os.path.join(args.outliers_path, 'm3d_outliers.csv'),
        os.path.join(args.outliers_path, 's2d3d_outliers.csv'),
        os.path.join(args.outliers_path, 'scg_outliers.csv')])
    if len(splits) > 0:
        dump_splits(splits, args, outliers)