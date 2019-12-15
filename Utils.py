'''
Project X
Collection of utility functions

Instructor: Edwin Mach
Student: Andy Song
'''

from datetime import datetime
from API_Key import *
from urllib.request import urlopen
import json

from pprint import pprint


TYPE_OZONE = 'o3'
TYPE_CO = 'co'
TYPE_NO2 = 'no2'
TYPE_SO2 = 'so2'


class Utils():  
      
    def KelvinToCelsius(self, kelvinTemp):
        ''' Convert Kelvin tempeature to Celsiue
        
        input: Kelvin temperatuure
        output: return Celsius temperature
        '''
        
        return "{:.1f}".format(kelvinTemp - 273.15)
    
            
    def KelvinToFahrenheit(self, kelvinTemp):
        ''' Convert Kelvin tempeature to Fahrenheit
        
        input: Kelvin temperatuure
        output: returnFahrenheit temperature
        '''
        
        return "{:.1f}".format((kelvinTemp - 273.15)* 1.8000 + 32.00)
    
    
    def UnixToDatetime(self, unixTime):
        ''' Format unix date time to regular form
        
        input: unix time
        output: return date and time 
        '''
        
        return datetime.fromtimestamp(int(unixTime)).strftime('%Y-%m-%d %H:%M:%S')
    
        
    def MeterToMiles(self, meter):
        ''' Convert meter to mile
        
        input: meter
        output: return mile
        '''
        
        return "{:.2f}".format((meter * 0.00062137))
    
        
    def MpsToMph(self, meterPerSecond):
        ''' Convert meter per second to mile per hour
        
        input: meter per second
        output: return mile per hour
        '''
        
        return "{:.1f}".format((meterPerSecond * (2.23693629)))

    
class Coordinates():

    def GetCoordinatesOfCity(self, city='Saratoga,ca, us'):
        ''' Convert a city to coordinates (latitude, lobgitude)

        input: city {, country} String
        output: return coordinates (latitude, lobgitude)
        '''

        from geopy.geocoders import Nominatim

        self.geolocator = Nominatim(user_agent="Project X Get UVI of a City")

        try:
            self.location = self.geolocator.geocode(city)
        except:
            # if geopy failed, use OpenCageGeocode wensite
            from opencage.geocoder import OpenCageGeocode
            self.geocoder = OpenCageGeocode(OCD_API_KEY)
            self.results = self.geocoder.geocode(city)
            self.coordinates = {'latitude': self.results[0]['geometry']['lat'],
                                'longitude': self.results[0]['geometry']['lng']}
        else:
            self.coordinates = {'latitude': self.location.latitude,
                                'longitude': self.location.longitude}

        return (self.coordinates)


class OpenWeatherMapUVI():
    
    def GetOpenWeatherMapUVI(self, location):
        ''' Send UVI inquiry request to Open Weather Map Web Server
        Retrieve the response object from Web Server, 
        read the object, decode it and make it jason format
        
        input: location object
        output: return UVI data dictionary
        '''

        # Return UVI jason data from Open Weather Map Web Server
        #===========================================================================
        # uvi_api_response = {
        #     'date': '',
        #     'date_iso': '',
        #     'lat': '',
        #     'lon': '',
        #     'value': ''
        #     }
        #===========================================================================
    
        self.url = "http://api.openweathermap.org/data/2.5/uvi?lat={}&lon={}&appid={}".format(location['latitude'], location['longitude'], OWM_API_KEY)
        self.response = urlopen(self.url)
        self.data = self.response.read().decode()
        self.jsonData = json.loads(self.data) 

        return(self.jsonData)


