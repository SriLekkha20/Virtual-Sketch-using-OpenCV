# Virtual Sketch using OpenCV 🎨

This project lets you draw in the air using a **colored object** (like a blue cap or marker) in front of your webcam.  
The system tracks the object and converts its motion into strokes on a virtual canvas.

## Features

- Real-time color-based object tracking
- Draw in the air – no mouse or touchscreen needed
- Clear the canvas with a single keypress
- Adjustable color range for different markers

## Tech Stack

- Python
- OpenCV
- NumPy

## How It Works

1. The webcam feed is captured and flipped (mirror view).
2. The frame is converted to HSV color space.
3. A mask is created for the chosen color range.
4. The largest contour is treated as the marker.
5. Marker positions are connected across frames to create strokes on a canvas.

## Installation

```bash
git clone https://github.com/<your-username>/virtual-sketch-opencv.git
cd virtual-sketch-opencv
pip install -r requirements.txt
