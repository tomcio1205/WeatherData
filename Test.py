from GetConfig import GetConfigParam
import requests
CONFIG_FILENAME = 'config.cfg'


def get_weather_data(**data):
	url = data['url'] + '/data/2.5/weather?q=' + data['city'] + '&' + 'units=' + data['units'] + '&' + 'appid=' + data['api_key']

	r = requests.post(url)
	print(str(r.json()))


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
	get_weather_data(**config_param)