# Arduino Garden

The following program detects weeds and plants, implementing OpenCV 
to threshold and find the edges of green objects. As of right now, 
the largest object is considered a plant while any other object above 
a certain size is considered a weed. One of the advantages of this 
program is that it performs under a range (albeit small) of lighting 
conditions. However, one of the disadvantages of using this program is 
that it does not implement any kind of machine learning. I aim to add 
in the future a neural network to identify plants regardless of size.

# About

This was a project inspired by Farmbot and a group called Sustainable Earth 
at Carnegie Mellon University. Overall, it has been a rewarding experience 
to understand to program such a large project in pieces, put everything 
together, and ultimately see some promising results.

# Requirements

1. Python 3.x
2. OpenCV 3.0 or higher (currently using 3.4.1)
3. numpy (latest available version preferred)
4. pillow (image resizing)
5. PyQt5 (for the Raspberry Pi interface)

    For more specific directions: https://raspberrypi.stackexchange.com/questions/62939/pyqt5-on-a-raspberry-pi
    
    PyQt4 is also possible, though the entire interface must be edited for that
    
6. serial (for Arduino communication, currently working on extension)
7. (FUTURE) tensorflow (normally runs on a 64-bit operating system, have not implemented)

# How to use this repo

## ImageControl.Controller Class

```from Image import ImageControl```
```imgControl = ImageControl.Controller()```

Creating a new instance of the Controller will immediately create two objects, 
a Drawer and an Editor. The Drawer handles all drawing and outline 
functions with opencv. The Editor creates different thresholds for image 
processing, and calls the Grip pipeline object for filtering.

```imgControl.image_grab()```

Must be called in order to initialize the image. Can use a given image in the Camera
folder or can take an image with a given camera.

```imgControl.find_plants()```

Finds a plant and weeds based on default thresholds. Future edits will allow for 
changes. Currently, the center-most object is identified as a plant, and all other 
objects identified as weeds. 

```imgControl.draw_all()```

Outlines the plant in green and the weeds in blue, and displays the result.

## ArduinoControl.Controller Class

```from Arduino import ArduinoControl```
```arduinoControl = ArduinoControl.Controller()```

Creating an instance of Controller opens up serial communication with an Arduino.
More testing will improve the consistency of the connection.

```arduinoControl.water_cycle()```

Commands such as watering are still being determined.

# Future Edits
I am continuing to add Arduino communication capabilities to allow one to implement 
the weed detection on a Raspberry Pi. The PyQt5 interface is already implemented on 
Raspberry Pi 3+.
