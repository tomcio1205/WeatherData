import configparser

config = configparser.RawConfigParser()


config.add_section('API')
config.set('API', 'api_key', '4a0d3cc607e3f12cae449fdb8f1c9d20')
config.set('API', 'url', 'http://api.openweathermap.org')
config.set('API', 'city', 'Rzeszow')
config.set('API', 'units', 'metric')

with open('config.cfg', 'w') as configfile:
    config.write(configfile)