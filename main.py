from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize

class MainWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.showMaximized()
        self.initUI()
        self.show()

    def createLayout(self):
        self.mainLine = QVBoxLayout()
        self.dockbarLine = QHBoxLayout()
        self.centerLine = QHBoxLayout()
        self.toolsLine = QVBoxLayout()

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

    def initUI(self):
        self.createLayout()
        self.createWidgets()
        self.setLayout(self.mainLine)

        self.mainLine.addLayout(self.dockbarLine)
        self.mainLine.addLayout(self.centerLine)

        self.centerLine.addWidget(self.picLabel)
        self.centerLine.addLayout(self.toolsLine)

        self.dockbarLine.addWidget(self.dockbar, alignment=Qt.AlignTop)


main = QApplication([])
mainW = MainWindow('ImageEditor')
main.exec_()
