# Particle-tracking-velocimetry-and-Discrete-Element-Method
 The trackball function uses OpenCV to track the ball from a video. You can change the video given that it is a clear video, and you define the colour of the ball. I have not tested this on other geometries but know it works well for small spherical geometries. 
The coefficient of restitution was calculated from distances and velocities. Distances were calculated from pixel coordinates. Velocities are calculated from distance and time.
E = (di/D0)^0.5 , E = vi/V0, E = Coefficient of restitution , di= distance after bounce , D0=distance before bounce , vi= velocity after bounce, v0= velocity before bounce 
v= m/s   d=metres
The comparisons file includes a discrete element model, which was programmed with drag and buoyancy considerations. It also has an analytical model which utilises SUVAT equations to simulate a ball's journey. A comparison between the DEM, analytical model and ball track model from a video is shown.
This program can be made better.
