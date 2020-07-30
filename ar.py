import cv2
import numpy as np
from PIL import Image


class GestureAR():
    def __init__(self):
        self.flag = False
        self.position = None
        self.qr = Image.fromarray(cv2.imread('ar.png'))

    def operate_ar(self, image, box, gesture_name):
        top, left, bottom, right = box
        x = (left + right) / 2
        y = (top + bottom) / 2
        _image = Image.fromarray(image)

        if gesture_name == 'moveAR' and not self.flag:
            _image.paste(self.qr, (int(x), int(y)))
            self.flag = True
        elif gesture_name == 'putAR' and self.flag:
            self.position = (x, y)
            self.flag = False
        elif gesture_name == 4:
            self.position = None
        else:
            return image

        image = np.asarray(_image)
        return image

    def fix_render(self, image):
        _image = Image.fromarray(image)

        if self.position is not None:
            _image.paste(self.qr, (int(self.position[0]), int(self.position[1])))
        else:
            return image

        image = np.asarray(_image)
        return image
