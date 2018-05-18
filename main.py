import sys
from PyQt5.QtWidgets import QApplication

from gui import Weather_App
from dao import Weather_DAO

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Weather_App(Weather_DAO())
    sys.exit(app.exec_())
