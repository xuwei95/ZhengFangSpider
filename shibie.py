# coding: utf-8
from PIL import Image
from sklearn.externals import joblib
def img2single(infile, where_save):#将验证码切片成单个字符的四部分并存储
    images = []
    raw_img = Image.open(infile).convert("L")
    x_size, y_size = raw_img.size
    y_size -= 5
    new = raw_img.crop((4, 1, x_size-18, y_size))
    x_size, y_size = new.size
    length = x_size/4
    for i in range(4):
        images.append(new.crop((i*length, 0, (i+1)*length, y_size)))
    for index, img in enumerate(images):
        img.save(where_save+'%s.png' % str(index+1))
def getdata(where_x_pics):
    pic_data = []
    for j in range(4):
        pic_file = where_x_pics + '%s.png' % str(j+1)
        im = Image.open(pic_file)
        width, height = im.size
        result = []
        for h in range(0, height):
            for w in range(0, width):
                pixel = im.getpixel((w, h))
                result.append(pixel)
        pic_data.append(result)
    return pic_data
def shibie(img):
    img2single(img,'save/')
    model='svm.pkl'
    data = getdata('save/')
    clf = joblib.load(model)
    a= clf.predict(data)
    result=''
    for i in range(len(a)):
        result+=a[i]
    return result
