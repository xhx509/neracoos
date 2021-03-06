# -*- coding: utf-8 -*-
"""
Created on Thu May 02 08:27:24 2013

@author: Huanxin
"""
####################################################
####################################################
#get temp data from neracoos OpenDap,generate a dataframe which includes time,lat,lon.temp and depth.
#then ,plots a graph
#Functions uses: get_neracoos_ctl, get_id_s_id_e_id_max_url, depth_select, get_neracoos_temp_data
#input values: datetime period,the mooring type, the name of mooring site
#output values: a data frame 
####################################################
####################################################
from matplotlib.dates import date2num, num2date
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
from pandas import *
from neracoos_def import get_neracoos_ctl,depth_select,get_id_s_id_e_id_max_url,get_neracoos_temp_data
from get_neracoos_ctl import get_neracoos_ctl_py

inputfilename='./get_neracoos_ctl.txt'
if inputfilename[-2:]=='py':
    mindtime,maxdtime,i_mindepth,i_maxdepth,model,sites=get_neracoos_ctl_py()
else:
    
    mindtime,maxdtime,i_mindepth,i_maxdepth,model,sites=get_neracoos_ctl(inputfilename) #get input from input file
model='sbe37' #####This hard code to make sure you get temp and salt data
sdtime_n=date2num(mindtime)-date2num(dt.datetime(1858, 11, 17, 0, 0)) #get number type of start time
edtime_n=date2num(maxdtime)-date2num(dt.datetime(1858, 11, 17, 0, 0)) #get number type of end time

depths,site_d=depth_select(sites,i_mindepth,i_maxdepth) #one site match one depth, 
if site_d==[]:
    print 'No right site , Please check website and your input data, '
    
for index_site in range(len(site_d)):
    
    if model=='sbe16':
        
       url='http://neracoos.org:8080/opendap/'+site_d[index_site]+'/'+site_d[index_site]+'.'+model+'.historical.nc?' 
    else:     
       url='http://neracoos.org:8080/opendap/'+site_d[index_site]+'/'+site_d[index_site]+'.'+model+'.historical.'+depths[index_site]+'m.nc?'     
    id_s,id_e0,id_max_url,maxtime,mintime=get_id_s_id_e_id_max_url(url,sdtime_n,edtime_n) # 'maxtime',the max time in this url, "id_s",the index of start time we want
    if mintime=='':   
        histvsreal='1' #"histvsreal" can help us judge if this  site has historical data.
        url='http://neracoos.org:8080/opendap/'+site_d[index_site]+'/'+site_d[index_site]+'.'+model+'.realtime.'+depths[index_site]+'m.nc?'     
        id_s,id_e0,id_max_url,maxtime,mintime=get_id_s_id_e_id_max_url(url,sdtime_n,edtime_n)  # 'maxtime',the max time in this url, "id_s",the index of start time we want
        #get id of start time and end time,max time id of this url, 
        print 'realtime from '+str(num2date(date2num(dt.datetime(1858, 11, 17, 0, 0))+mintime))+'to'+str(num2date(date2num(dt.datetime(1858, 11, 17, 0, 0))+maxtime))    
    else:
        histvsreal=''
    if id_e0<>'':  
      (depth_temp,period_str)=get_neracoos_temp_data(url,id_s,id_e0,id_max_url) #get data from web neracoos
      print 'the end time of this database is '+num2date(maxtime+date2num(dt.datetime(1858, 11, 17, 0, 0))).strftime("%d-%b-%y")
      
      df = DataFrame(np.array(depth_temp),index=period_str,columns=['depth','temp','salinity'])
      have_not=1   # dataframe not equal none ,so we can plot it
    else:
      print "According to your input, there is no data here"
      have_not=0   # dataframe equal none ,so we can not plot it
    if histvsreal<>'1': 
      if   maxtime<edtime_n: #make sure if we need a realtime data
        url='http://neracoos.org:8080/opendap/'+site_d[index_site]+'/'+site_d[index_site]+'.'+model+'.realtime.'+depths[index_site]+'m.nc?'     
        id_s,id_e,id_max_url,maxtime,mintime=get_id_s_id_e_id_max_url(url,sdtime_n,edtime_n)
        if id_e<>'':    
           have_not=1 # dataframe not equal none ,so we can plot it
           (depth_temp,period_str)=get_neracoos_temp_data(url,id_s,id_e,id_max_url)  #get data from web neracoos
           #df = DataFrame(np.array(depth_temp),index=period_str,columns=['                depth','      temp']).append(df)
           if id_e0=='':
              df = DataFrame(np.array(depth_temp),index=period_str,columns=['depth','temp','salinity'])#combine them in DataFrame   
           else:              
              df.append(DataFrame(np.array(depth_temp),index=period_str,columns=['depth','temp','salinity']))    
    
    
    if have_not==0:
        continue    # If dataframe== None, pass it
    else:
      fig, axes = plt.subplots(nrows=2, ncols=1)
    
      df_t=df.ix[:,[1]]  #creat a new df only for temp  
      df_t.plot(ax=axes[0],title=site_d[index_site]+'   Depth=-'+depths[index_site]+'m')
      plt.gcf().autofmt_xdate()
  
      df_s=df.ix[:,[2]]   #creat a new df only for salinity  
      df_s.plot(ax=axes[1],color='r')
      plt.gcf().autofmt_xdate()
      df.to_csv('temp_'+site_d[index_site]+'_'+depths[index_site]+'m.csv') #save it to a csv file
