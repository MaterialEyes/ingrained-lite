import sys
sys.path.append('../../../../')
import numpy as np
import matplotlib.pyplot as plt
import ingrained.image_ops as iop
from ingrained.utilities import print_frames

# Read image data
image_data = iop.image_open('HAADF149.dm3')

# Read the experimental image and preprocess
exp_img = image_data['Pixels'][0:470,0:470]

# Print the first 5 frames to file
print_frames(config_file='config.json', exp_img=exp_img, exp_title="CdTe [110]//[110] (MO = 82°)", progress_file="progress.txt", frame_selection="1-8", search_mode="gb", cmap="gray")

# Print the best frame to file
print_frames(config_file='config.json', exp_img=exp_img, exp_title="CdTe [110]//[110] (MO = 82°)", progress_file="progress.txt", frame_selection="best", search_mode="gb", cmap="gray")