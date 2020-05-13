from PIL import Image
import glob
import sys


arg = int(sys.argv[1])  # リサイズ後のサイズ
files = glob.glob("datasets/*.jpg")
output = open("Redatasets/annotation.txt", "w")
for file in files:
    file = file.split("/")[1]
    img = Image.open("datasets/"+file)
    w = arg/img.width
    h = arg/img.height
    img_resize = img.resize((arg, arg))
    try:
        img_resize.save("Redatasets/Re"+file)
    except:
        print(file)
        continue
    text = open("datasets/"+file[:-4]+".txt")
    line = list(map(int, text.readline().split(" ")))
    output.write("Redatasets/Re" + file + " ")
    output.write(str(int(line[1]*w)))
    output.write(",")
    output.write(str(int(line[2]*h)))
    output.write(",")
    output.write(str(int(line[3]*w)))
    output.write(",")
    output.write(str(int(line[4]*h)))
    output.write(",")
    output.write(str(line[0]))
    output.write("\n")
output.close()
