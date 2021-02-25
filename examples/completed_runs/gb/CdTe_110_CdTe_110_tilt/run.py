import sys
sys.path.append('../../../../')
import numpy as np
import ingrained.image_ops as iop
import matplotlib.pyplot as plt
from ingrained.structure import Bicrystal
from ingrained.optimize import CongruityBuilder

# Read image data
image_data = iop.image_open('HAADF149.dm3')

# Constrain optimization to clean region of image by cropping
exp_img = image_data['Pixels'][0:470,0:470]

# View the image before proceeding with optimization
plt.imshow(exp_img,cmap='gray'); plt.axis('off'); plt.show();

# Initialize a Bicrystal object and save the constructed bicrystal structure
bicrystal = Bicrystal(config_file='config.json', write_poscar=True);

# Initialize a ConguityBuilder with the Bicrystal and experimental image
congruity = CongruityBuilder(sim_obj=bicrystal, exp_img=exp_img);

# Define initial set of input parameters for an image simulation
pix_size          = image_data["Experiment Pixel Size"]        
interface_width   = 0.00
defocus           = 1.00
x_shear           = 0.00
y_shear           = 0.00
x_stretch         = 0.00
y_stretch         = 0.00
crop_height       = 301
crop_width        = 161

sim_params = [pix_size, interface_width, defocus, x_shear, y_shear, x_stretch, y_stretch, crop_height, crop_width]

# Find correspondence!
congruity.find_correspondence(objective='taxicab_ssim', initial_solution=sim_params, search_mode="gb")