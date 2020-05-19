import sys
from mainwindow import *
from theme import theme


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app = theme(app)

    wnd = MainWindow()

    wnd.show()

    app.exec_()
