import numpy as np
import cv2

def make_image():
    class_name = input("enter the class you want to make -> ")
    cap = cv2.VideoCapture(1)  # カメラ番号は多分0か1
    if cap.isOpened():
        print("successfully opened")
        print("make "+class_name)
        while True:
            _, frame = cap.read()
            cv2.imshow("window", frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                cv2.destroyWindow("window")
                break
        cap.release()
    else:
        print("failed to open camera")
        return

    a = input("continue to make images?(y/n) -> ")
    if a == "y":
        make_image()
    else:
        return

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
