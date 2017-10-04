import configparser

config = configparser.RawConfigParser()


config.add_section('API')
config.set('API', 'api_key', '4a0d3cc607e3f12cae449fdb8f1c9d20')
config.set('API', 'url', 'http://api.openweathermap.org')
config.set('API', 'city', 'Rzeszow')
config.set('API', 'units', 'metric')

config.add_section('Database')
config.set('Database', 'db_name', 'weather_data')
config.set('Database', 'db_user', 'postgres')
config.set('Database', 'db_password', 'postgres')
config.set('Database', 'db_host', '127.0.0.1')
config.set('Database', 'db_port', 5432)


with open('config.cfg', 'w') as configfile:
    config.write(configfile)
