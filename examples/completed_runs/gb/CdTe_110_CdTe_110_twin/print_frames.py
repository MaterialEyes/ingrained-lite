import sys
sys.path.append('../../../../')
import numpy as np
import matplotlib.pyplot as plt
import ingrained.image_ops as iop
from ingrained.utilities import print_frames

# Read image data
image_data = iop.image_open('HAADF26.dm3')

# Read the experimental image and preprocess
exp_img = np.fliplr(iop.apply_crop(iop.apply_rotation(image_data['Pixels'],66),328,328)[:-26,:-26])

# Print the first 5 frames to file
print_frames(config_file='config.json', exp_img=exp_img, exp_title="CdTe coherent {111} twin boundary", progress_file="progress.txt", frame_selection="1-8", search_mode="gb", cmap="gray")

# Print the best frame to file
print_frames(config_file='config.json', exp_img=exp_img, exp_title="CdTe coherent {111} twin boundary", progress_file="progress.txt", frame_selection="best", search_mode="gb", cmap="gray")