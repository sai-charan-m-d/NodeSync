from PySide6.QtWidgets import QWidget
#from PySide6.QtGui import

class CreateProjectWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setGeometry(100,100,800,600)
        self.setWindowTitle("Create Project")
        self.setGeometry(150,150,500,200)

        self.show()
