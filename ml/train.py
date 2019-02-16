from PIL import Image
import numpy as np
import os
from sklearn import svm
from sklearn.externals import joblib


def load_data():
    x_data = []
    y_data = []
    for label in os.listdir('data'):
        for i in os.listdir('data/%s' % label):
            img = Image.open('data/%s/%s' % (label, i))
            x = np.array(img).reshape(21 * 12)
            x_data.append(x)
            y_data.append(label)
    x_data = np.array(x_data)
    y_data = np.array(y_data)
    return x_data, y_data


if __name__ == '__main__':
    x_data, y_data = load_data()
    model = svm.LinearSVC()
    model.fit(x_data, y_data)
    joblib.dump(model, "svm.pkl")
