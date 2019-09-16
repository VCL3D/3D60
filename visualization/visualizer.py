import visdom
import numpy
import torch
import torchvision
import matplotlib.pyplot as plt

class VisdomImageVisualizer(object):
    def __init__(self, name, server="http://localhost", count=2):
        self.name = name
        self.server = server
        self.count = count
        self.visualizer = visdom.Visdom(server=self.server, port=8097,\
            env=self.name, use_incoming_socket=False)   

    def show_images_grid(self, images, title):        
        grid = torchvision.utils.make_grid(images)
        c, h, w = grid.size()
        scale_factor = 4
        opts = (
        {
            'title': title, 'width': w // scale_factor, 'height': h // scale_factor
        })
        self.visualizer.image(grid, opts=opts, win=title)

    def show_depths_grid(self, depths, title):
        b, c, h, w = depths.size()
        depths[torch.isinf(depths)] = 0.0
        canvas = torch.zeros(b, 3, h, w)        
        for i in range(b):
            array = depths[i, :, :, :].cpu().numpy().transpose(1, 2, 0)
            cmap = plt.cm.magma
            norm = plt.Normalize(vmin=0.0, vmax=7.5)
            image = cmap(norm(array)).transpose(3, 2, 0, 1).reshape(4, h, w)
            canvas[i, :, :, :] = torch.from_numpy(image)[:3, :, :].float()
        grid = torchvision.utils.make_grid(canvas)
        c, h, w = grid.size()
        scale_factor = 4
        opts = (
        {
            'title': title, 'width': w // scale_factor, 'height': h // scale_factor
        })
        self.visualizer.image(grid, opts=opts, win=title)

    
    def show_normals_grid(self, normals, title):
        normals[torch.isnan(normals)] = 0.0
        normals = torch.clamp(normals, min=-1.0, max=1.0)
        grid = torchvision.utils.make_grid(normals, \
            normalize=True, range=(-1.0, 1.0), scale_each=True)
        _, h, w = grid.size()
        opts = (
        {
            'title': title, 'width': w // 4, 'height': h // 4
        })
        self.visualizer.image(grid, opts=opts, win=title)

    def show_images(self, images, title):
        b, c, h, w = images.size()
        take = min(b, self.count)
        recon_images = images.detach().cpu()[:take, [2, 1, 0], :, :]\
            if c == 3 else\
            images.detach().cpu()[:take, :, :, :]
        opts = (
        {
            'title': title, 'width': take / 2 * 512,
            'height': take / 4 * 256
        })
        self.visualizer.images(recon_images, opts=opts,\
            win=self.name + title + "_window")

    def show_map(self, maps, title):
        b, c, h, w = maps.size()        
        maps_cpu = torch.flip(maps, dims=[2]).detach().cpu()[:self.count, :, :, :]
        for i in range(min(b, self.count)):
            opts = (
            {
                'title': title + str(i), 'colormap': 'Viridis'
            })
            heatmap = maps_cpu[i, :, :, :].squeeze(0)
            #TODO: flip images before heatmap call
            self.visualizer.heatmap(heatmap,\
                opts=opts, win=self.name + title + "_window_" + str(i))     