import sys
sys.path.append('../../../../')
import numpy as np
import matplotlib.pyplot as plt
import ingrained.image_ops as iop
from ingrained.utilities import print_frames

# Read image data
image_data = iop.image_open('HAADF91.tif')

# Read the experimental image and preprocess
exp_img = iop.apply_rotation(image_data['Pixels'][380:-240,370:-30],-2.3)

# Print the first 5 frames to file
print_frames(config_file='config.json', exp_img=exp_img, exp_title="M$_{3}$B$_{2}$ in Ni matrix [001]$_{_{M_{3}B_{2}}}//$[001]$_{_{Ni}}$", progress_file="progress.txt", frame_selection="1-5", search_mode="gb", cmap="gray")

# Print the best frame to file
print_frames(config_file='config.json', exp_img=exp_img, exp_title="M$_{3}$B$_{2}$ in Ni matrix [001]$_{_{M_{3}B_{2}}}//$[001]$_{_{Ni}}$", progress_file="progress.txt", frame_selection="best", search_mode="gb", cmap="gray")