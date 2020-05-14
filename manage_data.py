
import numpy as np
import cv2

def make_image():
    cap = cv2.VideoCapture(1)
    if cap.isOpened():
        print("Camera was successfully opened")     


def delete_image():
    print(2)

def save_image(c, img):
    pass

def main():
    s = input("make or delete? -> ")
    if s == "make":
        make_image()
    elif s == "delete":
        delete_image()
    else:
        print("invalid input")

if __name__ == '__main__':
    main()
