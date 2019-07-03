import random
import os
import cv2
import numpy as np
import pickle
from matplotlib import style
from AI_KNearestAlogrithm import Classifier
np.set_printoptions(threshold=np.inf, suppress=True)
style.use('fivethirtyeight')


class FacialClassifier:
    def __init__(self):
        self.frame_array = []
        self.face = []
        self.face_cascade = cv2.CascadeClassifier('C:\\Users\\DELL\\Python\\#DM\\haarcascade_frontalface_default.xml')

    def pick(self, pickle_file):
        if os.path.isfile(pickle_file):
            with open(pickle_file, 'rb') as f:
                self.frame_array = pickle.load(f)
        else:
            raise FileNotFoundError("Pickle file not found. ")

    def crop_face(self, img):
        array = []
        i = 0
        while array == []:
            i += 1
            faces = self.face_cascade.detectMultiScale(img, 1.3, 5)
            for (x, y, a, b) in faces:
                array = img[y:y+b, x:x+b]
            if i == 5:
                return img
        return array

    def process_img(self, frame):
        face = self.crop_face(frame)
        grey_face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        # frame = clahe.apply(grey_face)
        # f = cv2.equalizeHist(frame)
        frame = cv2.resize(face, (200, 200))
        # print(f)
        # cv2.imshow('window', frame)
        # cv2.waitKey(0)
        # frame_eigenvalue, frame_eigenvector = np.linalg.eig(frame)
        return frame

    def fit(self, directory=''):
        pics = os.listdir(directory)
        pics.remove('desktop.ini')
        random.shuffle(pics)
        # pics.remove('desktop.ini')
        groups = []
        for pic in pics:
            if pic[0] not in groups:
                groups.append(pic[0])
        for g in groups:
            similar = []
            i = 0
            for pic in pics:
                group = pic[0]
                print('detecting face ' + str(i + 1) + ' of ' + str(len(pics)))
                if group == g:
                    try:
                        frame = cv2.imread(directory + '\\' + pic)
                        frame_value = self.process_img(frame)
                        similar.append(frame_value.astype('int64'))
                    except:
                        pass
                i += 1
            self.frame_array.append([g, similar])
        return self.frame_array

    def return_face(self):
        return self.face

    def cache(self, pickle_file):
        with open(pickle_file, 'wb') as f:
            pickle.dump(self.frame_array, f)

    def recognize(self, image_dir=''):
        frame = []
        if image_dir == '':
            img = cv2.VideoCapture(0)
            for i in range(40):
                check, frame = img.read()
        else:
            frame = cv2.imread(image_dir)
        self.face = frame
        cv2.imshow('window', frame)
        cv2.waitKey(0)
        frame_eigenvalue = self.process_img(frame)
        CLR = Classifier(self.frame_array, opt='list')
        result = CLR.predict(frame_eigenvalue, 3)
        return result


class FacialNN:
    def __init__(self, X, Y, w1, b1):
        self.x = np.array(X)
        self.y = np.array(Y)
        self.w1 = np.array(w1)
        # self.w2 = np.array(w2)
        self.b1 = np.array(b1)
        # self.b2 = np.array(b2)
        self.L1 = np.array([])
        self.L2 = np.array([])

    def sigmoid(self, x):
        return 1 / (1 + np.e ** -x)

    def sigmoid_der(self, x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))

    def preprocess(self, directory='', remove="desktop.ini", parts=6):
        X = [[], [], [], [], [], []]
        Y = []
        if directory != '':
            pics = os.listdir()
            random.shuffle(pics)
            pics.remove(remove)
            for pic in pics:
                # print(pic)
                frame = cv2.imread(directory + '\\' + pic)
                grey_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                frame = cv2.resize(grey_frame, (234, 234))
                part_size = int(frame.shape[0] / parts)
                j = i = 0
                for _ in range(6):
                    print(i + part_size)
                    frame_part = frame[i:i + part_size, j:j + part_size]
                    X[_].append(frame_part)
                    i += part_size
                    j += part_size


        self.x = X

    def cache(self, pickle_file):
        with open(pickle_file, 'wb') as f:
            pickle.dump(self.x, f)

    def feed_forward(self):
        # Layer 1:
        self.WX11 = WX11 = np.dot(self.w1[0], self.x[0]) + self.b1[0]
        self.WX12 = WX12 = np.dot(self.w1[1], self.x[1]) + self.b1[1]
        # self.WX13 = WX13 = np.dot(self.w1[2], self.x[2]) + self.b1[2]
        L1 = self.sigmoid(WX11 + WX12 + self.b1[3])
        self.L2 = L1

        # Layer 2:
        # WX21 = np.dot(self.w2[0], L1)
        # WX22 = np.dot(self.w2[1], L1)
        # WX23 = np.dot(self.w2[2], L1)
        # self.L2 = self.sigmoid(WX21 + WX22 + WX23 + self.b2)

    def back_propagation(self):
        error = ((self.L2 - self.y)**2)/2
        loss = error.sum()
        print(loss)

        # WX11
        d1 = self.sigmoid_der(self.WX11)# self.sigmoid_der(self.WX11)
        d2 = d1 * error
        d3 = np.dot(d2, self.x[0].T)
        # WX12
        d4 = self.sigmoid_der(self.WX12)# self.sigmoid_der(self.WX11)
        d5 = d4 * error
        d6 = np.dot(d5, self.x[1].T)

        # Updates:
        self.w1[0] += d3
        # self.w2[1] -= d6

    #
    # def return_weights(self):
    # def predict(self):


X = [[[1,0,1], [0,0,0]], [[1,1,1], [0,1,1]]]
Y = [1,0,1]
w1 = np.random.rand(2,2)
b1 = [0.3, 0.2, 0.1, 0.5]

def main():
    FNN = FacialNN(X, Y, w1, b1)
    for i in range(60000):
        FNN.preprocess('C:\\Users\\DELL\\Pictures\\Camera Roll')
        FNN.feed_forward()
        FNN.back_propagation()


if __name__ == '__main__':
    main()




