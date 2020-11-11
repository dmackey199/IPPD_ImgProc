## Interfacing the Camera
Here is the tutorial used that is very helpful and includes pictures for installation.
https://www.dexterindustries.com/howto/installing-the-raspberry-pi-camera/  
Upon reboot, type  
```
vcgencmd get_camera
``` 
into the terminal to quickly see if you have installed the Raspberry Pi correctly. It should say something like  
supported = 1, detected = 1 if it has correctly been connected.If it shows detected = 0, there is something wrong with the connection. 

Check out the VideoEdgeDetect folder to see OpenCV's capabilities with your new camera installed!