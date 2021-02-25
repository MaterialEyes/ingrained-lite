import sys
sys.path.append('../../../../')
import numpy as np
import ingrained.image_ops as iop
import matplotlib.pyplot as plt
from ingrained.structure import PartialCharge
from ingrained.optimize import CongruityBuilder

# Read image data
image_data = iop.image_open('03h_Cu2O_111_034_fwd_z_plane.txt')

# Constrain optimization to clean region of image by cropping
exp_img = image_data['Pixels'][220:370,140:290]

# Read pixel value (CAUTION: be skeptical of rescaling and local imaging distorions)
exp_pix_size = image_data["Experiment Pixel Size"]
print("Experiment Pixel Size: {} (Å)".format(exp_pix_size))

# Display the experimental STM image
plt.imshow(exp_img,cmap='hot'); plt.axis('off'); plt.show();

# Initialize a PartialCharge object with the path to the PARCHG file
parchg = PartialCharge(filename='Cu2O_111_PARCHG');

# Initialize a ConguityBuilder with PARCHG and experimental image
congruity = CongruityBuilder(sim_obj=parchg, exp_img=exp_img);

# Input parameters to optimize for an image simulation:
z_below     = 1
z_above     = 1
r_val       = 0.016
r_tol       = 0.015
x_shear     = 0.00
y_shear     = 0.00
x_stretch   = 0.00
y_stretch   = 0.00
rotation    = 110
pix_size    = 0.27
sigma       = 0
crop_height = 101
crop_width  = 101

sim_params = [z_below, z_above, r_val, r_tol, x_shear, y_shear, x_stretch, y_stretch, rotation, pix_size, sigma, crop_height, crop_width]

# Find correspondence!
congruity.find_correspondence(objective='taxicab_ssim', initial_solution=sim_params, search_mode="stm")