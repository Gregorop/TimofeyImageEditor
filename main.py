from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter
import os

def helloworld():
    print('hello')

class MainWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        
        self.initUI()
        self.showMaximized()
        self.show()

    def createLayout(self):
        self.mainLine = QVBoxLayout(spacing = 0)
        #self.mainLine.addStretch()
        self.dockbarLine = QHBoxLayout()
        self.toolsLine = QHBoxLayout() #теперь это будет панелька под docбаром

    def createDockbar(self):
        self.dockbar = QMenuBar()
        self.dockbar.setMinimumSize(QSize(1920, 10))

        self.fileButton = QMenu("File")
        self.settingsButton = QMenu("Settings")
        self.dockbar.addMenu(self.fileButton)
        self.dockbar.addMenu(self.settingsButton)

        self.openFileAction = QAction('Open')
        self.openFileAction.triggered.connect(self.openFile)

        self.saveFileAction = QAction('Save')
        self.fileButton.addActions([self.openFileAction, self.saveFileAction])

    def createToolbar(self):
        self.toolbar = QMenuBar()
        self.toolbar.setMaximumSize(QSize(1920, 20))

        self.rotateButton = QMenu('Rotate')
        self.toolbar.addMenu(self.rotateButton)

        self.rotateCWAction = QAction('CW')
        self.rotateCWAction.triggered.connect(self.rotateImageCW)

        self.rotateButton.addActions([self.rotateCWAction])

    def createWidgets(self):
        self.picLabel = QLabel('#место для картинки') 
        self.file = 'blank.jpg'
        self.pixmap = QPixmap('blank.jpg') #картинка как набор пикселей, для рисования QPainter
        self.pixmap = self.pixmap.scaled(1000, 500)
        '''https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qtgui/qpainter.html?highlight=qpainter#QPainter'''
        self.picLabel.setPixmap(self.pixmap)
        self.picLabel.mousePressEvent = self.getPos

    def getPos(self , event):
        x = event.pos().x()
        y = event.pos().y() 
        print(x,y)


    def initUI(self):
        self.createLayout()
        self.createDockbar()
        self.createToolbar()
        self.createWidgets()

        self.mainLine.addLayout(self.dockbarLine)
        self.mainLine.addLayout(self.toolsLine)

        self.dockbarLine.addWidget(self.dockbar)
        self.toolsLine.addWidget(self.toolbar, alignment = Qt.AlignTop)
        self.mainLine.addWidget(self.picLabel, alignment = Qt.AlignCenter)
        self.setLayout(self.mainLine)
    
    def openFile(self):
        self.file, _ = QFileDialog.getOpenFileName()
        self.pixmap = QPixmap(self.file)
        self.picLabel.setPixmap(self.pixmap)

    def rotateImageCW(self):
        img = Image.open(self.file)
        newImg = img.rotate(90, expand=True)
        newImg.save('temp\\temp.png')
        self.pixmap = QPixmap('temp\\temp.png')
        self.picLabel.setPixmap(self.pixmap)
        self.file = 'temp\\temp.png'

main = QApplication([])
mainW = MainWindow('ImageEditor')

#возвращает не только имя файла, но и выбранную сортировку (Она нам не нужна)
#full_filename, _ = QFileDialog.getOpenFileName()
#print(_)
#print(full_filename)

main.exec_()
