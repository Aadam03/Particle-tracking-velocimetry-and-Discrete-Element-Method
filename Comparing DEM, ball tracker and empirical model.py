# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 02:44:29 2022

@author: Aadam
"""

import numpy as np

import matplotlib.pyplot as plt
import math

r = 2/1000
area = 4* (math.pi)*(r**2)
volume = area *r/3
rhofluid = 1.225 #kg/m^3
g = -9.81
CE = 0.764
CD = 0.51
m = 0.056 #kg
dt = 0.001
tmax = 4
N = int(abs(tmax/ dt))

rx0 = np.zeros(N)
ry0 = np.zeros(N)
vx0 = np.zeros(N)
vy0 = np.zeros(N)
drag_Fx = np.zeros(N)
drag_Fy = np.zeros(N)
Total_Fy = np.zeros(N)
Total_Fx = np.zeros(N)
ax = np.zeros(N)
ay = np.zeros(N)
Fb =volume*g*rhofluid
Fg= m*g
rx0[0] = 0
ry0[0] = 2


    
# finding positions and velocity through balls journey
for i in range(1, N):
    
    # finding forces affecting ball 
    drag_Fy[i] = CD *0.5*rhofluid*(vy0[i-1]**2)*area
    drag_Fx[i] = CD *0.5*rhofluid*(vx0[i-1]**2)*area
    Total_Fx[i] = drag_Fx[i-1]
    Total_Fy[i] = drag_Fy[i-1 ] +Fg - Fb
    ax[i]= (Total_Fx[i-1])/m # acceleration in x plane m/s/s
    ay[i]= Total_Fy[i-1]/m #m/s/s # acceleration in y plane 
    
    
    # findig velocities and positions of ball through journey 
    rx0[i] = rx0[i-1] + -vx0[i-1]*dt
    ry0[i] = ry0[i-1] + vy0[i-1]*dt
    vx0[i] = vx0[i-1] + ax[i-1]*dt
    vy0[i] = vy0[i-1] + ay[i-1] *dt
# bounce condition
    if ry0[i] < 0:
        vy0[i] *= -CE
        ry0[i] = 0

time = np.arange(N)*dt
##energy calculations
ke = vy0*vy0*0.5*m   
gpe = -m*g*vy0
totalenergy = gpe + ke

plt.plot(time, ry0,label = "DEM")
#plt.plot(time,ke)
#plt.plot(time,gpe)
#plt.plot(time,totalenergy)

###############################################################################

# initial time 
t=0
# acceleration
g = -9.81
# drop height
height = 2
# initial velocity
velocity = 0


#list of heights 
height_list = [height]
#list of times
t_list=  [0]
#list of velocities
velocity_list = []

#coeffcient of restitution 
e=0.764

# counter = number of iterations loop will do 
counter = 0
while counter <8: #loop will iterate 8 times (8 bounces)
    counter = counter +1  #counter increments after evrey iteration
    
    # calculating the maximum height v^2/-2g +inital height
    max_height = (velocity**2)/(-2*g) + height
    
    # calculating the time to go up  v/-g
    time_at_top = (velocity/-g)
    
    #adds time to each max height to to total time travelled by the particle 
    total_time=t_list[-1]+time_at_top

    # velocity at max height
    velocity_at_instantaneous_rest=0
     
    #appending velocity list with velocities calculated 
    velocity_list.append(velocity_at_instantaneous_rest)

    #appending height list with heights calculated 
    height_list.append( max_height) 
    
    #appendinf time list with times calculated
    t_list.append(total_time)

  


   #calculating fall time tf= sqrt(2*h/-g) 
    time_at_bottom = np.sqrt((2* max_height)/-g)

    #total time calculation by adding time at bottom to tlist 
    total_time=t_list[-1]+time_at_bottom
    
    
    #height at bottom
    height = 0
   #velocity after bounce
    velocity = (g*time_at_bottom) * -e 
    
    
 # appending the height time and velocity    
    height_list.append(height) 
    t_list.append(total_time)
    velocity_list.append(velocity)

plt.plot(t_list,height_list,'m-',label = "empirical")
################################################################################
from trackball import trackball 
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
initialh=2
video_file_path = r"C:\Users\Aadam\OneDrive - Coventry University\Documents\Chem Eng\Year 1\LDA\Portfolio 2\3.mp4"

Out=trackball(video_file_path,greenLower,greenUpper,initialh)
bout = Out  # assigning inputs to a global variable
# unpacking list
yt,xt,t,true_t,displacement,converted_xlist,converted_ylist,refined_velocity,refined_time,smooth_velocity,t_center,true_gpe,smooth_total_energy,smooth_ke,gpe, kinetic_energy = bout

#Legnth of true time list, easier to call
z = len(true_t)
#Legnth of true time list, easier to call
m = len(refined_velocity)
#assiging legnth of new gpe array to p
p = len(true_gpe)

#assiging legnth of ke array to l
l = len(kinetic_energy) 
plt.plot(true_t,(converted_ylist[0:z]),label="real trajectory") 
plt.title('Comparing how accurate the DEM and empirical model are when modelling trajectories of a ball',fontsize=10)
plt.xlabel('time (seconds)')
plt.ylabel('height (metres)')
plt.legend()
