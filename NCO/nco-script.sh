#!/bin/sh

# Using NCO 4.2.3 <http://nco.sourceforge.net/>
# Replace USERNAME and PASSWORD with your credentials making sure to use
# %40 instead of @ in the username: manross@ucar.edu should be manross%40ucar.edu

ncks -M -p http://USERNAME:PASSWORD@castle.ucar.edu/thredds/dodsC/FNLCollection/ best

