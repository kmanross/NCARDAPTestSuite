#!/bin/sh

# Using NCO 4.2.3 <http://nco.sourceforge.net/>
# Replace USERNAME and PASSWORD with your credentials making sure to use
# %40 instead of @ in the username: manross@ucar.edu should be manross%40ucar.edu

### Print some global variables
ncks -M -p http://USERNAME:PASSWORD@castle.ucar.edu/thredds/dodsC/FNLCollection/ best

### Get CAPE over CONUS for a period in May/Jun 2013 and dump to file
### Note: timesteps are integers. Values here are a guess
ncks -d lat,23.,51. -d lon,233.,310. -d time,20000,20268 -v Convective_available_potential_energy_surface -p http://USERNAME:PASSWORD@castle.ucar.edu/thredds/dodsC/FNLCollection best fullbest_CONUS_mayjuneish2013.nc


