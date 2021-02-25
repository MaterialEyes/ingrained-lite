import sys
sys.path.append('../../../../')
import numpy as np
import matplotlib.pyplot as plt
import ingrained.image_ops as iop
from ingrained.structure import Bicrystal
from ingrained.optimize import CongruityBuilder

# Read image data
image_data = iop.image_open('HAADF91.tif')

# Constrain optimization to clean region of image by cropping
exp_img = iop.apply_rotation(image_data['Pixels'][380:-240,370:-30],-2.3)

# View the image before proceeding with optimization
plt.imshow(exp_img,cmap='gray'); plt.axis('off'); plt.show();

# # Initialize a Bicrystal object and save the constructed bicrystal structure
# bicrystal = Bicrystal(config_file='config.json', write_poscar=True);

# Initialize a Bicrystal object and save the constructed bicrystal structure
bicrystal = Bicrystal(poscar_file='bicrystal.POSCAR.vasp');

# Initialize a ConguityBuilder a Bicrystal and experimental image
congruity = CongruityBuilder(sim_obj=bicrystal, exp_img=exp_img);

# Input parameters to optimize for an image simulation:
pix_size          = 0.125
interface_width   = 0.00
defocus           = 1.00
x_shear           = 0.00
y_shear           = 0.00
x_stretch         = 0.00
y_stretch         = 0.00
crop_height       = 285
crop_width        = 171

sim_params = [pix_size, interface_width, defocus, x_shear, y_shear, x_stretch, y_stretch, crop_height, crop_width]

# Find correspondence!
congruity.find_correspondence(objective='taxicab_ssim', initial_solution=sim_params, search_mode="gb")
