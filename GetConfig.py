import configparser


class GetConfigParam(object):
	def __init__(self, file_name):
		self.parser = configparser.ConfigParser()
		self.parser.read(file_name)

	def get_config_parameter(self, section, option):
		try:
			opt = self.parser.get(section, option)
			return opt
		except configparser.NoOptionError:
			print("That option not exist")
			return 0
