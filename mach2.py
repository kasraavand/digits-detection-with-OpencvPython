import cv2
import numpy as np
import argparse
import sys
import os
from PyQt4 import QtGui, QtCore
import codecs


class detector():
    def __init__(self, *args, **kwargs):
        self.raw_pic_name = kwargs['raw_pic']
        self.detection_number = kwargs['detection']
        self.raw_pic = self.read_raw_image()
        self.detection_pic = self.get_dtection_image()
        self.detection_height = self.detection_pic.shape[0]
        self.detection_widths = self.detection_pic.shape[1]
        self.result = self.detect()


    def get_dtection_image(self):
        file_name = 'distinc_digits/{}.png'.format(self.detection_number)
        img = cv2.imread(file_name)
        return img

    def read_raw_image(self):
        img = cv2.imread(self.raw_pic_name)
        return img

    def detect(self):
        gray2 = cv2.cvtColor(self.raw_pic, cv2.COLOR_BGR2GRAY)
        blur2 = cv2.GaussianBlur(gray2, (5, 5), 0)
        ret, thresh2 = cv2.threshold(blur2, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh2, 2, 1)

        for cnt in contours:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if (h > 27 and h < 35):
                tempim = self.raw_pic[y:y + h, x:x + w]
                new = cv2.resize(tempim, (self.detection_widths,
                                          self.detection_height))
                # new = np.float32(new)
                res = cv2.matchTemplate(self.detection_pic, new, 1)
                if res < 0.2:
                    cv2.rectangle(self.raw_pic, (x, y), (x + w, y + h), (0, 0, 255), 2)
        return self.raw_pic

    def show(self):
        cv2.imshow('result', self.result)
        cv2.waitKey(0)

    def write(self):
        cv2.imwrite('result.png', self.result)


class TestListView(QtGui.QDialog):
    def __init__(self, type, parent=None):
        super(TestListView, self).__init__(parent)
        self.setAcceptDrops(True)
        self.createFilesTable()
        self.label6 = QtGui.QTextEdit(self)
        self.label6.setGeometry(70, 260, 100, 30)
        self.numLabel = QtGui.QLabel("Number:")
        findButton = self.createButton("&Detect", self.find)
        buttonsLayout = QtGui.QHBoxLayout()
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(findButton)
        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.filesTable, 3, 0, 1, 3)
        browseButton = self.createButton("&Browse...", self.browse)
        self.directoryComboBox = self.createComboBox(QtCore.QDir.currentPath())
        directoryLabel = QtGui.QLabel("Your Path:")
        mainLayout.addWidget(directoryLabel, 2, 0)
        mainLayout.addWidget(self.numLabel, 5, 0)
        mainLayout.addWidget(self.directoryComboBox, 2, 1)
        mainLayout.addWidget(browseButton, 2, 2)
        mainLayout.addLayout(buttonsLayout, 5, 0, 1, 3)
        self.setLayout(mainLayout)

    def browse(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self)
        if fileName:
            inFile = QtCore.QFile(fileName)
            if not inFile.open(QtCore.QFile.ReadOnly):
                QtGui.QMessageBox.warning(self,
                                          "Codecs",
                                          "Cannot read file %s:\n%s" % (fileName,
                                                                        inFile.errorString()))
                return

        self.showFiles(fileName)

    def showFiles(self, files):
            file = QtCore.QFile(files)
            size = QtCore.QFileInfo(file).size()

            fileNameItem = QtGui.QTableWidgetItem(files)
            fileNameItem.setFlags(fileNameItem.flags() ^ QtCore.Qt.ItemIsEditable)
            sizeItem = QtGui.QTableWidgetItem("%d KB" % (int((size + 1023) / 1024)))
            sizeItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            sizeItem.setFlags(sizeItem.flags() ^ QtCore.Qt.ItemIsEditable)

            row = self.filesTable.rowCount()
            self.filesTable.insertRow(row)
            self.filesTable.setItem(row, 0, fileNameItem)
            self.filesTable.setItem(row, 1, sizeItem)

    def updateComboBox(self, comboBox):
        if comboBox.findText(comboBox.currentText()) == -1:
            comboBox.addItem(comboBox.currentText())

    def createButton(self, text, member):
        button = QtGui.QPushButton(text)
        button.clicked.connect(member)
        return button

    def createComboBox(self, text=""):
        comboBox = QtGui.QComboBox()
        comboBox.setEditable(True)
        comboBox.addItem(text)
        comboBox.setSizePolicy(QtGui.QSizePolicy.Expanding,
                               QtGui.QSizePolicy.Preferred)
        return comboBox


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(QtCore.SIGNAL("dropped"), links)
        else:
            event.ignore()

    def createFilesTable(self):
        self.filesTable = QtGui.QTableWidget(0, 2)
        self.itemm = QtGui.QTableWidgetItem()
        self.filesTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.filesTable.setHorizontalHeaderLabels(("File Name", "Size"))
        self.filesTable.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)
        self.filesTable.verticalHeader().hide()
        self.filesTable.setShowGrid(True)
        self.filesTable.cellActivated.connect(self.find)

    def find(self, fileName):
        path = self.directoryComboBox.currentText()
        self.updateComboBox(self.directoryComboBox)
        item = self.filesTable.item(0, 0)
        a = QtGui.QTableWidgetItem(item)
        d = detector(raw_pic=str(a.text()),
                     detection=str(self.label6.toPlainText()))
        d.show()



class MainForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.view = TestListView(self)
        self.connect(self.view, QtCore.SIGNAL("dropped"), self.pictureDropped)
        self.setCentralWidget(self.view)
        self.resize(700, 300)

    def pictureDropped(self, l):
        for url in l:
            if os.path.exists(url):
                print(url)
                icon = QtGui.QIcon(url)
                pixmap = icon.pixmap(72, 72)
                icon = QtGui.QIcon(pixmap)
                self.view.showFiles(url)


def main():
    app = QtGui.QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()

"""
if __name__ == "__main__":
    description = "Detect digits. Use -h or --help for help menu."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-P", "-picture_name", help="The name of picture.")
    parser.add_argument("-N", "-number", help="The number for detect.")

    args = parser.parse_args()
    name = args.P
    num = args.N
    d = detector(raw_pic=name, detection=num)
    d.show()
"""
