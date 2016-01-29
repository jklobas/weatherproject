# weatherproject
A project to visualize weather data scraped from ULMO

Hello Git,

I am not a programmer, coder, or anything; all of my scripting knowledge is self-learned. I write scripts to solve scientific problems, but in the past I've mainly limited myself to Mathematica, Igor Pro, Matlab, MathCAD, and a few other environments. I've always had a bit of trepidation for sharing my work, but I am not adverse to constructive criticism.  

This is my first attempt at (1) using Git, (2) using Python for scientific computing purposes, and (3) using GIS tools for data visualization.  The goals of this project are as follows:  (1) scrape data from remote sources, (2) process the data in some manner, (3) store this data in a retrievable package, (4) do something fun with this data, and (5) do all of this using Python only.

You'll find here two scripts: 

(1) GISloopiteratorv2.py which grabs weather station data from a list of IDs using the excellent ULMO tool, calculates the monthly normals for maximum and minimum temperature for the time period of 1951 - 2015, and generates statistics such as the average temperature at each weather station over the time period and the individual t-score deviations of the monthly measurements. The data is then pickled.

(2) plotteryv2.py which takes the data points of interest and then interpolates them spatially, generates contours and plots them on a map of the USA. 

For example:
![Average Maximum Temperatures in the USA - December](https://github.com/jklobas/weatherproject/blob/master/figure_1Avgs.png)
This graphic depicts the average maximum temperatures recorded in the USA between 1951 - 2015 as well as the weather station locations used to compute this data.

We can then plot the temperature anomaly (that is, subtract the monthly normal from the observered average). I do this here for December 2015:
![December 2015 Maximum Temperature Anomaly](https://github.com/jklobas/weatherproject/blob/master/figure_1anom.png)
I believe the dipole in Montana is an artifact of interpolating over bad weather station data.

And then we can also easily generate graphics depicting the Student's T-distribution score ( [observed - average] / standard deviation ), showing that for most of the Eastern United States, December 2015 was extraordinarily warm.
![December 2015 Maximum Temperature T-Scores](https://github.com/jklobas/weatherproject/blob/master/figure_1tstat.png)

Similarly, we can look at each individual weather station.  Here, we zoom into the Blue Hills Reservation weather station in Massachussets.
![December Minimum Temperatures by Year, Blue Hills Reservation](https://github.com/jklobas/weatherproject/blob/master/mintemp.png)
![December Maximum Temperatures by Year, Blue Hills Reservation](https://github.com/jklobas/weatherproject/blob/master/maxtemp.png)

Interestingly (to me, at least), we see that 2015 is by far the hottest December on record by both average high and average low. In fact, the average low temperature in December 2015 was ABOVE freezing!

As this project progresses, I'd like to add some hypothesis testing, to see if El Nino really does affect surface temperature in an easily extractable way.  
