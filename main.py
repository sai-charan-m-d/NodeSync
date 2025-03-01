import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel

class MyWidget(QWidget):
    def __inti__(self):
        super.__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        
        self.button = QPushButton("Click Me!")
        self.text - QLabel("Hello World", alignment = QtCore.Qt.AlignCenter)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800,600)
    widget.show()

    sys.exit(app.exec())