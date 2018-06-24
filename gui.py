from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QColor, QPixmap, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import requests

BIG_LIGHT_FONT = QFont("Calibri Light", pointSize = 18)
BIG_FONT = QFont("Calibri", pointSize = 18)
NORMAL_LIGHT_FONT = QFont("Calibri Light", pointSize = 14)
PURPLE_BLUE = QColor(204, 204, 255)


class Day_Forecast(QWidget):
    
    def __init__(self, weather_data, day_number):
        super().__init__()
        self.weather_data = weather_data
        self.day_number = day_number
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Pogoda szczegółowa')
        self.setGeometry(100, 100, 800, 500)

        layout = QVBoxLayout(self)

        lbl_date = QLabel(self.weather_data.get_date(self.day_number) + " ("+self.weather_data.get_weekday(self.day_number)+")", self)
        lbl_humidity = QLabel("Wilgotność powietrza: "+str(self.weather_data.get_humidity(self.day_number))+"%", self)
        lbl_rain = QLabel("Deszcz: "+str(self.weather_data.get_rain(self.day_number))+" mm", self)
        lbl_snow = QLabel("Śnieg: "+str(self.weather_data.get_snow(self.day_number))+" cm", self)
        lbl_avewind = QLabel("Średnia prędkość wiatru: "+str(self.weather_data.get_average_wind(self.day_number))+" km/h", self)
        lbl_maxwind = QLabel("Maksymalna prędkość wiatru: "+str(self.weather_data.get_max_wind(self.day_number))+" km/h", self)
        

        lbl_date.setFont(BIG_FONT)
        lbl_humidity.setFont(NORMAL_LIGHT_FONT)
        lbl_rain.setFont(NORMAL_LIGHT_FONT)
        lbl_snow.setFont(NORMAL_LIGHT_FONT)
        lbl_avewind.setFont(NORMAL_LIGHT_FONT)
        lbl_maxwind.setFont(NORMAL_LIGHT_FONT)

        layout.addWidget(lbl_date)
        layout.addWidget(lbl_humidity)
        layout.addWidget(lbl_rain)
        layout.addWidget(lbl_snow)
        layout.addWidget(lbl_avewind)
        layout.addWidget(lbl_maxwind)

        if self.day_number == 0 or self.day_number == 1:
            hourly_plot = Hourly_Plot_Widget(self.weather_data, self.day_number)
            layout.addWidget(hourly_plot)

        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(10)
        self.setLayout(layout)
      
      
class Day_Widget(QWidget):
    def __init__(self, weather_data, day_number):
        super().__init__()
        self.weather_data = weather_data
        self.day_number = day_number
        self.initUI()

    def initUI(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), PURPLE_BLUE)
        self.setPalette(p)
       
        lbl_weekday = QLabel(self.weather_data.get_weekday(self.day_number), self)
        lbl_weekday.setFont(BIG_FONT)
        
        lbl_date = QLabel(self.weather_data.get_date(self.day_number), self)
        lbl_date.setFont(BIG_FONT)
        
        lbl_temp = QLabel("%sC - %sC" % (str(self.weather_data.get_min_temperature(self.day_number)), str(self.weather_data.get_max_temperature(self.day_number))), self)
        lbl_temp.setFont(BIG_LIGHT_FONT)
       
        lbl_icon = QLabel(self)
        data = requests.get(self.weather_data.get_icon_url(self.day_number)).content
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        lbl_icon.setPixmap(pixmap)

        btn_more = QPushButton(self, text="More info")
        btn_more.setFont(NORMAL_LIGHT_FONT)
        btn_more.clicked.connect(self.on_click_button)
      
        grid = QGridLayout()
        grid.addWidget(lbl_weekday, 0, 0)
        grid.addWidget(lbl_date, 0, 1)
        grid.addWidget(lbl_temp, 1, 0)
        grid.addWidget(lbl_icon, 1, 1)
        grid.addWidget(btn_more, 2, 0, 1, 2)
        grid.setContentsMargins(20, 20, 20, 20)
        grid.setSpacing(20)
        self.setLayout(grid)


    @pyqtSlot()
    def on_click_button(self):
        self.details_window = Day_Forecast(self.weather_data, self.day_number)
        self.details_window.show()
        
