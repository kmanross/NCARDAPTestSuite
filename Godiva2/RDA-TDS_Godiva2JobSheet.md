Hopefully what follows is a coherent procedure for playing around with (I mean "testing") the Godiva2 viewer configured with the NCAR RDA's experimental THREDDS http://www.unidata.ucar.edu/projects/THREDDS/ which is at:

Send any questions/comments to manross@ucar.edu

http://castle.ucar.edu/thredds 
(Note: requires a subscription which can be found at https://rda.ucar.edu/index.html?hash=data_user&action=register)

### Getting started/familiar with the the Godiva2 Viewer: __Basics__

__First step__: Be sure you have an RDA account.  If you have already used the NCAR RDA (formerly known as DSS), and your account is still active, then you should be good to go!

__Next__: Go to the RDA THREDDS Data Server (TDS) at http://castle.ucar.edu/thredds/  You will be asked for your RDA username and password.  _(Your credentials may fail upon the first few attempts. I am looking for the source of this error. It should accept your login after 3-5 attempts.)_

__Then__: click on the "Best Timeseries" for the ds083.2 dataset

<img src="http://github.com/kmanross/NCARDAPTestSuite/blob/master/Godiva2/RDA_TDS_BestTimeseries.png?raw=true" width="350" height="450"/>

__After__: clicking on the Best Timeseries link, you will find a link near the bottom of the page for the Godiva2 viewer.  This will allow you to peruse the available data as images and even allow some rudimentary sampling.  (But I'm getting ahead of myself).

<img src="http://github.com/kmanross/NCARDAPTestSuite/blob/master/Godiva2/RDA_TDS_Godiva2.png?raw=true" width="350" height="450"/>

__At this point__: you should see a page with a maop in the middile and a few links in the upper left corner. Click on the plus sign to expand the list of available parameters for this dataset:

<img src="http://github.com/kmanross/NCARDAPTestSuite/blob/master/Godiva2/RDA_TDS_Gidiva2_InitialWindow.png?raw=true" width="450" height="350"/>

__Go__: ahead and find the link for Relative Humidity at specificed height above ground layer and click on it.  You should see an image like the one below sans ovals and arrows.  We'll get to those in a second...

<img src="http://github.com/kmanross/NCARDAPTestSuite/blob/master/Godiva2/RDA_TDS_RHAtHeightAboveGround_Default.png?raw=true" width="450" height="350"/>

  + __GREEN__ oval on the left should help you find the RH product.  It's corresponding oval at the top indicates the current product displayed on the map
  + __DARK GREEN__ oval indicates the height and is adjustable.  Based on the product you select this feature may or may not be available
  + __ORANGE__ oval in upper right is a calendar with clickable dates for all avalable data
  + __PURPLE__ oval above the map indicates the available times for this date and product.
  + __BLUE__ oval is the product overlayed on an interactive map.  You can pan & zoom.
  +     ... "But," you ask, "this is RH and the color scale seem all off!"
  + __BLUE__ _arrow_ allows you to reset the color scale based on the product.  You will need to use this each time you load a new product.
  + __YELLOW__ oval sets the opacity of the overlay of the map.  
  
Play around with these a bit and get used to them.  I have kept the same product sand time, but reset the color scale and opacity and now my map looks like this:

<img src="http://github.com/kmanross/NCARDAPTestSuite/blob/master/Godiva2/RDA_TDS_RHAtHeightAboveGround_ColorAndTransparent.png?raw=true" width="450" height="350"/>

### Getting started/familiar with the the Godiva2 Viewer: __Sampling__

You are encouraged to click on the Godiva2 Viewer's User Guide link in the lower left corner of the page to see what all can be done with this tool.
I'm now going to show you a few features that may come in handly for some quick and simple iterrogation of the data you might be interested in.

Go ahead and pick any other product, date, level that is available.  I'm going to choose the v-component of the wind for 9 April 2012 at 12z and select the 500 mb layer. I then select and area over Austrailia. (Don't forget to scale the color map!)

<img src="http://github.com/kmanross/NCARDAPTestSuite/blob/master/Godiva2/RDA_TDS_v-component_500mb_9April2012_12z.png?raw=true" width="450" height="350"/>


Now, if you click anywhere on the map, you should see a little box pop up where you clicked with the latitude, longitude and the __value__ of the pixel at that point.  Try a couple of places.

<img src="http://github.com/kmanross/NCARDAPTestSuite/blob/master/Godiva2/RDA_TDS_v-component_500mb_9April2012_12z_sampling.png?raw=true" width="450" height="350"/>

If you think that was neat, let's try something a bit more fun.  

__Just above the map__ and below the calendar is a little hand icon and to it's left is an icon resembling a few line segments.  Click that icon (it should turn yellow when you do meaning it is active).
__Now__ click somewhere on the left side of the map (be sure to be in a data area).
__Next__ pick a spot on the right side of the map and _double-click_ and wait to see what happens...

<img src="http://github.com/kmanross/NCARDAPTestSuite/blob/master/Godiva2/RDA_TDS_v-component_500mb_9April2012_12z_xsect.png?raw=true" width="450" height="350"/>

You should have a window pop up that looks like a cross section of the line you just created on the map!  Since we have loaded a three-dimensional product, we get a value trace at the level that is displayed (top graph) and values displayed for all levels (bottom graph) along te line we drew.

If you want to get crazy, try clicking multi-segment lines and remember to finish by double-clicking.  Now try to follow what you just sampled!  :-)




