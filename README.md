# Motion-Detection-Laser-Pointer

This project implements a motion detection laser turret control system using Python with OpenCV for motion detection and Arduino for controlling the laser turret. The system detects motion by analyzing changes in pixel color densities in consecutive video frames. It then uses these motion detections to control the movement of a laser turret via servo motors.

## Features

- Motion detection using OpenCV.
- Python script to control the motion detection process and servo movement.
- Arduino code to receive servo commands and control the servo motors accordingly.
- Serial communication between Python and Arduino.

## Requirements

To run this project, you will need the following materials:

- Laptop with Python installed (with OpenCV, PyWin32, and pyserial libraries).
- Arduino Uno.
- 2 servo motors.
- 1 laser diode.

## Setup Instructions

1. **Hardware Setup:**
   - Connect the servo motors and laser diode to the Arduino Uno according to the circuit diagram provided.

2. **Software Setup:**
   - Install OpenCV, PyWin32, and pyserial libraries for Python

3. **Usage:**
   - Run the Python script `final.py` on your laptop.
   - Ensure your webcam or camera is connected and properly configured.
   - Follow the on-screen instructions to calibrate motion detection and control the laser turret.

## Circuit Diagram

Include a circuit diagram here if applicable.

## Configuration

- Adjust the `num_diff_frames` parameter in the `motion_detection.py` script to control the sensitivity of motion detection.

## License

This project is licensed under the MIT License - see the [GNU General Public License v3.0](LICENSE).
