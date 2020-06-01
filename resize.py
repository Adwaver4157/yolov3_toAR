"""
Images, Annotation内にある画像をリサイズする

** datasetsディレクトリがないときerrorとなる **

Args:
        Width: リサイズ後の横の長さ(32の倍数)
        Height: リサイズ後の縦の長さ(32の倍数、Widthと同じ時省略できる)
        Number of classess: 使用したいクラス数(0の時、全てのクラスを使う)
        ex) resize.py 640 320 10

"""

import glob
import sys
import os
from PIL import Image

width = int(sys.argv[1])
height = int(sys.argv[2]) if len(sys.argv) == 4 else width

if width%32 != 0 or height%32 != 0:
    print('Width and Height must be multiple of 32')
else:
    class_num_limit = int(sys.argv[-1])
    class_directories = glob.glob(os.path.join("Images", "*"))
    class_name_txt = open("class_name.txt", "w")
    train_txt = open("train.txt", "w")

    img_num = 1
    class_num = 0

    for class_path in class_directories:
        class_name = os.path.basename(class_path)

        #class_name.txtへの書き込み(クラス名)
        class_name_txt.write(class_name)
        class_name_txt.write("\n")

        img_files = glob.glob(os.path.join(class_path, "*"))

        for img_path in img_files:
            img_name = os.path.basename(img_path)

            #画像のリサイズ
            img = Image.open(img_path)
            w = width/img.width
            h = height/img.height
            img_resize = img.resize((width, height))
            try:
                img_resize.save(os.path.join("datasets", "image"+str(img_num)+".jpg"))
            except Exception as e:
                print(e)
                continue

            #犬↓
            """
            text = open(os.path.join("Annotation", class_name, os.path.splitext(img_name)[0]))
            for i in range(18):
                text.readline()
            line = [0]*4
            for i in range(4):
                s = text.readline().strip()[6:-7]
                line[i] = int(s)
            for i in range(3):
                a = text.readline().strip()
            if "object" in a:  # 複数の犬がいるのは使わない
                continue
            """
            #犬↑
            #普段使う方↓

            text = open(os.path.join("Annotation", class_name, os.path.splitext(img_name)[0]+'.txt'))
            line = list(map(int, text.readline().split(",")))

            #普段使う方↑

            #train.txtへの書き込み(annotation)
            train_txt.write(os.path.join("datasets", "image"+str(img_num)+".jpg"))
            train_txt.write(str(int(line[0]*w)))
            train_txt.write(",")
            train_txt.write(str(int(line[1]*h)))
            train_txt.write(",")
            train_txt.write(str(int(line[2]*w)))
            train_txt.write(",")
            train_txt.write(str(int(line[3]*h)))
            train_txt.write(",")
            train_txt.write(str(class_num))
            train_txt.write("\n")

            img_num += 1

        class_num += 1
        if class_num == class_num_limit:
            break

    train_txt.close()
