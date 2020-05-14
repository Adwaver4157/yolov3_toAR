# keras-yolo3 のチュートリアル

以下の colab をコピーして学習、テストすることができます
https://colab.research.google.com/drive/1pi7Iskwi2G_nYMithtQFPoyqWzQ6BFmp?usp=sharing


# ディレクトリ構成
```
yolov3_toAR/
  ┝ README.md
  ┝ kears-yolov3
  ┝ Images
  |   ┝ class01 <-クラス名はなんでもいい
  |   |   ┝ class01.txt
  |   |   ┝ img1.jpg
  |   |   ...
  |   |   └ img1000.jpg
  |   ┝ class02 <-クラス名はなんでもいい
  |   |   ┝ class02.txt
  |   |   ┝ img1.jpg
  |   |   ...
  |   |   └ img1000.jpg
  ┝ Annotation
  |   ┝ ch01 <- 担当チャプター
  |   |   ┝ input <- 入力画像
  |   |   |   ┝ imori.jpg
  |   |   |   ┝ imori_noise.jpg
  |   |   |   ...
  |   |   |
  |   |   ┝ solution <- ソースコード
  |   |   |   ┝ solution01.py
  |   |   |   ┝ solution02.py
  |   |   |   ...
  |   |   |
  |   |   ┝ answer <- 出力画像(答え)
  |   |   |   ┝ answer01.jpg
  |   |   |   ┝ answer02.jpg
  |   |   |   ...
  |   |   |   
  |   |   └ supplement <- 補足資料(必要であれば)

  |   ...
```
