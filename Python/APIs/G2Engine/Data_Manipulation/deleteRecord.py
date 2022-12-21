#! /usr/bin/env python3

from os import getenv
from sys import exit
from senzing import G2BadInputException, G2Engine, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)

try:
    g2_engine = G2Engine()
    g2_engine.init('G2Engine', engine_config_json, False)
    g2_engine.deleteRecord('TEST', '1001')
    g2_engine.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception)as ex:
    print(ex)
    exit(-1)

print('Record deleted')
