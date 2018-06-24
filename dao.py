import requests
import json
from datetime import datetime, timedelta

class Weather_DAO:

    def __init__(self):
        self.download_current_data()

    def download_current_data(self):
        url = 'http://api.wunderground.com/api/a6986716e8fd9687/forecast10day/q/PL/Lublin.json'
        response = requests.get(url)

        if (response.ok):
            self.json_10days_weather = json.loads(response.content)
           
            '''
            print("-----Pobieram dane-----\n\n")
            for key in self.json_10days_weather:
                print(key + " : " + str(self.json_10days_weather[key]))
            print("\n\n")'''
           
        url = 'http://api.wunderground.com/api/a6986716e8fd9687/hourly/q/PL/Lublin.json'
        response = requests.get(url)

        if (response.ok):
            self.json_hourly_weather = json.loads(response.content)
            
            '''
            print("-----Pobieram dane-----\n\n")
            for key in self.json_hourly_weather:
                print(key + " : " + str(self.json_hourly_weather[key]))
            print("\n\n")'''
          
    def get_weekday(self, in_days):
        weekday = (datetime.now() + timedelta(days=in_days)).weekday()
        if weekday == 0:
            return 'Poniedziałek'
        if weekday == 1:
            return 'Wtorek'
        if weekday == 2:
            return 'Środa'
        if weekday == 3:
            return 'Czwartek'
        if weekday == 4:
            return 'Piątek'
        if weekday == 5:
            return 'Sobota'
        if weekday == 6:
            return 'Niedziela'
       
    def get_date(self, in_days):
        day = datetime.now() + timedelta(days=in_days)
        return '{:02}.{:02}'.format(day.day, day.month)

    def get_hour_now(self):
        return datetime.now().hour
   
    def get_min_temperature(self, in_days):
        return int(self.json_10days_weather['forecast']['simpleforecast']['forecastday'][in_days]['low']['celsius'])
   
    def get_max_temperature(self, in_days):
        return int(self.json_10days_weather['forecast']['simpleforecast']['forecastday'][in_days]['high']['celsius'])

    def get_rain(self, in_days):
        return int(self.json_10days_weather['forecast']['simpleforecast']['forecastday'][in_days]['qpf_allday']['mm'])

    def get_snow(self, in_days):
        return int(self.json_10days_weather['forecast']['simpleforecast']['forecastday'][in_days]['snow_allday']['cm'])

    def get_average_wind(self, in_days):
        return int(self.json_10days_weather['forecast']['simpleforecast']['forecastday'][in_days]['avewind']['kph'])

    def get_max_wind(self, in_days):
        return int(self.json_10days_weather['forecast']['simpleforecast']['forecastday'][in_days]['maxwind']['kph'])

    def get_humidity(self, in_days):
        return int(self.json_10days_weather['forecast']['simpleforecast']['forecastday'][in_days]['avehumidity'])
   
    def get_icon_url(self, in_days):
        return self.json_10days_weather['forecast']['simpleforecast']['forecastday'][in_days]['icon_url']

    def get_today_next_hours(self):
        hour = self.get_hour_now()
        hours = []
        for i in range(hour+1, 24):
            hours.append('{:02}:00'.format(i))
        return hours

    def get_today_hourly_temperature(self):
        hour = self.get_hour_now()
        dataset = []
        for i in range(len(self.get_today_next_hours())):
            dataset.append(int(self.json_hourly_weather['hourly_forecast'][i]['temp']['metric']))
        return dataset

    def get_today_hourly_rain(self):
        hour = self.get_hour_now()
        dataset = []
        for i in range(len(self.get_today_next_hours())):
            dataset.append(int(self.json_hourly_weather['hourly_forecast'][i]['qpf']['metric']))
        return dataset

    def get_tomorrow_next_hours(self):
        hours = []
        for i in range(0,24):
            #hours.append('{}:00'.format(i))
            hours.append(i)
        return hours

    def get_tomorrow_hourly_temperature(self):
        hour = self.get_hour_now()
        dataset = []
        for i in range(0,24):
            dataset.append(int(self.json_hourly_weather['hourly_forecast'][23-hour+i]['temp']['metric']))
        return dataset

    def get_tomorrow_hourly_rain(self):
        hour = self.get_hour_now()
        dataset = []
        for i in range(0,24):
            dataset.append(int(self.json_hourly_weather['hourly_forecast'][23-hour+i]['qpf']['metric']))
        return dataset
       
