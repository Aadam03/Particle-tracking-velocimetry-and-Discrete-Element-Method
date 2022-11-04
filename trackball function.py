# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 04:38:24 2022

@author: Aadam
"""
#####################################################################################
#importing all relevant modules needed to run code please make sure you have all!!!
#####################################################################################
from collections import deque
import numpy as np
import cv2
import imutils
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d
import math
#creating function trackball so instead of pasting big chunk of code I can
#just call function. This saves a lot of space!

def trackball(vid,Lower,Upper,initialheight):
    #defining initial x and y position
    x = 0
    y = 0
 # setting buffer to 10; this is the ring around object in tracking
    buffer = 10
    #setting pts deque to the size of the buffer
    pts = deque(maxlen=buffer)
    # setting size of xt and yt deques so all positions can fit (worst case scenario)
    xt = deque(maxlen=1000)
    yt = deque(maxlen=1000)
   # defining distance, time and velocity lists so i can update them later
    distance = []
    t = []
    velocity = []

    # open video and get frames pers second, handy tool!
    vs = cv2.VideoCapture(vid)
    fps = vs.get(cv2.CAP_PROP_FPS)
    
    # keep looping
    while True:
        # grab the current frame

        frame = vs.read()
        frame = frame[1]

        # If there are no more frames left stop tracking and video
        if frame is None:  break

        # resize and blur frame then convert it to the HSV
        # colour space
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        colour = cv2.inRange(hsv, Lower, Upper)
        

        # construct a mask for the relevant colour, then perform
        # dilations and erosions to remove anything
        # left in the mask that would hinder tracking
        mask = colour
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
       
       

        # if a contour was found then run
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle on the frame,
                #  update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
        
        # loop over the set of tracked points
        for i in range(1, len(pts)):
            # if either of the tracked points are 0, ignore
            # them

            if pts[i - 1] is None or pts[i] is None:
                continue

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(buffer / float(i + 1)) * 2.5)
            cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
            # display tracking to screens
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
                
        #update pts with center values
        pts.appendleft(center)
        #update xt deque
        xt.append(x)
        # find true y positions in yt by subtracting since open cv tracks upside down
        yt.append(frame.shape[0]-y)
        #making lists for y and x positions
        y_list = list(yt)
        x_list= list(xt)
        #time taken for each frame
        dt = 1/fps
        #getting times of each frane in video in seconds
        video_sec = vs.get(cv2.CAP_PROP_POS_MSEC)/1000
        # finding ratio between pixel measurments and meters

        ratio = initialheight/yt[0]
        #finding diplacement by subtraction in series
        displacement = [yt[ti+1]-yt[ti] for ti in range(len(yt)-1)]
        #finding distance  by subtraction 
        distance = ([abs(yt[ti] - yt[ti-1]) for ti in range(1, len(yt))])
        #t is being updated with duration of video
        t.append(video_sec)
        
    # close all windows
    cv2.destroyAllWindows()
    #finding half way time between each frame to capture true time 
    t_center = [0.5 * (t[0] + t[1]) for t[0], t[1] in zip(t[:-1], t[1:])]
    
    #finding velocity by dividning displacement in each frame by time of each frame (constant)
    velocity = (np.divide(displacement, dt))*ratio

    
    #removing anomalous values in velocity list
    idxs = [idx for idx, val in enumerate(velocity) if val != 0] 
    #removing anomalous reult in t_center list
    idjs = [idj for idj, val in enumerate(t_center) if val != 0]
    
    #creating time and velocity lists where no anomalous values from bad tracking are 
    #included
    refined_time = [val for idj, val in enumerate(t_center) if idj in idjs]
    refined_velocity = [val for idx, val in enumerate(velocity) if idx in idxs]

   
    # legnth of velocity list without anomalous values
    m = len(refined_velocity)
    #removing anomalous reult in t list and renaming new time list true_time
    idls = [idl for idl, val in enumerate(t) if val != 0]
    
    # time without any anomalous times
    true_t = [val for idl, val in enumerate(t) if idl in idls]
    #legnth of time list without anomalous values
    z = len(true_t)  # legnth of time array with the zeros due to capturing errors
    
    
    ## converting pixel units to metres in x and y lists
    converted_xlist = (np.multiply(x_list, ratio))
    converted_ylist = (np.multiply(y_list, ratio))
    
    
   
    
    # energy calculations
    #ke calculation
    g = 9.81  # m/s/s
    mass = 0.056  # kg
    
    # finding ke by 0.5*m*v^2
    kinetic_energy = (np.multiply(refined_velocity, refined_velocity))*0.5*mass
    

    #finding gpe by m*g*h where h is height in evrey frame
    gpe = (np.multiply(y_list, (g*mass)))*ratio
    
    #removing anomalous results from gpe list
    ipps = [idp for idp, val in enumerate(gpe) if val != 0]
    #defining new gpe list without anomalous results due to tracking errors
    true_gpe = [val for idl, val in enumerate(gpe) if idl in idls]
    
    #assiging legnth of new gpe array to p
    p = len(true_gpe)
    
    #assiging legnth of ke array to l
    l = len(kinetic_energy)
    #reduce choppines
    smooth_velocity = gaussian_filter1d(refined_velocity, sigma=2) 
    
    total_energy = gpe[0:l]+ kinetic_energy
    #reducing choppiness
    smooth_total_energy = gaussian_filter1d(total_energy, sigma=2)
    #reducing chopiness 
    smooth_ke = gaussian_filter1d(kinetic_energy, sigma=2)
 # doing this for better plots but the original plot will be kept in the code
 #and can be unhashtagged to see the difference.




    # defining outputs of the function which I will need to plot.
    Out=[yt,xt,t,true_t,converted_xlist,
           converted_ylist,refined_velocity,refined_time,smooth_velocity,t_center,
           true_gpe,smooth_total_energy,smooth_ke,gpe, kinetic_energy]
    return Out

    

