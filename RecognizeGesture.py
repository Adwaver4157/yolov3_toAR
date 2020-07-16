# coding:utf-8


class RecognizeGesture:
    def __init__(self, path):
        self.path = path
        self.dict = {}
        txt = open(self.path)
        while True:
            gesture = txt.readline()
            if not gesture:
                break
            gesture = gesture.strip().split(' ')
            name, definition = gesture[0], gesture[1]
            definition = definition.split(',')
            self.dict[int(name)] = list(map(int, definition))

    def recogniseGesture(self, image):
        return -1

    def showGesture(self):
        for i in range(len(self.dict)):
            print("ジェスチャー"+str(i)+" : ", end='')
            for j in range(len(self.dict[i])//2):
                print(str(self.dict[i][j*2])+"象限, サイン"+str(self.dict[i][j*2+1]), end='')
                if((j+1)*2 == len(self.dict[i])):
                    print()
                else:
                    print(" -> ", end='')
