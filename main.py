from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter
import os

def helloworld():
    print('hello')

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.file = 'C:\\Users\\User\\Desktop\\dve\\mygames\\ImageEditor\\blank.jpg'
        self.img = Image.open(self.file)
        self.setWindowTitle('Image Editor')
        self.initUI()
        self.showMaximized()
        self.show()

    def createLayout(self):
        self.mainLine = QVBoxLayout(spacing = 0)
        #self.mainLine.addStretch()
        self.dockbarLine = QHBoxLayout()
        self.toolsLine = QHBoxLayout() #теперь это будет панелька под docбаром
        self.infoLine = QHBoxLayout()

    def createDockbar(self):
        self.dockbar = QMenuBar()
        self.dockbar.setMinimumSize(QSize(1920, 20))

        self.fileButton = QMenu("File")
        self.settingsButton = QMenu("Settings")
        self.dockbar.addMenu(self.fileButton)
        self.dockbar.addMenu(self.settingsButton)

        self.openFileAction = QAction('Open')
        self.openFileAction.triggered.connect(self.openFile)
        self.saveFileAction = QAction('Save')
        #self.openFileAction.triggered.connect(self.saveFile)
        self.fileButton.addActions([self.openFileAction, self.saveFileAction])

    def createToolbar(self):
        self.toolbar = QMenuBar()
        self.toolbar.setMaximumSize(QSize(1920, 30))

        self.rotateButton = QMenu('Rotate')
        self.toolbar.addMenu(self.rotateButton)
        self.rotateCWAction = QAction('CW')
        self.rotateCWAction.triggered.connect(self.rotateImageCW)
        self.rotateCCWAction = QAction('CCW')
        self.rotateCCWAction.triggered.connect(self.rotateImageCCW)
        self.rotateButton.addActions([self.rotateCWAction, self.rotateCCWAction])

        self.flipButton = QMenu('Flip')
        self.toolbar.addMenu(self.flipButton)
        self.FlipTBAction = QAction('Top to bottom')
        self.FlipTBAction.triggered.connect(self.flipTopBottom)
        self.FlipLRAction = QAction('Left to right')
        self.FlipLRAction.triggered.connect(self.flipLeftRight)
        self.flipButton.addActions([self.FlipTBAction, self.FlipLRAction])

        self.filtersButton = QMenu('Filters')
        self.toolbar.addMenu(self.filtersButton)
        self.blurGroup = QMenu('Blur')
        self.gaussianBlurAction = QAction('Gaussian')
        self.gaussianBlurAction.triggered.connect(self.gaussianBlurFilter)
        self.boxBlurAction = QAction('Box Blur')
        self.boxBlurAction.triggered.connect(self.boxBlurFilter)
        self.blurGroup.addActions([self.gaussianBlurAction, self.boxBlurAction])
        self.contourAction = QAction('Contour')
        self.contourAction.triggered.connect(self.contourFilter)
        self.detailAction = QAction('Detail')
        self.detailAction.triggered.connect(self.detailFilter)
        self.filtersButton.addActions([self.gaussianBlurAction, self.contourAction, self.detailAction])
        self.filtersButton.addMenu(self.blurGroup)

    def createWidgets(self):
        global toolbar, pixmap
        self.infoLabel = QLabel(str(self.img.size))
        self.picLabel = QLabel('#место для картинки') 
        self.file = 'blank.jpg'
        self.pixmap = QPixmap('blank.jpg') #картинка как набор пикселей, для рисования QPainter
        self.pixmap = self.pixmap.scaled(1000, 500)
        '''https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qtgui/qpainter.html?'''
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
        self.mainLine.addLayout(self.infoLine)

        self.dockbarLine.addWidget(self.dockbar, alignment=Qt.AlignTop)
        self.toolsLine.addWidget(self.toolbar, alignment=Qt.AlignTop)
        self.mainLine.addWidget(self.picLabel, alignment=Qt.AlignCenter)
        self.infoLine.addWidget(self.infoLabel, alignment=Qt.AlignBottom)
        self.setLayout(self.mainLine)


    def openFile(self):
        self.file = QFileDialog.getOpenFileName()[0]
        self.pixmap = QPixmap(self.file)
        self.picLabel.setPixmap(self.pixmap)
        self.img = Image.open(self.file)
        self.infoLabel.setText(str(self.img.size))

    def saveFile(self):
        toSaveFile = QFileDialog().getSaveFileName(None, 'Save As', '/', 'Image files (*.png)')[0]
        self.img = Image.open(self.file)
        self.img.save(toSaveFile)
        self.infoLabel.setText(str(self.img.size))

    def updatePixMap(self, newImg):
        newImg.save('temp\\temp.png')
        self.pixmap = QPixmap('temp\\temp.png')
        self.file = 'temp\\temp.png'
        self.img = Image.open(self.file)
        self.picLabel.setPixmap(self.pixmap)
        self.infoLabel.setText(str(self.img.size))

    def getValue(self, win):
        win.hide()
        return win.slider.value()

    def rotateImageCW(self):
        self.updatePixMap(self.img.rotate(-90, expand=True))

    def rotateImageCCW(self):
        self.updatePixMap(self.img.rotate(90, expand=True))
    
    def flipTopBottom(self):
        self.updatePixMap(self.img.transpose(Image.Transpose.FLIP_TOP_BOTTOM))

    def flipLeftRight(self):
        self.updatePixMap(self.img.transpose(Image.Transpose.FLIP_TOP_BOTTOM))

    def gaussianBlurFilter(self):
        blurWindow = FilterWindow('Blur', ImageFilter.GaussianBlur, 1, 10, 1, 1)

    def boxBlurFilter(self):
        blurWindow = FilterWindow('Blur', ImageFilter.BoxBlur, 1, 10, 1, 1)

    def contourFilter(self):
        self.updatePixMap(self.img.filter(ImageFilter.CONTOUR))

    def detailFilter(self):
        self.updatePixMap(self.img.filter(ImageFilter.DETAIL))


