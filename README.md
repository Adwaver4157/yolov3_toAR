# kerasyolo3 のチュートリアル

以下の colab をコピーして学習、テストすることができます
https://colab.research.google.com/drive/1pi7Iskwi2G_nYMithtQFPoyqWzQ6BFmp?usp=sharing

## YOLO 系のコードに関して

keras 版 YOLOv3 モデルとして著名な次のコードを改修して使用しています。

https://github.com/qqwweee/keras-yolo3

## AR 系のコードに関して

次のコードを使用させていただいています。

https://github.com/ajaymin28/Aruco_python

yolo_ar.py に関しては各種いじっており、
objloader や calibration 関連はそのまま使用させてもらってます。

## ディレクトリ構成

```
yolov3_toAR/
  |
  ┝ README.md
  ┝ kears-yolov3
  |     |
  |     ┝ model_data
  |          ┝ yolo_anchor.txt
  |          ┝ ~~~~.h5 <- 学習済モデル
  ┝ resize.py
  ┝ manage_data.py <- ImagesとAnnotationを作成してくれる
  |
  sample
  | |
  | ┝ datasets         ┐
  | ┝ class_name.txt   | resize.pyで自動的に作られる
  | ┝ train.txt        ┘
  | |
  | |
  | ┝ Images <- manage_data.pyで作る(ここではhttp://vision.stanford.edu/aditya86/ImageNetDogsから持ってくる)
  | |   ┝ class01 <-クラス名はなんでもいい(ここではもとから命名されている)
  | |   |   ┝ img1.jpg
  | |   |   ...
  | |   |   └ img1000.jpg
  | |   ┝ class02
  | |   |   ┝ img1.jpg
  | |   |   ...
  | |   |   └ img1000.jpg
  | |   ...
  | |
  | └ Annotation
  |     ┝ class01 <-Images内のディレクトリに対応する名前
  |     |   ┝ class01.txt <- クラス内の画像の総数や、更新情報
  |     |   ┝ img1.txt <- Images内の同名画像のannotation(書式は下)
  |     |   ...
  |     |   └ img1000.txt
  |     ┝ class02
  |     |   ┝ class02.txt
  |     |   ┝ img1.txt
  |     |   ...
  |     |   └ img1000.txt
  |     ...
  |
  Hand <-その他、自分で作ったプロジェクト(sampleと同様の構成)
  | |
  |  ...
  ...
```

### annotation の書式

```
x_min,y_min,x_max,y_max
```

対象を囲う最小の box についての x の最小、y の最小、、、をカンマ区切りで書く  
（犬のを持ってくるときはそのままで大丈夫、ただし resize.py の内容の「普段」というところをコメントアウトして、「犬」のところを有効にする）

## manage_data.py の使い方

### ターミナル上

1. make or delete => データを作成するか削除するかを選ぶ(現状 make のみ)
2. enter project name => プロジェクト名を入力(kerasyolo3 および sample 以外)
3. enter class name =>　作りたいクラス名を入力(新規でも既存でも大丈夫)
4. successfully opend => カメラが開けた
   failed to open => カメラが開けない、11 行目の数字をいじる

### window 上

- 緑色の枠に目標物を入れる
- 枠の移動は

```
a:左、s:下、d:右、w:上、n:縮小、m:拡大
```

- x を押すと枠が赤くなる -> 赤い間は画像が保存される
- もう一度 x を押すと緑に戻る
- 止める時は q を押す

### ターミナル上

1. continue to make images?　=> 他のクラスを作りたいなら y、そうでないなら n
2. y なら上記の操作を繰り返す

## resize.py の使い方

### 引数

```
-p,--project_name       : リサイズしたい画像のプロジェクト名
-W,--width              : リサイズ後の横の長さ(32の倍数)
-H,--height             : リサイズ後の縦の長さ(32の倍数、Widthと同じ時省略できる)
-n,--number_of_classes  : 使用したいクラス数(0の時、全てのクラスを使う)
```

### !!注意!!

- datasets ディレクトリが存在すると error になる => 事前に datasets がない状態にする(コンフリクトを避けるため)

## ジェスチャー認識による AR 操作（yolo_ar.py の使い方）

### 環境構築

入れるのが難しいものがあるので、後で詳細を追記します

```
imutils==0.5.3
opencv-contrib-python==4.2.0.34
Pillow==7.1.2
pygame==1.9.6
PyOpenGL==3.1.5
PyOpenGL-accelerate==3.1.5
PyYAML==5.3.1
```

### 事前準備(工事中)

1. calibration のディレクトリに移動し、main.py を実行してください。
2. 生成された camera_matrix_aruco.yaml を一番上のディレクトリ（yolov3_toAR）に移動させてください。

### 3D モデルについて

- 描画したい 3D モデルは、一番上のディレクトリ（yolov3_toAR）に対応する.mtl ファイルと.ogj ファイルをおいてください。

### 実行の仕方

```
~/.../yolov3_toAR$ python yolo_ar.py --gestures_path (ジェスチャーパス)
```
