import sys
sys.path.append('../../../../')
import numpy as np
import matplotlib.pyplot as plt
import ingrained.image_ops as iop
from ingrained.structure import Bicrystal
from ingrained.optimize import CongruityBuilder

# Read image data
image_data = iop.image_open('HAADF26.dm3')

# Constrain optimization to clean region of image by cropping
exp_img = np.fliplr(iop.apply_crop(iop.apply_rotation(image_data['Pixels'],66),328,328)[:-26,:-26])

# View the image before proceeding with optimization
plt.imshow(exp_img,cmap='gray'); plt.axis('off'); plt.show();

# Initialize a Bicrystal object with the path to the slab json file
bicrystal = Bicrystal(config_file='config.json', write_poscar=True);

# Initialize a ConguityBuilder with a Bicrystal and experimental image
congruity = CongruityBuilder(sim_obj=bicrystal, exp_img=exp_img);

# Input parameters to optimize for an image simulation:
pix_size          = image_data["Experiment Pixel Size"]+0.005
interface_width   = 0.20
defocus           = 1.25
x_shear           = 0.00
y_shear           = 0.00
x_stretch         = 0.00
y_stretch         = 0.00
crop_height       = 201
crop_width        = 167

sim_params = [pix_size, interface_width, defocus, x_shear, y_shear, x_stretch, y_stretch, crop_height, crop_width]

# Find correspondence!
congruity.find_correspondence(objective='taxicab_ssim', initial_solution=sim_params, search_mode="gb")