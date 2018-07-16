#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

# 该脚本问分配训练样本到训练文件夹
from PIL import Image
import math
import os
import shutil

from util import listfiles,buildvector,VectorCompare


ERROR_FILE = "../jpg/error.txt"


if __name__ == '__main__':
    numset = ['0','1','2','3','4','5','6','7','8','9']
    symbol_set = []
    iconset = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
               'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    imageset = []
    for letter in iconset:
        for img in os.listdir('../iconset1/%s/' % (letter)):
            temp = []
            if img != "Thumbs.db" and img != ".DS_Store":
                temp.append(buildvector(Image.open("../iconset1/%s/%s" % (letter, img))))
            imageset.append({letter: temp})

    path = "../jpg/letter/"
    jpgname = listfiles(path, "gif")
    # ../jpg/letter/20161210145303813.gif
    for item in jpgname:
        print(item)
        try:
            # 加载训练集
            v = VectorCompare()

            guess = []
            # 这样子写是为了close文件
            # 不然报错：[WinError 32] 另一个程序正在使用此文件，进程无法访问。: '../jpg/letter/201612101452081010.gif'
            im3 = Image.open(item)

            # 将切割得到的验证码小片段与每个训练片段进行比较
            for image in imageset:
                for x, y in image.items():
                    if len(y) != 0:
                        guess.append((v.relation(y[0], buildvector(im3)), x))

            # 排序选出夹角最小的（即cos值最大）的向量，夹角越小则越接近重合，匹配越接近
            guess.sort(reverse=True)
            print("", guess[0])
            # 移动文件
            shutil.copy(item, "../iconset1/%s/" % (guess[0][1]))
        except Exception as err:
            print(err)
            with open()
            # 如果错误就记录下来
            file = open(, "a")
            file.write("\n" + item)
            file.close()
