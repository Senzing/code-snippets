#! /usr/bin/env python3

from os import getenv
from sys import exit
from senzing import G2BadInputException, G2Engine, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)
config_id = 193870676

try:
    g2_engine = G2Engine()
    g2_engine.initWithConfigID('G2Engine', engine_config_json, config_id, False)
    g2_engine.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception) as ex:
    print(ex)
    exit(-1)

print(f'G2Engine initialized (then destroyed) with config ID: {config_id}')
