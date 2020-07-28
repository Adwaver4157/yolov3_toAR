from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from objloader import *
import cv2.aruco as aruco
import yaml
import cv2
import os
from kerasyolo3.yolo import YOLO
from RecognizeGesture import RecognizeGesture
import argparse
from ar import GestureAR
import numpy as np


class OpenGL():
    INVERSE_MATRIX = np.array([[1.0, 1.0, 1.0, 1.0],
                               [-1.0, -1.0, -1.0, -1.0],
                               [-1.0, -1.0, -1.0, -1.0],
                               [1.0, 1.0, 1.0, 1.0]])

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.object = None
        self.texture_background = None

        ####
        self.cam_matrix, self.dist_coefs, revecs, tvecs = self.get_cam_matrix(
            "camera_matrix_aruco.yaml")

    def get_cam_matrix(self, file):
        with open(file) as f:
            loadeddict = yaml.load(f)
            cam_matrix = np.array(loadeddict.get('camera_matrix'))
            dist_coeff = np.array(loadeddict.get('dist_coeff'))
            rvecs = np.array(loadeddict.get('rvecs'))
            tvecs = np.array(loadeddict.get('tvecs'))
            return cam_matrix, dist_coeff, rvecs, tvecs

    def init_gl(self, Width, Height):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(37, 1.3, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

        glLightfv(GL_LIGHT0, GL_POSITION, (-40, 300, 200, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)

        # load 3D object
        File = 'Sinbad_4_000001.obj'
        self.object = OBJ(File, swapyz=True)

        # assign texture
        glEnable(GL_TEXTURE_2D)
        self.texture_background = glGenTextures(1)

    def draw_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # get frame
        _, image = self.cap.read()

        # convert image to appropriate format
        bg_image = cv2.flip(image, 0)  # flip upside down
        bg_image = Image.fromarray(bg_image)
        x = bg_image.size[0]
        y = bg_image.size[1]
        ####
        bg_image = bg_image.tobytes("raw", "BGRX", 0, -1)

        glBindTexture(GL_TEXTURE_2D, self.texture_background)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, x, y, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, bg_image)
        # draw texture_background
        glBindTexture(GL_TEXTURE_2D, self.texture_background)
        glPushMatrix()
        glTranslatef(0.0, 0.0, -10.0)
        self.draw_background()
        glPopMatrix()

        # draw object
        image = self.handle_glyphs(image)

        glutSwapBuffers()

    def handle_glyphs(self, image):

        # aruco settings
        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        result, mClass, mBox = yolo.detect_image(image)
        if mClass is not None:
            cv2.rectangle(result, (mBox[1], mBox[0]),
                          (mBox[3], mBox[2]), (0, 0, 255))
        gesture_name = rg.recognizeGesture(result, mBox, mClass)
        if gesture_name is not None:
            gesture_ar.fix_render(image)
            if gesture_name >= 2:
                image = gesture_ar.operate_ar(image, mBox, gesture_name)
        ####

        height, width, channel = image.shape
        corners, ids, _ = aruco.detectMarkers(image, aruco_dict)
        if ids is not None and corners is not None:
            rvecs, tvecs, _objpoints = aruco.estimatePoseSingleMarkers(
                corners[0], 0.6, self.cam_matrix, self.dist_coefs)
            rmtx = cv2.Rodrigues(rvecs)[0]

            view_matrix = np.array([[rmtx[0][0], rmtx[0][1], rmtx[0][2], tvecs[0][0][0]],
                                    [rmtx[1][0], rmtx[1][1], rmtx[1]
                                        [2], tvecs[0][0][1]],
                                    [rmtx[2][0], rmtx[2][1], rmtx[2]
                                        [2], tvecs[0][0][2]],
                                    [0.0, 0.0, 0.0, 1.0]])
            view_matrix = view_matrix * self.INVERSE_MATRIX
            view_matrix = np.transpose(view_matrix)

            glPushMatrix()
            glLoadMatrixd(view_matrix)
            glCallList(self.object.gl_list)
            glPopMatrix()
        # optional(yolo)
        cv2.imshow("cv2 frame", image)
        cv2.waitKey(1)

    def draw_background(self):
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-4.0, -3.0, 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(4.0, -3.0, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(4.0, 3.0, 0.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-4.0, 3.0, 0.0)
        glEnd()

    def ex(self):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()

    def main(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(250, 150)
        self.window = glutCreateWindow(b"OpenGL")
        glutDisplayFunc(self.draw_scene)
        glutIdleFunc(self.draw_scene)
        self.init_gl(640, 480)
        glutKeyboardFunc(self.ex)
        glutMainLoop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    current_path = os.getcwd()
    parser.add_argument(
        '--model_path', type=str,
        help='path to model weight file, default ' +
        YOLO.get_defaults("model_path")
    )
    parser.add_argument(
        '--anchors_path', type=str,
        help='path to anchor definitions, default ' +
        YOLO.get_defaults("anchors_path")
    )
    parser.add_argument(
        '--classes_path', type=str,
        help='path to class definitions, default ' +
        YOLO.get_defaults("classes_path")
    )
    parser.add_argument(
        '--gestures_path', type=str,
        help='path to gesture definition, default ' +
        'kerasyolo3/model_data/gestures.txt'
    )
    FLAGS = vars(parser.parse_args())
    for arg in FLAGS:
        FLAGS[arg] = os.path.join(current_path, FLAGS[arg])
    print(FLAGS)

    gestures_path = FLAGS.pop("gestures_path")

    # create YOLO and RecognizeGesture
    yolo = YOLO(**FLAGS)
    rg = RecognizeGesture(gestures_path)
    rg.showGesture()
    gesture_ar = GestureAR()

    # create OpenGL
    openGL = OpenGL()
    openGL.main()