class FilterWindow(QWidget):
    def __init__(self, filterName, filter, minimum, maximum, step, defaultValue):
        super().__init__()
        self.setWindowTitle(filterName)
        self.resize(200,50)
        self.filter = filter
        self.min = minimum
        self.max = maximum
        self.step = step
        self.default = defaultValue
        self.initUI()
        self.show()

    def createLayout(self):
        self.mainLine = QVBoxLayout()
        self.topLine = QHBoxLayout()
        self.midLine = QHBoxLayout()
        self.bottomLine = QHBoxLayout()
    
    def createWidgets(self):
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(self.min)
        self.slider.setMaximum(self.max)
        self.slider.setSingleStep(self.step)
        self.slider.setValue(self.default)
        self.slider.valueChanged.connect(self.updateValue)
        self.label = QLabel(f'Filter intensity:{self.slider.value()}')
        self.okButton = QPushButton('OK')
        self.okButton.clicked.connect(lambda:mainW.updatePixMap(mainW.img.filter(self.filter(mainW.getValue(self)))))

    def initUI(self):
        self.createLayout()
        self.createWidgets()

        self.topLine.addWidget(self.label, alignment=Qt.AlignCenter)
        self.midLine.addWidget(self.slider, alignment=Qt.AlignCenter)
        self.bottomLine.addWidget(self.okButton, alignment=Qt.AlignCenter)
        self.mainLine.addLayout(self.topLine)
        self.mainLine.addLayout(self.midLine)
        self.mainLine.addLayout(self.bottomLine)

        self.setLayout(self.mainLine)

    def updateValue(self): self.label.setText(f'Filter intensity: {self.slider.value()}')



main = QApplication([])
mainW = MainWindow()

main.exec_()