class Ten_Days_Plot_Widget(QWidget):
    
    def __init__(self, weather_data, parent=None):
        super(Ten_Days_Plot_Widget, self).__init__(parent)
        self.weather_data = weather_data

        figure = Figure()
        canvas = FigureCanvasQTAgg(figure)

        axis_rain = figure.add_subplot(111)
        axis_rain.set(ylabel='opady[mm]',title='Pogoda na 10 dni')
        axis_rain.xaxis.set_major_locator(plt.MultipleLocator(1))
        
        axis_temp = axis_rain.twinx()
        axis_temp.set(ylabel='temperatura [C]')
        axis_temp.yaxis.set_major_locator(plt.MultipleLocator(5))
        
        x = self.create_x_dataset()
        y_max = self.create_max_temp_dataset()
        y_min = self.create_min_temp_dataset()
        y_rain = self.create_rain_dataset()

        axis_rain.bar(x, y_rain, color='#B3FFFF')
        axis_temp.plot(x, y_max, 'ro-')
        axis_temp.plot(x, y_min, 'bo-')

        axis_temp.set_ylim(axis_temp.get_ylim()[0]-5, axis_temp.get_ylim()[1]+5)
        
        
        for i in range(0,10):
            axis_temp.annotate(y_max[i], (x[i], y_max[i]+1))
            axis_temp.annotate(y_min[i], (x[i], y_min[i]+1))

        self.layoutVertical = QVBoxLayout(self)
        self.layoutVertical.addWidget(canvas)

    def create_x_dataset(self):
        x_dataset = []
        for i in range(0,10):
            x_dataset.append(self.weather_data.get_date(i)+'\n'+self.weather_data.get_weekday(i))
        return x_dataset
        
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

    def create_rain_dataset(self):
        y_dataset = []
        for i in range (0, 10):
            y_dataset.append(self.weather_data.get_rain(i))
        return y_dataset

class Hourly_Plot_Widget(QWidget):
    
    def __init__(self, weather_data, day_number, parent=None):
        super(Hourly_Plot_Widget, self).__init__(parent)
        self.weather_data = weather_data
        self.day_number = day_number

        figure = Figure()
        canvas = FigureCanvasQTAgg(figure)

        axis_rain = figure.add_subplot(111)
        axis_rain.set(ylabel='opady[mm]',title='Pogoda godzinowa')
        axis_rain.xaxis.set_major_locator(plt.MaxNLocator(10))
        axis_rain.xaxis.set_major_formatter(plt.FormatStrFormatter('%d:00'))
        axis_rain.set_ylim(0, 20)
        
        axis_temp = axis_rain.twinx()
        axis_temp.set(ylabel='temperatura [C]')
        axis_temp.yaxis.set_major_locator(plt.MultipleLocator(5))
        
        x = self.create_x_dataset()
        y_temp = self.create_temp_dataset()
        y_rain = self.create_rain_dataset()
        print(x)
        print(y_temp)
        print(y_rain)

        axis_rain.bar(x, y_rain, color='#B3FFFF')
        axis_temp.plot(x, y_temp, 'ro-')
        
        
        axis_temp.set_ylim(axis_temp.get_ylim()[0]-2, axis_temp.get_ylim()[1]+2)
        
        
        for i in range(0,len(x)):
            axis_temp.annotate(y_temp[i], (x[i], y_temp[i]+1))
            #axis_temp.annotate(y_min[i], (x[i], y_min[i]+1))

        self.layoutVertical = QVBoxLayout(self)
        self.layoutVertical.addWidget(canvas)

    def create_x_dataset(self):
        if self.day_number == 0:
            return self.weather_data.get_today_next_hours()
        elif self.day_number == 1:
            return self.weather_data.get_tomorrow_next_hours()
            
        
    def create_temp_dataset(self):
        if self.day_number == 0:
            return self.weather_data.get_today_hourly_temperature()
        elif self.day_number == 1:
            return self.weather_data.get_tomorrow_hourly_temperature()
        

    def create_rain_dataset(self):
        if self.day_number == 0:
            return self.weather_data.get_today_hourly_rain()
        elif self.day_number == 1:
            return self.weather_data.get_tomorrow_hourly_rain()
       
      
class Weather_App(QWidget):

    def __init__(self, weather_data):
        super().__init__()
        self.weather_data = weather_data
        self.initUI()
        self.d = Day_Forecast(weather_data,1).show()

    def initUI(self):
        self.setWindowTitle('Pogoda')
        self.setGeometry(50, 50, 1280, 960)

        grid = QGridLayout()

        for i in range (0,10):
            day = Day_Widget(self.weather_data, i)
            grid.addWidget(day, i >= 5, i % 5)

        plot = Ten_Days_Plot_Widget(self.weather_data)   
        grid.addWidget(plot, 2, 0, 2, 5)
        
        grid.setContentsMargins(30, 30, 30, 30)
        grid.setSpacing(30)
        self.setLayout(grid)
       
        self.show()
