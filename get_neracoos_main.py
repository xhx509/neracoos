3# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:30:34 2013
This is the main program of neracoos,you could get temp,wind,current data from here
*Before you running it, please check the control file

@author: hxu
"""

print "    please input data in 'get_neracoos_ctl.txt' "
print "    1= get temperture data  "
print "    2= get wind data"
print "    3= get current surface data "
print "    4= get current layers data"

option=raw_input('\nMake a selection: ')
#option='4'
print "you just selected option "+ option
if option=='1':
    print 'to get temp data' 
    execfile("get_neracoos_temp.py")
    
if option=='2':
    print 'to get wind data'
    execfile("get_neracoos_wind.py")
    
if option=='3':
    print'to get surface current data'
    execfile("get_neracoos_current.py")
    
if option=='4':
    print 'to get layer current data'
    execfile("get_neracoos_deep_current.py")
    



##################################################
''' lat and lon of sites, you may use it in control file
Dataset: A01.sbe37.historical.50m.nc
lat, 42.5180647466176
lon, -70.5652227043109
Dataset: B01.sbe37.historical.20m.nc
lat, 43.1806472713891
lon, -70.4276963702579
Dataset: D02.sbe37.historical.10m.nc
lat, 43.7617166666667
lon, -69.9878833333333
Dataset: E01.sbe37.historical.50m.nc
lat, 43.7151721464189
lon, -69.3557710445127
Dataset: E02.sbe37.historical.50m.nc
lat, 43.7065
lon, -69.32
Dataset: F01.sbe37.historical.50m.nc
lat, 44.0556001811715
lon, -68.9967173062176
Dataset: F02.sbe37.realtime.1m.nc
lat, 44.3878
lon, -68.8308
Dataset: I01.sbe37.historical.50m.nc
lat, 44.1059919278702
lon, -68.1084972935196
Dataset: M01.sbe37.historical.250m.nc
lat, 43.4897
lon, -67.8815
Dataset: N01.sbe37.historical.180m.nc
lat, 42.3314893622147
lon, -65.9064274838096
'''
###############################################################