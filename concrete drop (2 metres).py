# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 14:14:39 2022

@author: Aadam
"""

import numpy as np
import matplotlib.pyplot as plt
from trackball import trackball 
from scipy.ndimage.filters import gaussian_filter1d
import math

# define the lower and upper boundaries of different ball colours
# in the HSV color space
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

initialh = 2
Out=trackball("C:/Users/Aadam/OneDrive - Coventry University/Documents/Chem Eng/LDA/Portfolio 2/3.mp4"
              ,greenLower,greenUpper,initialh)
bout = Out
# unpacking list
yt,xt,t,true_t,converted_xlist,converted_ylist,refined_velocity,refined_time,smooth_velocity,t_center,true_gpe,smooth_total_energy,smooth_ke,gpe, kinetic_energy = bout

#Legnth of true time list, easier to call
z = len(true_t)
#Legnth of true time list, easier to call
m = len(refined_velocity)
#assiging legnth of new gpe array to p
p = len(true_gpe)

#assiging legnth of ke array to l
l = len(kinetic_energy)

## coefficient of restitution calcuation 

#finding the positions when a bounce occurs by estimating how large y is at these times 
c = [(i) for i, y in enumerate(converted_ylist) if y < 0.07]
#print(c)
#first to start from in the list when finding the max after first bounce
lower_limit1 = c[1]
#v_before = refined_velocity[:bounce] 
height_after_bounce1 = max(converted_ylist[lower_limit1:] )
#mean_v_before = sum(v_before)/len(v_before)
#mean_v_after = sum(v_after)/len(v_after)  
coefficent_of_restitution1 = abs(math. sqrt((height_after_bounce1/initialh) ))



#Cr is sqrt max height afte bounce/ initial height
#second bounce is 3rd position in list
lower_limit2 = c[3]
max_height_before_bounce2 = height_after_bounce1
max_height_after_bounce2 = max(converted_ylist[lower_limit2:] )
coefficent_of_restitution2 = abs(math.sqrt((max_height_after_bounce2/max_height_before_bounce2) ))

#3rd bounce
lower_limit3= c[5]
max_height_before_bounce3 = max_height_after_bounce2
max_height_after_bounce3 = max(converted_ylist[lower_limit3:] )
coefficent_of_restitution3 = abs(math.sqrt((max_height_after_bounce3/max_height_before_bounce3) ))





average_Cr_from_heights = round(((coefficent_of_restitution1 + coefficent_of_restitution2+ coefficent_of_restitution3)/3),3)


## velocity method of finding coefficient of res
## limits can basically be same as the ones used height because when 
#h tends to 0 v tends to 
# its max value which can be taken as final and initial velocities depending on which 
# way it is looked at and this process can be repeated


initial_velocity1 = abs(( min(refined_velocity[0:lower_limit1])))
final_velocity1 = max(refined_velocity[lower_limit1:])
initial_velocity2 = final_velocity1
#final_velocity2 = max(refined_velocity[])
gg = [(i) for i,(refined_velocity) in enumerate(refined_velocity[lower_limit2:]) if refined_velocity < 0]
lower_limit3 = gg[0] + lower_limit2
lower_limit4= gg[51] 
final_velocity2 = max(refined_velocity[c[2]:])
cr1 = final_velocity1/initial_velocity1
cr2 = final_velocity2/initial_velocity2
initial_velocity3 = final_velocity2

final_velocity3 = min(refined_velocity[lower_limit4:])
cr3 = abs(final_velocity3/initial_velocity3)

average_cr_from_velocities= round(abs((cr1+cr2+cr3)/3),3)

print("The average coefficient of restitution found from heights, for your model was:",+ average_Cr_from_heights, 
      "and the average COR from velocities for your model was",+ average_cr_from_velocities)

##plotting plots
fig, axs = plt.subplots(2,2)

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