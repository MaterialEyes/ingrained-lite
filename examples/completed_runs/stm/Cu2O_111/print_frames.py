import sys
sys.path.append('../../../../')
import numpy as np
import matplotlib.pyplot as plt
import ingrained.image_ops as iop
from ingrained.utilities import print_frames

# Read image data
image_data = iop.image_open('03h_Cu2O_111_034_fwd_z_plane.txt')

# Read the experimental image and preprocess
exp_img = image_data['Pixels'][220:370,140:290]

# Print the first 25 frames to file
print_frames(config_file='Cu2O_111_PARCHG', exp_img=exp_img, exp_title="Cu$_{2}$O(111)", progress_file="progress.txt", frame_selection="1-25", search_mode="stm", cmap="hot")

# Print the best frame to file
print_frames(config_file='Cu2O_111_PARCHG', exp_img=exp_img, exp_title="Cu$_{2}$O(111)", progress_file="progress.txt", frame_selection="best", search_mode="stm", cmap="hot")