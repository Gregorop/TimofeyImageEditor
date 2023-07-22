from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap

class MainWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        
        self.initUI()
        self.showMaximized()
        self.show()

    def createLayout(self):
        self.mainLine = QVBoxLayout()
        self.dockbarLine = QHBoxLayout()
        self.toolsLine = QHBoxLayout() #теперь это будет панелька под docбаром

    def createWidgets(self):
        self.dockbar = QMenuBar()
        self.dockbar.setMaximumSize(QSize(1920, 25))

        self.fileButton = QMenu("File")
        self.settingsButton = QMenu("Settings")
        self.dockbar.addMenu(self.fileButton)
        self.dockbar.addMenu(self.settingsButton)

        self.openFileAction = QAction('open')
        self.saveFileAction = QAction('save')
        self.fileButton.addActions([self.openFileAction, self.saveFileAction])

        self.picLabel = QLabel('#место для картинки') 
        self.pixmap = QPixmap('blank.png') #картинка как набор пикселей, для рисования QPainter
        '''https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qtgui/qpainter.html?highlight=qpainter#QPainter'''

        self.picLabel.setPixmap(self.pixmap)

    def initUI(self):
        self.createLayout()
        self.createWidgets()
        self.setLayout(self.mainLine)

        self.mainLine.addLayout(self.dockbarLine)

        #? почему между докбаром и картинкой километр пустоты?
        self.dockbarLine.addWidget(self.dockbar, alignment=Qt.AlignTop)
        self.mainLine.addWidget(self.picLabel, alignment=Qt.AlignCenter)

        


main = QApplication([])
mainW = MainWindow('ImageEditor')
main.exec_()
