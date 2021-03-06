import sys,os
import argparse
import math
from PIL import Image
import time
import random

# 创建文件夹
def mkdir(path):
    try:
        os.makedirs(path)
    except:
        pass

# 找出文件夹下所有文件
def listfiles(rootdir, prefix='.xml'):
    file = []
    for parent, dirnames, filenames in os.walk(rootdir):
        if parent == rootdir:
            for filename in filenames:
                if filename.endswith(prefix):
                    file.append(os.path.join(os.path.abspath(parent),filename))
                    # file.append(rootdir + filename)
            return file
        else:
            pass

# 夹角公式
class VectorCompare:
    # 计算矢量大小
    # 计算平方和
    def magnitude(self, concordance):
        total = 0
        for word, count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    # 计算矢量之间的 cos 值
    def relation(self, concordance1, concordance2):
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                # 计算相乘的和
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))


# 将图片转换为矢量
def buildvector(im):
    d1 = {}
    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1


# 生成所有的字母
def gen_all_letters(case_sensitive = False):
    low_set = [chr(x) for x in range(ord('a'), ord('z') + 1)]
    up_set = []
    if case_sensitive:
        up_set = [chr(x) for x in range(ord('A'), ord('Z') + 1)]
    return low_set + up_set



def train(path):
    if not os.path.exists(path):
        print('src path is empty')
    pdir = os.path.dirname(path)
    outdir = os.path.join(pdir,'point')
    mkdir(outdir)

    jpgname = listfiles(path, "jpg")
    for item in jpgname:
        try:
            jpgpath = item
            im = Image.open(jpgpath)
            # jpg不是最低像素，gif才是，所以要转换像素
            im = im.convert("P")
            # 打印像素直方图
            his = im.histogram()
            values = {}
            for i in range(0, 256):
                values[i] = his[i]
            # 排序，x:x[1]是按照括号内第二个字段进行排序,x:x[0]是按照第一个字段
            sorted(values.items(), key=lambda x: x[1], reverse=True)
            # 占比最多的10种颜色
            # for j, k in temp[:10]:
            #     print(j, k)
            # 255 12177
            # 0 772
            # 254 94
            # 1 40
            # 245 10
            # 12 9
            # 236 9
            # 243 9
            # 2 8
            # 6 8
            # 255是白底，0是黑色，可以打印来看看0和254

            # 获取图片大小，生成一张白底255的图片
            im2 = Image.new("P", im.size, 255)

            for y in range(im.size[1]):
                # 获得y坐标
                for x in range(im.size[0]):
                    # 获得坐标(x,y)的RGB值
                    pix = im.getpixel((x, y))
                    # 这些是要得到的数字
                    # 事实证明只要0就行，254是斑点
                    if pix == 0:
                        # 将黑色0填充到im2中
                        im2.putpixel((x, y), 0)
            # 生成了一张黑白二值照片
            # im2.show()
            # 纵向切割
            # 找到切割的起始和结束的横坐标
            inletter = False
            foundletter = False
            start = 0
            end = 0

            letters = []

            for x in range(im2.size[0]):
                for y in range(im2.size[1]):
                    pix = im2.getpixel((x, y))
                    if pix != 255:
                        inletter = True
                if foundletter == False and inletter == True:
                    foundletter = True
                    start = x

                if foundletter == True and inletter == False:
                    foundletter = False
                    end = x
                    letters.append((start, end))

                inletter = False
            # print(letters)
            # [(27, 47), (48, 71), (73, 101), (102, 120), (122, 147), (148, 166)]
            # 打印出6个点，说明能切割成6个字母，正确

            # 保存切割下来的字段
            count = 0
            for letter in letters:
                # (切割的起始横坐标，起始纵坐标，切割的宽度，切割的高度)
                im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))
                # 随机生成0-10000的数字
                a = random.randint(0, 10000)
                # 更改成用时间命名
                file_name = "%s/%s.gif" % (outdir,time.strftime('%Y%m%d%H%M%S', time.localtime()) + str(a))
                im3.save(file_name)
                print('save image:{}'.format(file_name))
                count += 1

        except Exception as err:
            print(err)
            with open(os.path.join(pdir,"error.txt"),"a") as f:
                f.write("\n" + item)

def assign():
    pass

def captcha():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-type", help="[train|assign|captcha]", type=str)
    parser.add_argument("-path",help="deal image path")

    args = parser.parse_args()

    action = args.type
    path = args.path

    mod = sys.modules[__name__] #获取当前模块对象
    # print(getattr(mod,"train"))

    if action in ["train","assign","captcha"]:
        func = getattr(mod,action)
        func(os.path.abspath(path))
    else:
        print("not support")

