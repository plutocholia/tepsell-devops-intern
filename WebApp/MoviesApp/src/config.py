import json

with open('../config/config.json') as config_file:
    data = json.load(config_file)

mysql_configs = data['mysql']
redis_configs = data['redis']
logging_configs = data['log']
flask_configs = data['flask']
