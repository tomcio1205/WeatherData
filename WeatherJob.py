# -*- coding: utf-8 -*-
import requests
import logging

from GetConfig import GetConfigParam
from DBConnection.DatabaseConnection import PostgresConnection

logging.basicConfig(filename='WeatherData.log', level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

CONFIG_FILENAME = 'config.cfg'


def get_weather_data(**data):
	url = data['url'] + '/data/2.5/weather?q=' + data['city'] + '&' + 'units=' +\
	      data['units'] + '&' + 'appid=' + data['api_key']

	response = requests.post(url)
	response_json = response.json()
	logging.debug("Response : " + str(response_json))
	return {
		'cloudiness': response_json['clouds']['all'],
		'city': response_json['name'],
		'humidity': response_json['main']['humidity'],
		'pressure': response_json['main']['pressure'],
		'temp': response_json['main']['temp'],
		'sunrise': response_json['sys']['sunrise'],
		'sunset': response_json['sys']['sunset'],
		'weather_description': response_json['weather'][0]['description'],
		'rain': response_json['rain']['3h'] if 'rain' in response_json else 0,
		'snow': response_json['snow']['3h'] if 'snow' in response_json else 0,
		'weather_description': response_json['weather'][0]['description'],
		'wind_speed': response_json['wind']['speed'],
		'wind_deg': response_json['wind']['deg'],
		'visibility': response_json['visibility'],

	}


def execute_query(query, params, args=()):
	with PostgresConnection(params, query, args) as ps:
		return ps

if __name__ == '__main__':
	logging.debug("Weather data saving process start")
	cfg = GetConfigParam(CONFIG_FILENAME)
	api_param = cfg.get_config_parameter('API')
	database_param = cfg.get_config_parameter('Database')
	weather_data = get_weather_data(**api_param)
	query = "insert into weather_data (city, humidity, weather_description, wind_speed, visibility, sunrise, sunset," \
	        " cloudiness, temp, pressure, wind_deg, rain, snow)" \
	        " values (%(city)s, %(humidity)s, %(weather_description)s, %(wind_speed)s, %(visibility)s," \
			" to_timestamp(%(sunrise)s), to_timestamp(%(sunset)s), %(cloudiness)s, %(temp)s, %(pressure)s, %(wind_deg)s, %(rain)s, %(snow)s)"
	execute_query(query, database_param, weather_data)
	logging.debug("Weather data saving process finished")
