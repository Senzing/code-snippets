#! /usr/bin/env python3

from os import getenv
from sys import exit
from senzing import G2ConfigMgr, G2BadInputException, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)
config_id = 1646704028

try:
    g2_config_mgr = G2ConfigMgr()
    g2_config_mgr.init('G2ConfigMgr', engine_config_json, False)
    g2_config_mgr.setDefaultConfigID(config_id)
    g2_config_mgr.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception) as ex:
    print(ex)
    exit(-1)

print(f'Default config ID set to: {config_id}')
