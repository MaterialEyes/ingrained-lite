![image](https://drive.google.com/uc?export=view&id=1H3PYFTqZpiytEAR4KFbFV_7U2bKUWyUV)

| :hammer_and_pick:| An automated framework for fusing materials imaging simulations into experiments. |
|---------------|:------------------------|

## Current features
Grain boundary structure initialization from atomic-resolution HAADF STEM imaging ([CdTe [110]-[110] tilt grain boundary](https://aip.scitation.org/doi/10.1063/1.5123169))

<img src="https://drive.google.com/uc?export=view&id=1UpoiBue9R7rgBNWvk584Ozc85luHSY7Y" alt="alt text" width="704" height="260">
  
STM structure validation from simulated images of partial charge densities volumes from DFT-simulation ([Cu<sub>2</sub>O(111)](https://pubs.rsc.org/en/content/articlelanding/2018/cp/c8cp06023a#!divAbstract))

<img src="https://drive.google.com/uc?export=view&id=1C46_e0WO0ajaQ_ON_EWi9tZeL_RNjcJ8" alt="alt text" width="704" height="260">


## Getting started
  
### Requirements
To install *ingrained*, you need:
  * python 3.x 
  * a conda package manager to configure the basic installation environment
  * [Materials Project API key](https://materialsproject.org/open)

### Installation
The following will install a local copy of *ingrained* and create a custom [conda](https://docs.conda.io/en/latest/) development environment for both STEM and STM functionalities.

Clone this repo and navigate to the root directory:
```sh
git clone https://github.com/MaterialEyes/ingrained
cd ingrained
```
Create the environment from the <code>environment.yml</code> file and activate it:
```sh
conda env create -f utils/environment.yml
conda activate ingrained
```
Set your [Materials Project API key](https://materialsproject.org/open) "MAPI_KEY" environment variable:
```python
./utils/set_key.sh mYaPiKeY
```
Install additional (external) packages to parse standard experimental files (i.e. dm3, sxm, etc...)
```sh
./utils/install_parsers.sh
```
## *ingrained* workflow
1. Isolate a clean region of an experimental image, and preprocess if necessary (*i.e. Wiener filter, contrast enhancement, etc.*)
2. Initialize a *structure* object from an appropriate classes in [structure.py](https://github.com/MaterialEyes/ingrained/blob/master/ingrained/structure.py). For grain boundaries, a <code>Bicrystal()</code> object requires a path to a configuration file, <code>config.json</code>. For STM structure validation, a <code>PartialCharge()</code> object requires a path to a <code>PARCHG</code> file.
3. Initialize an *optimize* object from the <code>ConguityBuilder()</code> class in [optimize.py](https://github.com/MaterialEyes/ingrained/blob/master/ingrained/optimize.py), by passing in the current *structure* object and the prepared experimental image.
4. Run the optimization by calling the <code>find_correspondence</code> method of the <code>ConguityBuilder()</code>, with a *reasonable* initial set of input parameters. Better initial approximations often lead to better final solutions!

## Examples

The [clean_templates](https://github.com/MaterialEyes/ingrained/tree/master/examples/clean_templates) folder in the examples directory provides a collection of minimal working examples. For the full examples containing structures and record of the optimization progress (as outlined in the [paper](https://)), refer to the [completed_runs](https://github.com/MaterialEyes/ingrained/tree/master/examples/completed_runs) folder.

### Ex. 1: Grain boundary structure initialization from HAADF STEM

Here, we outline the contents of the [example](https://github.com/MaterialEyes/ingrained/tree/master/examples/completed_runs/gb/CdTe_110_CdTe_110_tilt) given for a [CdTe [110]-[110] tilt grain boundary](https://aip.scitation.org/doi/10.1063/1.5123169) structure 

(1) Experimental target image ([HAADF149.dm3](https://github.com/MaterialEyes/ingrained/blob/master/examples/completed_runs/gb/CdTe_110_CdTe_110_tilt/HAADF149.dm3)).

<img src="https://drive.google.com/uc?export=view&id=19OdPSowDw4k2O5oEn5u9h7OjPliSQqE6" alt="alt text" width="300" height="319">

(2) Configuration file ([config.json](https://github.com/MaterialEyes/ingrained/blob/master/examples/completed_runs/gb/CdTe_110_CdTe_110_tilt/config.json)) to specify parameters and settings for bicrystal crystal construction.
```
{
	"slab_1":{
		"chemical_formula":"CdTe",
		"space_group":"F-43m",
		"uvw_project":[1,1,0],
		"uvw_upward":[-1,1,0],
		"tilt_angle":8,
		"max_dimension":40,
		"flip_species":false
	},
	"slab_2":{
		"chemical_formula":"CdTe",
		"space_group":"F-43m",
		"uvw_project":[1,1,0],
		"uvw_upward":[0,0,1],
		"tilt_angle":0,
		"max_dimension":40,
		"flip_species":false
	},
	"constraints":{
		"min_width":30,
		"max_width":60,
		"min_depth":8,
		"max_depth":20,
		"interface_1_width": 0,
		"interface_2_width": 0,
		"collision_removal":[true,true],
		"pixel_size":0.16388347372412682
	},
	"structure_file": "bicrystal.POSCAR.vasp" (OPTIONAL - include only if bicrystal structure already exists!)
}
```
Summary of configuration parameters:
> *slab parameters*
> -  chemical_formula: An element or compound describing the composition of the bulk.
> -  space_group: The symmetry group of the configuration
> -  uvw_project: The direction of projection (screen to viewer) as a lattice vector, ua + vb + wc
> -  uvw_upward: The upward direction is a lattice vector ua + vb + wc (must be normal to uvw_project).
> -  tilt_ang: The CCW rotation around 'uvw_project' (applied after uvw_upward is set)
> -  max_dimension: The maximum edge length along any dimension (Å)
> -  flip_species: Only applies for compounds containing two chemical elements, will swap chemical identities for all elements

> *construction parameters*
> -  min/max width: bounds on width in imaging plane (Å)
> -  min/max depth: bounds on depth along imaging axis (Å)
> -  interface_1_width: spacing between max position of bottom grain and min position of top grain (Å)
> -  interface_2_width: spacing between max position of top grain and min position of bottom grain (Å)
> -  collision_removal: remove atoms closer than 1Å in distance within a in volume around [interface_1,interface_2]
> -  pixel_size: pixel size of experimental image (check <code>iop.image_open(image_file)["Experiment Pixel Size"]</code>)

> *optional*
> -  structure_file: bypass the construction and initialize <code>Bicrystal()</code> object with existing structure

(3) Python script to execute steps of the *ingrained* workflow ([run.py](https://github.com/MaterialEyes/ingrained/blob/master/examples/completed_runs/gb/CdTe_110_CdTe_110_tilt/run.py)).
```python

import sys
sys.path.append('../../../../')
import matplotlib.pyplot as plt
import ingrained.image_ops as iop
from ingrained.structure import Bicrystal
from ingrained.optimize import CongruityBuilder

# Read image data
image_data = iop.image_open('HAADF149.dm3')

# Constrain optimization to clean region of image by cropping
exp_img = image_data['Pixels'][0:470,0:470]

# View the image before proceeding with optimization
plt.imshow(exp_img, cmap='gray'); plt.axis('off'); plt.show();

# Initialize a Bicrystal object and save the constructed bicrystal structure
bicrystal = Bicrystal(filename='config.json', write_poscar=True);

# Initialize a ConguityBuilder with bicrystal and experimental image
congruity = CongruityBuilder(sim_obj=bicrystal, exp_img=exp_img);

# Input parameters to optimize for an image simulation:
pix_size        =  image_data["Experiment Pixel Size"]        
interface_width =  0.00
defocus         =  1.50
x_shear         =  0.00
y_shear         =  0.00
x_stretch       =  0.00
y_stretch       =  0.00
crop_height     =  289
crop_width      =  161

sim_params = [pix_size, interface_width, defocus, x_shear, y_shear, x_stretch, y_stretch, crop_height, crop_width]

# Find correspondence (supports 'Powell' and 'COBYLA' methods from scipy.optimize.minimize)
congruity.find_correspondence(objective='taxicab_ssim', optimizer='Powell', initial_solution=sim_params, search_mode="gb")
```
Summary of optimization parameters:
> -  pix_size: real-space pixel size (Å).
> -  interface_width: spacing between max position of bottom grain and miniumum position of top grain (Å)
> -  defocus: controls degree to which edges blur in microscopy image (Å)
> -  x_shear: fractional amt shear in x (+ to the right)
> -  y_shear: fractional amt shear in y (+ up direction)
> -  x_stretch: fractional amt stretch (+) or compression (-) in x
> -  y_stretch: fractional amt stretch (+) or compression (-) in y
> -  crop_height: final (cropped) image height in pixels
> -  crop_width: final (cropped) image width in pixels

### Ex. 2: STM structure validation from simulated PARCHG images

Here, we outline the contents of the [example](https://github.com/MaterialEyes/ingrained/tree/master/examples/completed_runs/stm/Cu2O_111) given for a [Cu<sub>2</sub>O(111)](https://pubs.rsc.org/en/content/articlelanding/2018/cp/c8cp06023a#!divAbstract) surface

(1) Experimental target image (cropped) ([03h_Cu2O_111_034_fwd_z_plane.txt](https://github.com/MaterialEyes/ingrained/tree/master/examples/completed_runs/stm/03h_Cu2O_111_034_fwd_z_plane.txt)).

<img src="https://drive.google.com/uc?export=view&id=1XTzx4OEc_Ljy4L9-HZvyUGEaAnBD888Y" alt="alt text" width="300" height="319">

(2) Configuration file ([PARCHG](https://github.com/MaterialEyes/ingrained/tree/master/examples/completed_runs/stm/Cu2O_111/parchg_download.sh)) which provides the partial charge densities from a DFT-simulation.

This file will need to be downloaded, as it is not stored in the repo.
```sh
bash parchg_download.sh 
```

(3) Python script to execute steps of the *ingrained* workflow ([run.py]()).
```python

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

# Display the experimental STM image
plt.imshow(exp_img,cmap='hot'); plt.axis('off'); plt.show();

# Initialize a PartialCharge object with the path to the PARCHG file
parchg = PartialCharge(filename='PARCHG_with_Cu_cus_modelA_P1_stm1.5');

# Initialize a ConguityBuilder with PARCHG and experimental image
congruity = CongruityBuilder(sim_obj=parchg, exp_img=exp_img);

# Input parameters to optimize for an image simulation:
z_below     = 2
z_above     = 12
r_val       = 0.27
r_tol       = 0.24
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

# Find correspondence (supports 'Powell' and 'COBYLA' methods from scipy.optimize.minimize)
congruity.find_correspondence(objective='taxicab_ssim', optimizer='Powell', initial_solution=sim_params, search_mode="stm")
```
Summary of optimization parameters:
> -  z_below: thickness or depth from top in (Å)
> -  z_above: distance above the surface to consider (Å)
> -  r_val: isosurface charge density plane
> -  r_tol: tolerance to consider while determining isosurface
> -  x_shear: fractional amt shear in x (+ to the right)
> -  y_shear: fractional amt shear in y (+ to the right)
> -  x_stretch: fractional amt stretch (+) or compression (-) in x
> -  y_stretch: fractional amt stretch (+) or compression (-) in y
> -  rotation: image rotation angle (in degrees) (+ is CCW)
> -  pix_size: real-space pixel size (Å).
> -  sigma: std. deviation for gaussian kernel used in postprocessing
> -  crop_height: final (cropped) image height in pixels
> -  crop_width: final (cropped) image width in pixels

(4) Python script for final relaxation of <code>z_above</code> parameter ([relax_z_above.py](https://github.com/MaterialEyes/ingrained/tree/master/examples/completed_runs/stm/Cu2O_111/relax_z_above.py))

Run only after <code>find_correspondence</code> has completed. Currently, <code>z_above</code> acts as a free variable 
once it exceeds the top of the charge surface, and optimization may make this value arbitarily high when the best solution 
is at the top of the surface. This function ensures that <code>z_above</code> represents a physically meaningful distance 
(Å) above the surface.

### Output

Execution of the sequence outlined in [run.py]() will produce:
 * [bicrystal.POSCAR.vasp](https://github.com/MaterialEyes/ingrained/blob/master/examples/completed_runs/gb/CdTe_110_CdTe_110_tilt/HAADF149.POSCAR.vasp) - (Ex. 1 only) a POSCAR of the newly constructed bicrystal  
 * [strain_info.txt](https://github.com/MaterialEyes/ingrained/blob/master/examples/completed_runs/gb/CdTe_110_CdTe_110_tilt/strain_info) - (Ex. 1 only) record of the amount of strain in each bicrystal grain (given as % along width and depth)
 * [progress.txt](https://github.com/MaterialEyes/ingrained/blob/master/examples/completed_runs/gb/CdTe_110_CdTe_110_tilt/progress.txt) - record of the optimization solution and the respective figure-of-merit (FOM) at each optimization step.

Additional tools are included to view and write optimization progress to a movie 
* [print_frames.py](https://github.com/MaterialEyes/ingrained/blob/master/examples/completed_runs/gb/CdTe_110_CdTe_110_tilt/print_frames.py) - writes specified optimization steps (frames) to custom image panels (.png)
* [make_movie.sh](https://github.com/MaterialEyes/ingrained/blob/master/examples/completed_runs/gb/CdTe_110_CdTe_110_tilt/make_movie.sh) - wrapper around [FFmpeg](https://ffmpeg.org/) to create a movie from the sequence of panels created in [print_frames.py](https://github.com/MaterialEyes/ingrained/blob/master/examples/completed_runs/gb/CdTe_110_CdTe_110_tilt/print_frames.py)

Make adjustments to the <code>frame_selection</code> argument passed to [print_frames.py](https://github.com/MaterialEyes/ingrained/blob/master/examples/completed_runs/gb/CdTe_110_CdTe_110_tilt/print_frames.py) to customize the output, or just choose "all" to print all steps of the optimization. With the frames printed, make a movie outlining the progress by simply running:

```sh
bash make_movie.sh
```
## Future Development
- [ ] Implement additional image similarity measurements (i.e. VIFP, etc).
- [ ] Cutoff <code>z_above</code> parameter in [PartialCharge()](https://github.com/MaterialEyes/ingrained/blob/master/ingrained/structure.py) when it extends beyond height of charge surface.
- [ ] Consolidate configuration and optimization parameters to improve automation.
- [ ] Work to speedup bicrystal construction.
- [ ] Create Python package.

## Citation
If you find this code useful, please consider citing our [paper](#paper)
```sh
@article{,
  title={},
  author={},
  journal={},
  volume={},
  number={},
  pages={},
  year={},
  publisher={}
}
```

## Acknowledgements <a name="credits"></a>
This material is based upon work supported by Laboratory Directed Research and Development (LDRD) funding from Argonne National Laboratory, provided by the Director, Office of Science, of the U.S. Department of Energy under Contract No. DE-AC02-06CH11357

This work was performed at the Center for Nanoscale Materials, a U.S. Department of Energy Office of Science User Facility, and supported by the U.S. Department of Energy, Office of Science, under Contract No. DE-AC02-06CH11357.

We gratefully acknowledge the computing resources provided on Bebop, a high-performance computing cluster operated by the Laboratory Computing Resource Center at Argonne National Laboratory.

## License <a name="license"></a>
