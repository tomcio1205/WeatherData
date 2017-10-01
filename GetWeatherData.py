import configparser

parser = configparser.ConfigParser()
parser.read('config.cfg')


def get_config_parameter(section, option):
	try:
		opt = parser.get(section, option)
		return opt
	except configparser.NoOptionError:
		print("That option not exist=")

get_config_parameter('API', 'url')
print("test")
