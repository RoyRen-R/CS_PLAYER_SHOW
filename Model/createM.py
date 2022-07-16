# -*- coding: utf-8 -*- 
# @Time : 2022/7/12 18:56
# @Author : 任浩天
# @File : Cmodel.py

import numpy as np
from sklearn import preprocessing
import os
import cv2 as cv

face_faces = cv.CascadeClassifier('G:/ProJect/data3/cascade_files/haarcascade_frontalface_alt.xml')


# 为图片做好标记，将文字变为数字，序号转为文字，再训练
class LabelEncoder:
    # 文字到数字
    def encode_labels(self, labeL_words):
        self.le = preprocessing.LabelEncoder()
        self.le.fit(labeL_words)

    # 文字转换为数字位置
    def word_to_num(self, label_word):
        return self.le.transform([label_word])[0]

    # 将位置转换为文字
    def num_to_word(self, label_num):
        return self.le.inverse_transform([label_num])[0]


# 读取文件及标识
def get_images_and_labels(input_data):
    label_words = []
    for root, dirs, files in os.walk(input_data):
        # 取.jpg格式的文件循环
        for filename in (x for x in files if x.endswith(".jpg")):
            filepath = os.path.join(root, filename)  # 路径与文件拼接起来
            label_words.append(filepath.split("\\")[-2])  # 取文件上一级文件夹的人名
    # 编码
    le = LabelEncoder()
    le.encode_labels(label_words)
    images = []  # 人脸灰度图像保存
    labels = []  # 图像对应的人名的数组中序号
    for root, dirs, files in os.walk(input_data):
        for filename in (x for x in files if x.endswith(".jpg")):
            filepath = os.path.join(root, filename)  # 路径与文件拼接起来
            '''
            中文识别
            '''
            image = cv.imdecode(np.fromfile(filepath, dtype=np.uint8), 0)
            # 读入灰度图像
            # 获取人脸标记
            name = filepath.split("\\")[-2]
            # 检测是否有人脸，并获取人脸数据
            faces = face_faces.detectMultiScale(image, 1.1, 5)
            # 输入每个人脸的数据
            for x, y, w, h in faces:
                images.append(image[y:y + h, x:x + w])
                labels.append(le.word_to_num(name))
    return images, labels, le


if __name__ == '__main__':
    input_path = '../data3/faces_dataset/train'  # 训练集的路径
    # 人脸识别训练初始化工作
    recognizer = cv.face.LBPHFaceRecognizer_create()
    # 取得用来训练的数据
    images, labels, le = get_images_and_labels(input_path)
    print(labels)
    # 开始模型训练
    print('使用训练集对模型进行训练')
    recognizer.train(images, np.array(labels))
    # 保存训练的模型
    recognizer.save('my_LBPHFaceRecognizer.xml')