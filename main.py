from PySide6.QtWidgets import QApplication 
from ns_mainwindow import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow(app)
    window.show()


    app.exec()