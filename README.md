A generator level simulation to create and plot data related to K0sK0s -> pi+pi-pi+pi- events resulting from double pomeron exchanges.

To change data generation parameters such as number of events to be generated without editing the python file, a user can make edits to mymain04.cmnd. See
the Pythia8 documentation on command files for more information.

To install, use the following steps:
  1. Install Pythia8 according to documentation found at http://home.thep.lu.se/Pythia/
  2. Download and unzip repository files
  3. Move unzipped files to the examples folder Pythia8 directory
  
******************************************
Functionality
******************************************
While in the Pythia8 examples directory:

  Data generation: python2.7 mymain04.py
  
  Create histograms from data: python2.7 sim_hists.py
