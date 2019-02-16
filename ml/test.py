from sklearn.externals import joblib
from PIL import Image
import numpy as np
model = joblib.load("svm.pkl")


def predict(img):
    images = []
    img = Image.open(img).convert("L")
    x_size, y_size = img.size
    y_size -= 5
    new = img.crop((4, 1, x_size - 18, y_size))
    x_size, y_size = new.size
    length = x_size // 4
    for i in range(4):
        single = new.crop((i * length, 0, (i + 1) * length, y_size))
        single = np.array(single).reshape(1, 12 * 21)
        images.append(single)
    result = ''
    for i in images:
        result += model.predict(i)[0]
    return result


if __name__ == '__main__':
    a = predict('code.jpg')
    print(a)
