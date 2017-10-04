# -*- coding: utf-8 -*-
import requests
import logging
import json

from datetime import datetime
from GetConfig import GetConfigParam
from DBConnection.DatabaseConnection import PostgresConnection

logging.basicConfig(filename='WeatherData.log', level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

CONFIG_FILENAME = 'config.cfg'


def get_weather_data(url, api_key, city):
	url = url + api_key + '/conditions/q/CA/' + city + '.json'

	response = requests.post(url)
	response_json = response.json()
	return {
		'temp_c': response_json['current_observation']['temp_c'],
		'city': response_json['current_observation']['display_location']['city'],
		'relative_humidity': response_json['current_observation']['relative_humidity'],
		'wind_dir': response_json['current_observation']['wind_dir'],
		'wind_degrees': response_json['current_observation']['wind_degrees'],
		'wind_kph': response_json['current_observation']['wind_kph'],
		'pressure_mb': response_json['current_observation']['pressure_mb'],
		'visibility_km': response_json['current_observation']['visibility_km'],
		'precip_1hr_string': response_json['current_observation']['precip_1hr_string'],
		'precip_1hr_in': response_json['current_observation']['precip_1hr_in'],
		'precip_today_string': response_json['current_observation']['precip_today_string'],
		'precip_today_in': response_json['current_observation']['precip_today_in'],
		'weather': response_json['current_observation']['weather'],
		'response_conditions_body': json.dumps(response_json)
	}


def get_astronomy_data(url, api_key, city):
	url = url + api_key + '/astronomy/q/CA/' + city + '.json'

	response = requests.post(url)
	response_json = response.json()
	sunset, sunrise = datetime.now(), datetime.now()
	sunrise = sunrise.replace(hour=int(response_json['sun_phase']['sunrise']['hour']))
	sunrise = sunrise.replace(minute=int(response_json['sun_phase']['sunrise']['minute']))
	sunset = sunset.replace(hour=int(response_json['sun_phase']['sunset']['hour']))
	sunset = sunset.replace(minute=int(response_json['sun_phase']['sunset']['minute']))
	moon_phase = response_json['moon_phase']['phaseofMoon']
	return {
		'moon_phase': moon_phase,
		'sunset': str(sunset),
		'sunrise': str(sunrise),
		'response_astronomy_body': json.dumps(response_json)
	}


def execute_query(query, params, args=()):
	with PostgresConnection(params, query, args) as ps:
		return ps


if __name__ == '__main__':
	logging.debug("Weather data saving process start")
	cfg = GetConfigParam(CONFIG_FILENAME)
	api_param = cfg.get_config_parameter('API')
	database_param = cfg.get_config_parameter('Database')
	weather_data = get_weather_data(api_param['url'], api_param['api_key'], api_param['city'])
	astronomy_data = get_astronomy_data(api_param['url'], api_param['api_key'], api_param['city'])
	query_data = {**astronomy_data, **weather_data}
	query = """
	INSERT INTO new_weather_data(
            temp_c, city, relative_humidity, wind_dir, wind_degrees,
            wind_kph, pressure_mb, visibility_km, precip_1hr_string, precip_1hr_in,
            precip_today_string, precip_today_in, weather, sunrise, sunset,
            moon_phase, response_astronomy_body, response_conditions_body)
    VALUES (%(temp_c)s, %(city)s, %(relative_humidity)s, %(wind_dir)s, %(wind_degrees)s,
            %(wind_kph)s, %(pressure_mb)s, %(visibility_km)s, %(precip_1hr_string)s, %(precip_1hr_in)s,
            %(precip_today_string)s, %(precip_today_in)s, %(weather)s, %(sunrise)s, %(sunset)s,
            %(moon_phase)s, %(response_astronomy_body)s, %(response_conditions_body)s)
	"""

	execute_query(query, database_param, query_data)
	logging.debug("Weather data saving process finished")
