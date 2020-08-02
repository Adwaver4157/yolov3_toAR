import cv2
import numpy as np
from PIL import Image


class GestureAR():
    def __init__(self):
        self.flag = False
        self.position = None

    def operate_ar(self, box, gesture_name):
        top, left, bottom, right = box
        x = (left + right) / 2
        y = (top + bottom) / 2 + 40

        if gesture_name == 'moveAR' and not self.flag and self.position is None:  # trace mode
            render_position = np.array([[[x - 50, y - 50], [x + 50, y - 50], [x + 50, y + 50], [x - 50, y + 50]]]
                                       ).astype(np.float32)
            self.flag = True

        elif gesture_name == 'resetAR' and not self.flag:  # reset mode
            self.position = None
            render_position = None
        else:
            return None

        return render_position

    def trace_render(self, box, class_num):
        top, left, bottom, right = box
        x = (left + right) / 2
        y = (top + bottom) / 2 + 40

        if class_num == 1 and self.flag:
            render_position = np.array([[[x - 50, y - 50], [x + 50, y - 50], [x + 50, y + 50], [x - 50, y + 50]]]
                                       ).astype(np.float32)
        elif class_num == 2 and self.flag:  # fix mode
            render_position = np.array([[[x - 50, y - 50], [x + 50, y - 50], [x + 50, y + 50], [x - 50, y + 50]]]
                                       ).astype(np.float32)
            self.position = (x, y)
            self.flag = False
        else:
            return None

        return render_position

    def fix_render(self):

        if self.position is not None:
            x = self.position[0]
            y = self.position[1]
            render_position = np.array([[[x - 50, y - 50], [x + 50, y - 50], [x + 50, y + 50], [x - 50, y + 50]]]
                                       ).astype(np.float32)
        else:
            return None

        return render_position
