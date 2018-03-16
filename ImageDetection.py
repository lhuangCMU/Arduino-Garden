import numpy as np
import cv2
import ImageEdit6 as ImageEdit          # version 4 contains polygon detection
import ImageGrab2 as ImageGrab
import GripEdit3 as GripEdit            # version 3 only
import ImageHelp

class Detector():

    def __init__(self):
        '''Calibration and set-up'''
        self.plantLocations = [(), (), (), ()]
        self.numPlants = len(self.plantLocations)
        self.lastWater = None
        self.img = self.image_grab()
        self.imgEdit = GripEdit.filter(self.img)
        self.editor = ImageEdit.Editor(self.imgEdit)
        self.thresholdBrightness = .4       # .6 is the default value
        self.weeds = []
        self.weedFactor = 1/100   # size of weeds in comparison to plant

        # Initialized later
        self.regions = None
        self.plant = None
        self.startSize = None
        self.finalImg = None
        self.largeRegions = None

    def image_grab(self):
        img = ImageGrab.grab(0)     # built-in camera number = 0
                                    # attached camera number = 1
        #img = cv2.imread('Capture\\1521224317.jpg', 1)
        return img

    def find_plant(self):
        '''Finds the largest object and designates as the plant.
            Currently the most inefficient code.'''
        maxPixel = self.editor.find_max()
        while True:
            locations = self.editor.max_locations(maxPixel, self.thresholdBrightness)
            self.regions = self.editor.get_all_regions(locations)

            # Find the largest region. In the case of a tie, lower the brightness threshold.
            (largestRegion, self.startSize) = self.editor.obtain_largest_region(self.regions)
            if len(largestRegion) == 1:
                break
            else:
                self.thresholdBrightness -= .01
        self.plant = largestRegion[0]        # set the largest region as the plant

    def find_weeds(self):
        '''Determine if an object is a plant or a weed. Currently, the plant is removed, and everything
            else is designated as a weed.'''
        plantFound = False
        plantIndex = None
        self.largeRegions = self.editor.keep_large_regions(self.regions, self.startSize * self.weedFactor)
        for index in range(len(self.largeRegions)):
            region = self.largeRegions[index]
            newLocation = self.editor.find_centroid(region)
            if not plantFound and ImageHelp.equalArray(region, self.plant):
                print("Location of plant:", newLocation)
                plantFound = True
                plantIndex = index
            else:
                self.weeds.append(newLocation)
        self.largeRegions.pop(plantIndex)
        print("Locations of weeds:", self.weeds)

    def draw_plant(self):
        '''Outlines the contour of the plant.'''
        if ImageHelp.equalArray(self.finalImg, None):
            self.finalImg = self.editor.outline(self.img, [self.plant],
                                                needToCopy=True)
        else:
            self.editor.outline(self.finalImg, [self.plant])

    def draw_weeds(self):
        '''Outlines the contour of each weed.'''
        if ImageHelp.equalArray(self.finalImg, None):
            self.finalImg = self.editor.outline(self.img, self.largeRegions,
                                                needToCopy=True)
        else:
            self.editor.outline(self.finalImg, self.largeRegions)

    def display_drawings(self):
        '''Displays a list of images.'''
        imgNames = ['self.img', 'self.imgEdit', 'self.finalImg']
        imgs = [self.img, self.imgEdit, self.finalImg]
        ImageHelp.display(imgNames, imgs)