class OpenWeatherMapWeather():
    
    def GetOpenWeatherMapWeather(self, city='London,uk'):
        ''' Send weather inquiry request Open Weather Map Web Server
        Retrieve the response object from Web Server, 
        read the object, decode it and make it jason format
        
        input: city
        output: return weather data dictionary, weather icon
        '''

        # Return weather jason data from Open Weather Map Web Server
        #===============================================================================
        # weather_api_response = {
        #  "coord": { "lon": "","lat": ""},
        #   "weather": [
        #     {
        #       "id": "",
        #       "main": "",
        #       "description": "",
        #       "icon": ""
        #     }
        #   ],
        #   "base": "",
        #   "main": {
        #     "temp": "",
        #     "pressure": "",
        #     "humidity": "",
        #     "temp_min": "",
        #     "temp_max": ""
        #   },
        #   "wind": {
        #     "speed": "",
        #     "deg": ""
        #   },
        #   "clouds": {
        #     "all": ""
        #   },
        #   "dt": "",
        #   "sys": {
        #     "type": "",
        #     "id": "",
        #     "message": "",
        #     "country": "",
        #     "sunrise": "",
        #     "sunset": ""
        #   },
        #   "timezone": "",
        #   "id": "",
        #   "name": "",
        #   "cod": ""        # }
        #===============================================================================
        
        self.url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(city, OWM_API_KEY) 
        self.response = urlopen(self.url)
        self.data = self.response.read().decode()
        self.jsonData = json.loads(self.data)
        
        #=======================================================================
        # pprint(self.response)
        # pprint(self.data)
        # pprint(self.jsonData)
        #=======================================================================
        
        # Gets corresponding weather icon
        self.weatherIcon = self.jsonData['weather'][0]['icon']
        self.urlIcon = "http://openweathermap.org/img/w/{}.png".format(self.weatherIcon)
        self.ico = urlopen(self.urlIcon)
        
        return(self.jsonData, self.ico)


class OpenWeatherMapPollution():
    
    def GetOpenWeatherMapPollution(self, location, type = TYPE_OZONE):
        ''' Send pollution inquiry request to Open Weather Map Web Server
        Retrieve the response object from Web Server, 
        read the object, decode it and make it jason format
        
        input: location object
        output: return pollution data dictionary
        '''
        
        # Return pollution jason data from Open Weather Map Web Server
        #===========================================================================
        # ozone_data_dict = {
        #     'data': '',
        #     'location': {'latitude': '',
        #                  'longitude': ''}
        #     'time': ''
        #     }
        #
        # co_data_dict = {
        #     'data': [{'precision': '', 'pressure': '', 'value': ''},
        #              {'precision': '', 'pressure': '', 'value': ''},
        #              ... 35x
        #             ]
        #     'location': {'latitude': '',
        #                  'longitude': ''}
        #     'time': ''
        #     }
        #
        # no2_data_dict = {
        #     'data': [{'precision': '', 'pressure': '', 'value': ''},
        #              {'precision': '', 'pressure': '', 'value': ''},
        #              ... 35x
        #             ]
        #     'location': {'latitude': '',
        #                  'longitude': ''}
        #     'time': ''
        #     }
        #
        # so2_data_dict = {
        #     'data': [{'precision': '', 'pressure': '', 'value': ''},
        #              {'precision': '', 'pressure': '', 'value': ''},
        #              ... 35x
        #             ]
        #     'location': {'latitude': '',
        #                  'longitude': ''}
        #     'time': ''
        #     }
        #
        #===========================================================================

        self.url = "http://api.openweathermap.org/pollution/v1/{}/{:03.1f},{:03.1f}/current.json?appid={}".format(type, location['latitude'], location['longitude'], OWM_API_KEY)
       
        try:
            self.response = urlopen(self.url)
        except:
            # Nitrogen Dioxide are not available yet
            self.jsonData = {'data': [{'precision': 'N/A',
                                       'pressure': 'N/A',
                                       'value': 'N/A'}]}
        else:
            self.data = self.response.read().decode()
            self.jsonData = json.loads(self.data) 

        #=======================================================================
        # pprint(self.url)
        # pprint(self.response)
        # pprint(self.data)
        # pprint(self.jsonData)
        #=======================================================================
        
        return(self.jsonData)
    

if __name__ == "__main__":
    coordinates = Coordinates()
    location = coordinates.GetCoordinatesOfCity()
      
    owmUvi = OpenWeatherMapUVI()
    owmUvi.GetOpenWeatherMapUVI(location)
     
    owmWeather = OpenWeatherMapWeather()
    owmWeather.GetOpenWeatherMapWeather()

    # Beta version only support the default coordinates
    location = {"latitude" : 0.00000000,
                "longitude" : 10.000000}
    owmPollution = OpenWeatherMapPollution()
    owmPollution.GetOpenWeatherMapPollution(location, TYPE_OZONE)
    owmPollution.GetOpenWeatherMapPollution(location, TYPE_CO)
    owmPollution.GetOpenWeatherMapPollution(location, TYPE_SO2)
    owmPollution.GetOpenWeatherMapPollution(location, TYPE_NO2)
