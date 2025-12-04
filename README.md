# IBVS-Control-for-MyCobot-280PI

This project implements an Image-Based Visual Servoing (IBVS) control system for the MyCobot 280 Pi robot. The control architecture is developed primarily in Python, while computationally intensive mathematical operations are executed through MATLAB, which is called directly from the Python environment.

The objective of the project is to design, simulate, and deploy an IBVS controller capable of adjusting the robot’s end-effector motion based on real-time visual feedback. By extracting image features and minimizing their error with respect to desired target positions, the robot can achieve precise and reactive visual-based control.

The Python–MATLAB hybrid workflow leverages:

Python for robotics control, real-time communication, and image processing.

MATLAB for heavy matrix computations, Jacobian estimation, and optimization routines.

This repository contains the complete implementation, including:

-IBVS control code

-Vision processing scripts

-MATLAB functions wrapped for Python

-Experiments with the MyCobot 280 Pi

This project serves as a foundation for research and experimentation in vision-based robotics, hybrid computation workflows, and advanced control strategies for compact robotic manipulators.
