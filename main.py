from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

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
        self.fileButton = QMenu("File")
        self.settingsButton = QMenu("Settings")
        self.dockbar.addMenu(self.fileButton)
        self.dockbar.addMenu(self.settingsButton)

    def initUI(self):
        self.createLayout()
        self.createWidgets()
        self.setLayout(self.mainLine)
        self.mainLine.addLayout(self.dockbarLine)
        self.dockbarLine.addWidget(self.dockbar)


main = QApplication([])
mainW = MainWindow('window')
main.exec_()
