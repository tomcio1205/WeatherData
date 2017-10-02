import requests
import logging

from GetConfig import GetConfigParam

logging.basicConfig(filename='WeatherData.log', level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

CONFIG_FILENAME = 'config.cfg'


def get_weather_data(**data):
	url = data['url'] + '/data/2.5/weather?q=' + data['city'] + '&' + 'units=' + data['units'] + '&' + 'appid=' + data['api_key']

	response = requests.post(url)
	response_json = response.json()
	logging.debug(str(response_json))
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


def get_config_param(cfg):
	return {
		'city': cfg.get_config_parameter('API', 'city'),
		'url': cfg.get_config_parameter('API', 'url'),
		'api_key': cfg.get_config_parameter('API', 'api_key'),
		'units': cfg.get_config_parameter('API', 'units')
	}

if __name__ == '__main__':
	cfg = GetConfigParam(CONFIG_FILENAME)
	config_param = get_config_param(cfg)
	x = get_weather_data(**config_param)
	print(str(x))