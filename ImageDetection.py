import cv2
from ImageEdit6 import ImageEditor          # version 4 contains polygon detection
import GripEdit3 as GripEdit            # version 3 only
import ImageHelp


class Detector():

    def __init__(self, thresholdBrightness=.6, weedFactor=1/100):
        self.thresholdBrightness = thresholdBrightness
        self.weedFactor = weedFactor   # size of weeds in comparison to plant
        self.weeds = []

        # Initialized later
        self.regions = None
        self.plant = None
        self.startSize = None
        self.finalImg = None
        self.largeRegions = None

        self.drawImgs = []
        self.drawNames = []

    def image_grab(self, name, cameraNum):
        import time
        '''Grabs an image. Uses an existing image if name is given. Otherwise takes an
            image using a given camera.'''
        if name == None:
            cap = cv2.VideoCapture(cameraNum)
            img = cap.read()[1]
            cv2.imwrite('Capture\\' + str(int(time.time())) + '.jpg', img)
            cap.release()   # When everything done, release the capture
        else:
            img = cv2.imread('Capture\\' + name, 1)
        self.img = img
        self.thresh1 = GripEdit.filter(self.img)
        self.editor = ImageEditor(self.thresh1)

    def find_plant(self):
        '''Finds the largest object and designates as the plant.
            Currently the most inefficient code.'''
        #maxPixel = self.editor.find_max()
        maxPixel = 255
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

    def outline_plant(self):
        color = (0, 255, 0)
        '''Outlines the contour of the plant.'''
        if ImageHelp.equalArray(self.finalImg, None):
            self.finalImg = self.editor.outline(self.img, [self.plant], color,
                                                needToCopy=True)
        else:
            self.editor.outline(self.finalImg, [self.plant], color)

    def outline_weeds(self):
        '''Outlines the contour of each weed.'''
        color = (255, 0, 255)
        if ImageHelp.equalArray(self.finalImg, None):
            self.finalImg = self.editor.outline(self.img, self.largeRegions, color,
                                                needToCopy=True)
        else:
            self.editor.outline(self.finalImg, self.largeRegions, color)

    def draw_outlines(self):
        self.drawImgs.append(self.finalImg)
        self.drawNames.append('self.finalImg')

    def draw_first_threshold(self):
        self.drawImgs.append(self.thresh1)
        self.drawNames.append('self.thresh1')

    def draw_second_threshold(self):
        self.thresh2 = self.editor.combine_regions(self.regions)
        self.drawImgs.append(self.thresh2)
        self.drawNames.append('self.thresh2')

    def display_drawings(self):
        '''Displays a list of images.'''
        imgs = [self.img] + self.drawImgs
        imgNames = ['self.img'] + self.drawNames
        ImageHelp.display(imgNames, imgs)

    @staticmethod
    def detect_all(detector, imgName, cameraNum):
        Detector.image_grab(detector, imgName, cameraNum)
        Detector.find_plant(detector)
        Detector.find_weeds(detector)

    @staticmethod
    def draw_all(detector):
        Detector.outline_weeds(detector)
        Detector.outline_plant(detector)
        Detector.draw_outlines(detector)
        Detector.draw_first_threshold(detector)
        Detector.draw_second_threshold(detector)
        Detector.display_drawings(detector)
