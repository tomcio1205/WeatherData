import configparser


class GetConfigParam(object):
	def __init__(self, file_name):
		self.parser = configparser.ConfigParser()
		self.parser.read(file_name)

	def get_config_parameter(self, section):
		options = self.parser.options(section)
		ret_options = {}
		for option in options:
			ret_options[option] = self.parser.get(section, option)
		return ret_options

