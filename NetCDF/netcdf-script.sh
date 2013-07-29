#!/bin/sh

# Using NetCDF 4.2 (built Aug 2012) <http://www.unidata.ucar.edu/software/netcdf/>
# Replace USERNAME and PASSWORD with your credentials making sure to use
# %40 instead of @ in the username: manross@ucar.edu should be manross%40ucar.edu

ncdump -h http://USERNAME:PASSWORD@castle.ucar.edu/thredds/dodsC/ds083.2/best