plt.show()




























'''
mindtime1,maxdtime1,i_mindepth,i_maxdepth,site2,mindtime,maxdtime
	  #According to the conditions to select data from "emolt_sensor"
url2="http://gisweb.wh.whoi.edu:8080/dods/whoi/emolt_sensor?emolt_sensor.SITE,emolt_sensor.TIME_LOCAL,emolt_sensor.YRDAY0_LOCAL,emolt_sensor.TEMP,emolt_sensor.DEPTH_I&emolt_sensor.TIME_LOCAL>="+str(mindtime1)+"&emolt_sensor.TIME_LOCAL<="\
+str(maxdtime1)+"&emolt_sensor.DEPTH_I>="+str(i_mindepth)+"&emolt_sensor.DEPTH_I<="+str(i_maxdepth)+site2
try:   
    dataset1=open_url(url2)
except:
    print 'Sorry, '+url2+' not available' 
    sys.exit(0)
emolt_sensor=dataset1['emolt_sensor']
try:   
	          sites2=list(emolt_sensor['SITE'])
except:
	          print "'Sorry, According to your input, here are no value. please check it! ' "
	          sys.exit(0) 
	  #sites2=list(emolt_sensor['SITE'])
time=list(emolt_sensor['TIME_LOCAL'])
yrday0=list(emolt_sensor['YRDAY0_LOCAL'])
temp=list(emolt_sensor['TEMP'])
depth1=list(emolt_sensor['DEPTH_I'])
	

	  time1,temp1,yrday01,sites1,depth=[],[],[],[],[]
	  for m in range(len(time)):
	      #if mindtime<=dt.datetime.strptime(str(time[m]),'%Y-%m-%d')<=maxdtime:
	      if date2num(mindtime)<=yrday0[m]%1+date2num(dt.datetime.strptime(str(time[m]),'%Y-%m-%d'))<=date2num(maxdtime):
	      #if str(time[m])=='2012-01-01':
	        temp1.append(temp[m])
	        yrday01.append(yrday0[m]%1+date2num(dt.datetime.strptime(str(time[m]),'%Y-%m-%d')))
	        sites1.append(sites2[m])
	        time1.append(date2num(dt.datetime.strptime(str(time[m]),'%Y-%m-%d'))) 
	        depth.append(depth1[m])
	  #print len(temp1)     
	  return time1,yrday01,temp1,sites1,depth,'''

