"""
引数は size class_num
例えば 320 10
"""

import glob
import sys
from PIL import Image

#Images内のクラスごとにdatasets,class_name.txt,train.txtを作る

size = int(sys.argv[1])  # リサイズ後のサイズ
class_num_limit = int(sys.argv[2])  # Image内で使うクラス数（出てきた順に使う）
classes = glob.glob("Images/*")
class_name = open("class_name.txt", "w")
train = open("train.txt", "w")

img_num = 1
class_num = 0

for c in classes:
    class_num += 1

    #class_nameへの書き込み(クラス名)
    class_name.write(c.split("/")[1])
    class_name.write("\n")

    files = glob.glob(c+"/*")
    for f in files:  # imageの名前
        f_split = f.split("/")

        #画像のリサイズ
        img = Image.open(f)
        w = size/img.width
        h = size/img.height
        img_resize = img.resize((size, size))
        try:
            img_resize.save("datasets/image"+str(img_num)+".jpg")
        except Exception as e:
            print(e)
            continue

        text = open("Annotation/"+f_split[1]+"/"+f_split[2][:-4])

        #犬↓
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
        #犬↑
        #普段使う方↓
        """
        #trainへの書き込み(annotation)
        line = list(map(int, text.readline().split(",")))
        """
        #普段使う方↑
        train.write("datasets/image" + str(img_num) + ".jpg ")
        train.write(str(int(line[0]*w)))
        train.write(",")
        train.write(str(int(line[1]*h)))
        train.write(",")
        train.write(str(int(line[2]*w)))
        train.write(",")
        train.write(str(int(line[3]*h)))
        train.write(",")
        train.write(str(class_num))
        train.write("\n")

        img_num += 1
    if class_num == class_num_limit:
        break
train.close()
