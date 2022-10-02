# -*- coding: utf-8 -*-
"""


@author: Aadam
"""
#soft 1m
import numpy as np
import matplotlib.pyplot as plt
from trackball import trackball 
from scipy.ndimage.filters import gaussian_filter1d


# define the lower and upper boundaries of the ball colours in 
#the HSV color space
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
orangeLower = (18,40,90)
orangeUpper = (27,255,255)
redLower= (0,150,0)
redUpper = (10,255,255)
blueLower= (100,150,0)
blueUpper=(140,255,255)
yellowLower= (22,93,0)
yellowUpper = (45,255,255)
purpleLower = (129,50,70)
purpleUpper = (158,255,255)
blackLower= (0,0,0)
blackUpper = (180,255,30)
whiteLower = (0,0,231)
whiteUpper = (180,18,255)


#exp1
initialh = 1
Out=trackball("C:/Users/Aadam/OneDrive - Coventry University/Documents/Chem Eng/LDA/Portfolio 2/31.mp4"
              ,greenLower,greenUpper,initialh)
bout = Out
# unpacking list
yt,xt,t,true_t,converted_xlist,converted_ylist,refined_velocity,refined_time,smooth_velocity,t_center,true_gpe,smooth_total_energy,smooth_ke,gpe, kinetic_energy = bout
# COR calculation
max_height1 = max(converted_ylist[50:])
cr = round(np.sqrt( max_height1/initialh),3)
print("The coefficient of restitution for your model was",+ cr)
#Legnth of true time list, easier to call
z = len(true_t)
#Legnth of true time list, easier to call
m = len(refined_velocity)
#assiging legnth of new gpe array to p
p = len(true_gpe)

#assiging legnth of ke array to l
l = len(kinetic_energy)


##plotting plots
fig, axs = plt.subplots(2,2)


#distance against time

axs[0,0].plot(true_t,converted_xlist[0:z])  
axs[0,0].set_title('distance against time plot')
axs[0,0].set_xlabel('time (seconds)')
axs[0,0].set_ylabel('distance (metres)')


#height against time

axs[0,1].plot(true_t,(converted_ylist[0:z])) 
axs[0,1].set_title('height against time plot')
axs[0,1].set_xlabel('time (seconds)')
axs[0,1].set_ylabel('height (metres)')



#height against distance 
 
axs[1,0].plot(converted_xlist,converted_ylist)
axs[1,0].set_title('height against distance plot')
axs[1,0].set_xlabel('distance (metres)')
axs[1,0].set_ylabel('height (metres)')


#velocity time graph before smoothing
#plt.plot((refined_time[0:m]),refined_velocity)
#plt.title('velocity against time plot')
#plt.xlabel('time (seconds)')
#plt.ylabel('velocity (m/s)')
#plt.show()

#plotting a smoother velocity graph 


axs[1,1].plot((refined_time[0:m]),smooth_velocity) 
axs[1,1].set_title('velocity against time plot')
axs[1,1].set_xlabel('time (seconds)')
axs[1,1].set_ylabel('velocity (m/s)')

plt.tight_layout()
plt.show()

fig, (ax1, ax2,ax3) = plt.subplots(1,3)

##plot for gpe over time

ax1.plot(t_center[0:p],true_gpe)
ax1.set_title('GPE TIME')
ax1.set_xlabel('time (seconds)')
ax1.set_ylabel('Gravitational Potential Energy (Joules)')

## plot of ke without smoothing over time
#plt.plot(t_center[0:m],kinetic_energy)
#plt.title('Kinetic Energy against time plot')
#plt.xlabel('time (seconds)')
#plt.ylabel('Kinetic Energy (Joules)')
#plt.show()

##plot for ke with smoothing with time 

ax2.plot(t_center[0:l], smooth_ke)
ax2.set_title('KE time plot')
ax2.set_xlabel('time (seconds)')
ax2.set_ylabel('Kinetic Energy (Joules)')

##finding total energy without smoothing
#total_energy = gpe[0:l]+ kinetic_energy
## raw total energy plot
#plt.plot(t_center[0:l],total_energy)
#plt.title('Total Energy against time plot')
#plt.xlabel('time (seconds)')
#plt.ylabel('Total Energy (Joules)')
#plt.show()
## plot for total energy  over time
ax3.plot(t_center[0:l], smooth_total_energy)
ax3.set_title('Total Energy  time plot')
ax3.set_xlabel('time (seconds)')
ax3.set_ylabel('Total Energy (Joules)')
 
plt.tight_layout()
plt.show()
