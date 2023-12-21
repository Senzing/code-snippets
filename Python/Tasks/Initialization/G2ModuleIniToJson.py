#! /usr/bin/env python3

import configparser

ini_file_name = "../../../Resources/G2Module/G2Module.ini"
engine_config_json = {}

cfgp = configparser.ConfigParser()
cfgp.optionxform = str
cfgp.read(ini_file_name)

for section in cfgp.sections():
    engine_config_json[section] = dict(cfgp.items(section))

print(engine_config_json)
