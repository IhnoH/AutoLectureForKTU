import time
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *

class Thread1(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        self.parent.textBrowser.append("경주마1이 출발하였습니다.")
        for i in range(20):
            self.parent.textBrowser.append("경주마1이"+str( i )+"km째   달리고 있습니다.")
            time.sleep(2)
        self.parent.textBrowser.append("경주마1이 결승지에 도착하였습니다.")

class Thread2(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        self.parent.textBrowser.append("경주마2가 출발하였습니다.")
        for i in range(20):
            self.parent.textBrowser.append("경주마2가"+str( i )+"km째   달리고 있습니다.")
            time.sleep(2)
        self.parent.textBrowser.append("경주마2가 결승지에 도착하였습니다.")

class WindowClass(QMainWindow):
    def __init__(self) :
        super().__init__()

        # 각 버튼에 대한 함수 연결
        self.runButton1.clicked.connect(self.actionFunction1)
        self.runButton2.clicked.connect(self.actionFunction2)

    # 경주마1 출발 버튼을 눌렀을 때 실행 될 메서드
    def actionFunction1(self):
        h1 = Thread1(self)
        h1.start()

    # 경주마2 출발 버튼을 눌렀을 때 실행 될 메서드
    def actionFunction2(self):
        h2 = Thread2(self)
        h2.start()

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()