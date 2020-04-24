import sys
from mainwindow import *


if __name__ == "__main__":
    app = QApplication(sys.argv)

    wnd = MainWindow()

    wnd.show()

    app.exec_()