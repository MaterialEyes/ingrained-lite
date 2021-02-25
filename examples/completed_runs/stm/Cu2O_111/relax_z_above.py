import sys
sys.path.append('../../../../')
import numpy as np
import ingrained.image_ops as iop
import matplotlib.pyplot as plt
from ingrained.structure import PartialCharge
from ingrained.optimize import CongruityBuilder

"""
This script will reduce the the z_above value incrementally until it negatively affects the FOM.
z_above acts as a free variable once it exceeds the top of the charge surface and optimization may 
make this value arbitarily high when the best solution is at the top of the surface. 
"""

# Get solutions from text file
progress = np.genfromtxt("progress.txt", delimiter=',')
best_idx = int(np.argmin(progress[:,-1]))
x = progress[best_idx][1:-1]
x = [a for a in x[:-2]] + [int(a) for a in x[-2::]]

# Read image data
image_data = iop.image_open('03h_Cu2O_111_034_fwd_z_plane.txt')

# Constrain optimization to clean region of image by cropping
exp_img = image_data['Pixels'][220:370,140:290]

# # Initialize a PartialCharge object with the path to the PARCHG file
parchg = PartialCharge(filename='Cu2O_111_PARCHG');

# # Initialize a ConguityBuilder with PARCHG and experimental image
congruity = CongruityBuilder(sim_obj=parchg, exp_img=exp_img, iter=int(progress[-1,0]+1));

decimp = [1,1E-1,1E-2,1E-3,1E-4,1E-5,1E-6,1E-7,1E-8]

final_fom = congruity.taxicab_ssim_objective(x=x)
for d in decimp:
	for val in np.arange(0,10,d):
		x[1] = x[1] - val
		fom = congruity.taxicab_ssim_objective(x=x)
		if fom > final_fom:
			x[1] = x[1] + val
			break
congruity.taxicab_ssim_objective_gb(x=x)
print("Relaxed z_above solution: ",x)