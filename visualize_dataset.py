import ThreeD60
import visualization

from torch.utils.data import DataLoader

if __name__ == "__main__":
    datasets = ThreeD60.get_datasets(".//splits//3D60_train.txt", \
        datasets=["suncg", "m3d", "s2d3d"],        
        placements=[ThreeD60.Placements.CENTER, ThreeD60.Placements.RIGHT, ThreeD60.Placements.UP],
        image_types=[ThreeD60.ImageTypes.COLOR, ThreeD60.ImageTypes.DEPTH, ThreeD60.ImageTypes.NORMAL], longitudinal_rotation=True)
    print("Loaded %d samples." % len(datasets))
    
    viz = visualization.VisdomImageVisualizer("3D60", "127.0.0.1")
    dataset_loader = DataLoader(datasets, batch_size=32, shuffle=True, pin_memory=False, num_workers=4)
    for i, b in enumerate(dataset_loader):
        viz.show_images_grid(ThreeD60.extract_image(b, ThreeD60.Placements.CENTER, ThreeD60.ImageTypes.COLOR), "all_colors")
        viz.show_depths_grid(ThreeD60.extract_image(b, ThreeD60.Placements.CENTER, ThreeD60.ImageTypes.DEPTH), "all_depths")
        viz.show_normals_grid(ThreeD60.extract_image(b, ThreeD60.Placements.CENTER, ThreeD60.ImageTypes.NORMAL), "all_normals")
