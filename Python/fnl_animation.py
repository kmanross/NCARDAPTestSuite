#!/bin/env python

import sys
import argparse
from datetime import datetime,timedelta, time
import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma
from datetime import datetime,timedelta, time
from mpl_toolkits.basemap import Basemap, shiftgrid
from scipy.ndimage.filters import minimum_filter, maximum_filter
from netCDF4 import Dataset as NetCDFFile, date2index, num2date
import matplotlib.animation as animation




#import inspect
#c=inspect.currentframe()


class ani:
    startdate = None
    enddate = None
    data = None
    dates = None
    fig = None
    CS1 = None
    CS2 = None
    Q = None
    m = None
    longitudes = None
    latitudes = None
    slp = None
    u = None
    v = None
    txt = None
    lons = None
    lats = None
    x = None
    y = None
    clevs = None
    plotarrows = False


    def __init__(self, *args, **kwargs):
        #self.args(args, kwargs)
        rgs = self.args(args)

        baseurl = '@castle.ucar.edu:8443/thredds/dodsC/FNLCollection/best'
        URL = 'https://' + self.uname(rgs.username) + ':' + rgs.password +  baseurl
        try:
            self.data = NetCDFFile(URL)
        except:
            raise IOError('opendap server not providing the requested data')

        self.setupmap()
        if len(self.dates) > 1:
            a = animation.FuncAnimation(self.fig,self.updatefig,frames=len(self.dates))
        plt.show()


    def uname(self,u):
        return u.replace('@','%40')

    def args(self, *args, **kwargs):
        parser = argparse.ArgumentParser()
        parser.add_argument("username", help="username for accessing NCAR RDA")
        parser.add_argument("password", help="password or accessing NCAR RDA")
        parser.add_argument("date", help="Enter date *ON or AFTER* 00z on 08/14/1999\
                             Format = YYYYmmdd\nEg., 20130401")
        parser.add_argument("hour", help="valid hours are 00, 06, 12, or 18")
        parser.add_argument('-ed', '--enddate',\
                             help="OPTIONAL end date. If included, will produce\
                                   animation. Valid date is prior to NOW-24 hours and\
                                   after 'date'")
        parser.add_argument('-eh', '--endhour',\
                             help="OPTIONAL end hour. Default is 00.")
        parser.add_argument('-a','--plotarrows',action='store_true',\
                            default=False, \
                            help="OPTIONAL plot wind vectors.\
                                  **EXPERIMENTAL - Not working very well right now**")


        args = parser.parse_args()

        self.testargs(args)
        self.plotarrows = args.plotarrows

        return args
        

    def testargs(self, args):
        sd = None
        ed = None

        ### Test for valid time
        validhours = ['00','06','12','18']
        if args.hour not in validhours:
            sys.exit("Invalid hour. Valid hours are '00','06','12','18'")

        if args.endhour is not None:
            if args.endhour not in validhours:
                sys.exit("Invalid endhour hour. Valid hours are '00','06','12','18'")


        self.testargdates((args.date, args.enddate))

        sd = datetime.strptime(args.date+args.hour,'%Y%m%d%H')

        ### If there is an end date, test for end hour and then make sure
        ### End date is after date (including hour).
        ### Note: if enddate is given, but end hour is not, we default to 00
        if args.enddate is not None:
            hr = '00' if args.endhour is None else args.endhour
            ed = datetime.strptime(args.enddate+hr,'%Y%m%d%H')
            if ed <= sd:
                raise sys.exit("[ERROR] :End date ("+ed.isoformat()+") is "+\
                               "not later than start date ("+sd.isoformat()+")")

        ### Note: setting ed = sd should provide single snapshot
        else:
            ed = sd 


        self.startdate = sd
        self.enddate = ed

        return

 

    def testargdates(self, dates):
        earliestdate = datetime.strptime('19990814 00','%Y%m%d %H')
        latestdate = datetime.today() - timedelta(hours=24)

        for date in dates:
            if date is None: continue ### Skip null

            ### Test for valid date format """
            try:
                datetime.strptime(date,'%Y%m%d')
            except:
                sys.exit("Invalid date format. Required format YYYYMMDD. Eg. 20130701")
        
            ### Test user date is after earliest available date """
            if datetime.strptime(date,'%Y%m%d') < earliestdate:
                sys.exit("[ERROR] Invalid date. Please chose date after: " + \
                         earliestdate.date().isoformat())
    
            ### Test user date is before latest available date """
            if datetime.strptime(date,'%Y%m%d') > latestdate:
                sys.exit("[ERROR] Invalid date. Please chose date no later than: " + \
                         latestdate.date().isoformat())

        return


    def extrema(self,mat,mode='wrap',window=10):
        """find the indices of local extrema (min and max)
        in the input array."""
        mn = minimum_filter(mat, size=window, mode=mode)
        mx = maximum_filter(mat, size=window, mode=mode)
        # (mat == mx) true if pixel is equal to the local max
        # (mat == mn) true if pixel is equal to the local in
        # Return the indices of the maxima, minima
        return np.nonzero(mat == mn), np.nonzero(mat == mx)

    def updatefig(self,nt):
        date = self.dates[nt]
        if self.CS1 is not None:
            for c in self.CS1.collections: c.remove()
        self.CS1 = self.m.contour(self.x,self.y,self.slp[nt,:,:],self.clevs,\
                                  linewidths=0.5,colors='k')

        if self.CS2 is not None:
            for c in self.CS2.collections: c.remove()
        self.CS2 = self.m.contourf(self.x,self.y,self.slp[nt,:,:],self.clevs,\
                                   cmap=plt.cm.RdBu_r)

        self.updateextrema(nt)
        self.txt = plt.title('SLP and Wind Vectors '+str(date))

        if self.plotarrows is True:
            if self.Q is None:
                # plot wind vectors over map.
                self.Q = self.m.quiver(self.x,self.y,self.u[nt,:,:],self.v[nt,:,:],\
                                       scale=500,zorder=10)
                # make quiver key.
                qk = plt.quiverkey(self.Q, 0.1, 0.1, 20, '20 m/s', labelpos='W')
            else:
                self.Q.set_UVC(self.u[nt,:,:],self.v[nt,:,:])

    
    def updateextrema(self,nt):
        del self.fig.gca().texts[:]
        # the window parameter controls the number of highs and lows detected.
        # (higher value, fewer highs and lows)
        local_min, local_max = self.extrema(self.slp[nt], mode='wrap', window=50)
        xlows = self.x[local_min]
        xhighs = self.x[local_max]
        ylows = self.y[local_min]
        yhighs = self.y[local_max]
        lowvals = self.slp[nt][local_min]
        highvals = self.slp[nt][local_max]
        # plot lows as blue L's, with min pressure value underneath.
        xyplotted = []
        # don't plot if there is already a L or H within dmin meters.
        yoffset = 0.022*(self.m.ymax-self.m.ymin)
        dmin = yoffset
    
        for x,y,p in zip(xlows, ylows, lowvals):
            if x < self.m.xmax and x > self.m.xmin and y < self.m.ymax and \
                                                            y > self.m.ymin:
                dist = [np.sqrt((x-x0)**2+(y-y0)**2) for x0,y0 in xyplotted]
                if not dist or min(dist) > dmin:
                    plt.text(x,y,'L',fontsize=14,fontweight='bold',
                            ha='center',va='center',color='b')
                    plt.text(x,y-yoffset,repr(int(p)),fontsize=9,
                            ha='center',va='top',color='b',
                            bbox = dict(boxstyle="square",ec='None',fc=(1,1,1,0.5)))
                    xyplotted.append((x,y))
    
        # plot highs as red H's, with max pressure value underneath.
        xyplotted = []
        for x,y,p in zip(xhighs, yhighs, highvals):
            if x < self.m.xmax and x > self.m.xmin and y < self.m.ymax and \
                                                            y > self.m.ymin:
                dist = [np.sqrt((x-x0)**2+(y-y0)**2) for x0,y0 in xyplotted]
                if not dist or min(dist) > dmin:
                    plt.text(x,y,'H',fontsize=14,fontweight='bold',
                            ha='center',va='center',color='r')
                    plt.text(x,y-yoffset,repr(int(p)),fontsize=9,
                            ha='center',va='top',color='r',
                            bbox = dict(boxstyle="square",ec='None',fc=(1,1,1,0.5)))
                    xyplotted.append((x,y))
    
    
    

    def setupmap(self):
        # read lats,lons,times.
        self.latitudes = self.data.variables['lat'][:]
        self.longitudes = self.data.variables['lon'][:].tolist()
        times = self.data.variables['time']

        ntime1 = date2index(self.startdate,times,calendar='standard')
        ntime2 = date2index(self.enddate,times,calendar='standard')
        
        # get sea level pressure and 10-m wind data.
        slpdata = self.data.variables['Pressure_reduced_to_MSL_msl']
        udata = self.data.variables['u-component_of_wind_height_above_ground']
        vdata = self.data.variables['v-component_of_wind_height_above_ground']
        
        # mult self.slp by 0.01 to put in units of millibars.
        slpin = 0.01*slpdata[ntime1:ntime2+1,:,:]
        uin = udata[ntime1:ntime2+1,0,:,:]
        vin = vdata[ntime1:ntime2+1,0,:,:]
        self.dates = num2date(times[ntime1:ntime2+1], times.units, calendar='standard')
        
        # add cyclic points
        self.slp = np.zeros((slpin.shape[0],slpin.shape[1],slpin.shape[2]+1),np.float64)
        self.slp[:,:,0:-1] = slpin; self.slp[:,:,-1] = slpin[:,:,0]
        self.u = np.zeros((uin.shape[0],uin.shape[1],uin.shape[2]+1),np.float64)
        self.u[:,:,0:-1] = uin; self.u[:,:,-1] = uin[:,:,0]
        self.v = np.zeros((vin.shape[0],vin.shape[1],vin.shape[2]+1),np.float64)
        self.v[:,:,0:-1] = vin; self.v[:,:,-1] = vin[:,:,0]
        self.longitudes.append(360.); self.longitudes = np.array(self.longitudes)
        
        # make 2-d grid of lons, lats
        self.lons, self.lats = np.meshgrid(self.longitudes,self.latitudes)
        
        # make orthographic basemap.
        self.m = Basemap(resolution='c',projection='ortho',lat_0=45.,lon_0=-97.)
        uin = udata[ntime1:ntime2+1,0,:,:]
        vin = vdata[ntime1:ntime2+1,0,:,:]
        
        # create figure, add axes (leaving room for colorbar on right)
        self.fig = plt.figure()
        ax = self.fig.add_axes([0.1,0.1,0.7,0.7])
        
        # set desired contour levels.
        self.clevs = np.arange(950,1065,7)
        
        # compute native x,y coordinates of grid.
        self.x, self.y = self.m(self.lons, self.lats)
        
        # define parallels and meridians to draw.
        parallels = np.arange(-80.,90,20.)
        meridians = np.arange(0.,360.,20.)
        
        # number of repeated frames at beginning and end is n1.
        pos = ax.get_position()
        l, b, w, h = pos.bounds
        
        # loop over times, make contour plots, draw coastlines, 
        # parallels, meridians and title.
        nt = 0; 
        self.updatefig(nt)
        
        # draw coastlines, parallels, meridians, title.
        self.m.drawcoastlines(linewidth=1.5)
        self.m.drawparallels(parallels)
        self.m.drawmeridians(meridians)
        self.m.drawstates()
        
        # plot colorbar on a separate axes (only for first frame)
        cax = plt.axes([l+w-0.05, b, 0.03, h]) # setup colorbar axes
        self.fig.colorbar(self.CS2,drawedges=True, cax=cax) # draw colorbar
        cax.text(0.0,-0.05,'mb')
        plt.axes(ax) # reset current axes
        
   

        
if __name__ == '__main__':
    a = ani(sys.argv)

