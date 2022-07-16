# -*- coding: utf-8 -*- 
# @Time : 2022/7/12 18:59 
# @Author : 任浩天
# @File : main.py
import os
from Model.Rating import predict
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from pyqt5_plugins.examplebutton import QtWidgets
from sklearn import preprocessing

from SQL import SQL_name,SQL_player_data
from Ui import login, DataShow


# 登录窗口
class login_action(QMainWindow, login.Ui_MainWindow):
    def __init__(self,next_win):
        super().__init__()
        self.setupUi(self)
        self.timer = QtCore.QTimer()
        self.pre_name = ''
        self.timer.timeout.connect(self.show_viedo)
        self.pushButton.clicked.connect(self.video_button)
        self.pushButton_2.clicked.connect(self.change_win)
        self.cap_video = 0
        self.flag = 0
        self.img = []
        self.next_win = next_win

    def change_win(self):
        # 数据库中存储的人的姓名
        ls = SQL_name.SQL_name()
        names = ls.name
        if self.pre_name in names:
            self.timer.stop()
            self.label.clear()
            self.cap_video.release()
            self.close()
            cv2.destroyAllWindows()
            self.next_win.show()

    def video_button(self):
        if self.flag == 0:
            self.cap_video = cv2.VideoCapture(0)
            self.timer.start(50)
            self.flag += 1
            self.pushButton.setText("关闭人脸识别")
        else:
            self.timer.stop()
            self.cap_video.release()
            self.label.clear()
            self.pushButton.setText("打开人脸识别")
            self.flag = 0

    def show_viedo(self):
        ret, self.img = self.cap_video.read()
        predict_image = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        faces = face_faces.detectMultiScale(predict_image, 1.1, 5)
        for x, y, w, h in faces:
            # 识别
            predicated_index, conf = recognizer.predict(predict_image[y:y + h, x:x + w])
            if conf < 40:
                predicated_name = le.num_to_word(predicated_index)
                self.pre_name = predicated_name
                cv2.rectangle(self.img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.rectangle(self.img, (x, y + h - 35), (x + w, y + h), (0, 0, 255), 2)
                # 中文显示
                img = Image.fromarray(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))
                # 创建一个可以在图像上绘图的对象
                draw = ImageDraw.Draw(img)
                # 字体的格式
                fontstyle = ImageFont.truetype('../resources/华文黑体.ttf', 25, encoding='utf-8')
                # 绘制文本
                draw.text((x + 6, y + h - 28), predicated_name, (255, 255, 255), font=fontstyle)
                # 转换为cv的图片
                self.img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
            else:
                name = '???'
                cv2.putText(self.img, name, (x + 6, y + h - 6), cv2.FONT_HERSHEY_DUPLEX, 1.5,
                            (255, 255, 255), 2)
        if ret:
            self.show_cv_img(self.img)

    def show_cv_img(self, img):
        shrink = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        qtimg = QtGui.QImage(shrink.data,
                             shrink.shape[1],
                             shrink.shape[0],
                             shrink.shape[1] * 3,
                             QtGui.QImage.Format_RGB888)
        jpg_out = QtGui.QPixmap(qtimg).scaled(
            self.label.width(), self.label.height())
        self.label.setPixmap(jpg_out)


# 数据显示窗口
class Datashow_action(QMainWindow, DataShow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_1.clicked.connect(self.get_showdata)
        self.pushButton_2.clicked.connect(self.get_query)
        self.pushButton_3.clicked.connect(self.get_predict)
        self.pushButton2.clicked.connect(self.get_payer_data)
        self.pushButton31.clicked.connect(self.predict_rating)

    def predict_rating(self):
        kast = float(self.lineEdit.text().strip())
        kill_round = float(self.lineEdit_2.text().strip())
        death_round = float(self.lineEdit_3.text().strip())
        damage_round = float(self.lineEdit_4.text().strip())
        impact = float(self.lineEdit_5.text().strip())
        print(kast, kill_round, death_round, damage_round, impact)
        rating = predict(damage_round, kast, impact, kill_round, death_round)
        rating = str(rating[0][0])
        self.label_2.setText(rating)

    def get_payer_data(self):
        name = self.lineEdit21.text()
        data = SQL_player_data.player_data().data
        payer_data = ()
        for i in data:
            if i[0] == name:
                payer_data = i
                break
        for j in range(1, len(payer_data)):
            item = QtWidgets.QTableWidgetItem(str(payer_data[j]))
            self.tableWidget2.setItem(0, j - 1, item)
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignHCenter)

    def get_showdata(self):
        self.frame.show()
        data = SQL_player_data.player_data().data
        # 遍历二维元组, 将 id 和 name 显示到界面表格上
        x = 0
        for i in data:
            y = 0
            for j in i:
                item = QtWidgets.QTableWidgetItem(str(data[x][y]))
                self.tableWidget.setItem(x, y, item)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignHCenter)
                y = y + 1
            x = x + 1
            if x > 807:
                break
        self.frame2.hide()
        self.frame3.close()

    def get_query(self):
        self.frame2.show()
        self.frame.hide()
        self.frame3.close()

    def get_predict(self):
        self.frame3.show()
        self.frame.hide()
        self.frame2.close()


# 标签编码
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
            image = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), 0)
            # 获取人脸标记
            name = filepath.split("\\")[-2]
            # 检测是否有人脸，并获取人脸数据
            faces = face_faces.detectMultiScale(image, 1.1, 5)
            # 输入每个人脸的数据
            for x, y, w, h in faces:
                images.append(image[y:y + h, x:x + w])
                labels.append(le.word_to_num(name))
    return images, labels, le


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('../Model/my_LBPHFaceRecognizer.xml')
face_faces = cv2.CascadeClassifier('../data3/cascade_files/haarcascade_frontalface_alt.xml')
input_path = '../data3/faces_dataset/train'  # 训练集的路径
images, labels, le = get_images_and_labels(input_path)

