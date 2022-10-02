# Particle-tracking-velocimetry-and-Discrete-Element-Method
trackball is the main function that used OpenCV to track the ball from video. You can change the video given that it is a clear video, and you define the colour. I have not tested this on other geometries but know it works well for small spherical geometries. 
Coefficient of restitution was calculated from distances and velocities. distances were calculated from pixel coordinates. Velcoities calculated from distance and time.
E = (di/D0)^0.5 , E = vi/V0    di= distance after bounce D0=distance before bounce    vi= velocity after bounce v0= velocity before bounce 
v= m/s   d=metres
Comparisons file shows how a DEM was prgrammed with drag and buoyancy considerations. It also computes an analytical model which utilises suvat equations. Shows a comparison between DEM,analytical and ball track from video. 
This program can be made better.
