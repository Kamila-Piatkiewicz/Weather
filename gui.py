from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import requests


class Day_Forecast(QWidget):
    def __init__(self):
        super().__init__()
      
      
class Day_Widget(QWidget):
    def __init__(self, weather_data, day_number):
        super().__init__()
        self.weather_data = weather_data
        self.day_number = day_number
        self.initUI()

    def initUI(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(200,180,200))
        self.setPalette(p)
       
        lbl_weekday = QLabel(self.weather_data.get_weekday(self.day_number), self)
        lbl_date = QLabel(self.weather_data.get_date(self.day_number), self)
        lbl_temp = QLabel("%sC - %sC" % (str(self.weather_data.get_min_temperature(self.day_number)), str(self.weather_data.get_max_temperature(self.day_number))), self)
       
        lbl_icon = QLabel(self)
        data = requests.get(self.weather_data.get_icon_url(self.day_number)).content
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        lbl_icon.setPixmap(pixmap)
      
        grid = QGridLayout()
        grid.addWidget(lbl_weekday, 0, 0)
        grid.addWidget(lbl_date, 0, 1)
        grid.addWidget(lbl_temp, 1, 0)
        grid.addWidget(lbl_icon, 1, 1)
        grid.setContentsMargins(20, 20, 20, 20)
        grid.setSpacing(30)
        self.setLayout(grid)
        
class Hourly_Plot_Widget(QWidget):
    
    def __init__(self, weather_data, parent=None):
        super(Hourly_Plot_Widget, self).__init__(parent)
        self.weather_data = weather_data

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        
        self.axis = self.figure.add_subplot(111)
        self.axis.set(ylabel='temperatura',title='Pogoda godzinowa')
        self.axis.xaxis.set_major_locator(plt.MultipleLocator(1))
        self.axis.yaxis.set_major_locator(plt.MultipleLocator(5))
        x = self.create_x_dataset()
        y_max = self.create_max_temp_dataset()
        y_min = self.create_min_temp_dataset()
        self.axis.plot(x, y_max,'ro-')
        self.axis.plot(x, y_min,'bo-')
        #self.axis.set_yticklabels(self.create_max_temp_dataset)
        for i in range(0,10):
            self.axis.annotate(y_max[i], (x[i], y_max[i]+1))
            self.axis.annotate(y_min[i], (x[i], y_min[i]+1))

        self.layoutVertical = QVBoxLayout(self)
        self.layoutVertical.addWidget(self.canvas)
        
    def create_max_temp_dataset(self):
        y_dataset = []
        for i in range (0, 10):
            y_dataset.append(self.weather_data.get_max_temperature(i))
        return y_dataset
    
    def create_min_temp_dataset(self):
        y_dataset = []
        for i in range (0, 10):
            y_dataset.append(self.weather_data.get_min_temperature(i))
        return y_dataset
    
    def create_x_dataset(self):
        x_dataset = []
        for i in range(0,10):
            x_dataset.append(self.weather_data.get_date(i)+'\n'+self.weather_data.get_weekday(i))
        return x_dataset
      
class Weather_App(QWidget):

    def __init__(self, weather_data):
        super().__init__()
        self.weather_data = weather_data
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Pogoda')
        self.setGeometry(200, 200, 1280, 960)
      
        day0 = Day_Widget(self.weather_data, 0)
        day1 = Day_Widget(self.weather_data, 1)
        day2 = Day_Widget(self.weather_data, 2)
        day3 = Day_Widget(self.weather_data, 3)
        day4 = Day_Widget(self.weather_data, 4)
        day5 = Day_Widget(self.weather_data, 5)
        day6 = Day_Widget(self.weather_data, 6)
        day7 = Day_Widget(self.weather_data, 7)
        day8 = Day_Widget(self.weather_data, 8)
        day9 = Day_Widget(self.weather_data, 9)
        
        plot = Hourly_Plot_Widget(self.weather_data)
       
        grid = QGridLayout()
        grid.addWidget(day0, 0, 0)
        grid.addWidget(day1, 0, 1)
        grid.addWidget(day2, 0, 2)
        grid.addWidget(day3, 0, 3)
        grid.addWidget(day4, 0, 4)
        grid.addWidget(day5, 1, 0)
        grid.addWidget(day6, 1, 1)
        grid.addWidget(day7, 1, 2)
        grid.addWidget(day8, 1, 3)
        grid.addWidget(day9, 1, 4)
        grid.addWidget(plot, 2, 0, 2, 5)
        grid.setContentsMargins(30, 30, 30, 30)
        grid.setSpacing(30)
        self.setLayout(grid)
       
        self.show()
