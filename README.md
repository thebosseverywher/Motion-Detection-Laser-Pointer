# Motion-Detection-Laser-Pointer

This Project uses Open-cv python for motion detection.
The basic idea was for motion detection was change in pixel colour densities. If there is no motion the pixels dont change.
So considering a video as a stack of pictures I made that stack of pictures into a list named as diff frames and num diff frames is a number which can be any number
suppose if the number is 5, the code takes the difference of pixel densitites between first and fifth frame to find motion
after the difference, if there are bright spots, we get to know that motion is detected.

final is the python code that runs on your computer
laser turret final is the .ino that goes onto your arduino

needed materials
laptop with python and opencv,pywin libraries
arduino uno
2 servos
1 laser diode
