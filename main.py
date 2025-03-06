from PySide6.QtWidgets import QApplication 
from PySide6.QtCore import Qt
from ns_mainwindow import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow(app)
    window.setWindowFlag(Qt.FramelessWindowHint)
    window.show()

    with open("E:/01_WORK/01_PROJ/NODESYNC/NodeSync/style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)


    app.exec()