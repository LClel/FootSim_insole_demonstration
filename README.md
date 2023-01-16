<<<<<<< HEAD
# FootSim_insole_demonstration
## Code and data used to simulate tactile responses to steps in "Modelling foot sole cutaneous afferents (FootSim)" (Katic et al. (2023), iScience, 105874-105874)
=======
# FootSim insole demonstration
## Code and data used to simulate tactile responses to steps in "Modelling foot sole cutaneous afferents (FootSim)" (Katic et al., under review, iScience)
>>>>>>> 840a9ca5caf030c9154cf828f7fd3c77b6f9b032

The code used within this mini-repository builds upon that in FootSim (https://github.com/ActiveTouchLab/footsim-python) to simulate tactile responses to walking

The data used within this simulations is part of a larger project, titled "Complexity of spatiotemporal plantar pressure patterns during everyday behaviours" (Cleland et al., in prep.). Further data and code related to this project can be found at https://github.com/LClel/project_insole. To generate the files in `preprocessed_data`, the pipeline run within https://github.com/LClel/project_insole will need to be run.

To run this code, you will need to have FootSim installed and a virtual environment set up. Instructions on how to do this can be found at https://github.com/ActiveTouchLab/footsim-python. All dependencies are included within the main FootSim package.

### This repository contains:
* `/data` - raw data files
* `/processed_data` - processed data that can be loaded in to generate only the figures
* `/code` - the code used to generate figures
     - `/insole.py`- code used to map raw data onto the foot
     - `/spatial_plots.py` - code used to generate and save spatial plots of Stimulus and Response objects onto the foot
     - `/population_and_plots.py` - code used to generate and save population responses across the entire foot and specific regions as a lineplot
     - `functions.py` - plotting functions
* `/figures` - figures generated using the code

## Questions?
Questions, comments and suggestions regarding simulations of walking using FootSim can be directed to Luke Cleland at ldcleland1@sheffield.ac.uk from https://activetou.ch.
