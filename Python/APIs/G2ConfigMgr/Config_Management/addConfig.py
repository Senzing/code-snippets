#! /usr/bin/env python3

import os
import sys
from senzing import G2ConfigMgr, G2BadInputException, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = os.getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)
current_config_id = bytearray()
current_config = bytearray()
new_config_id = bytearray()

with open('../../../../Resources/Configs/Test_Config.json', 'r') as file:
    config = file.read().strip()

try:
    g2_config_mgr = G2ConfigMgr()
    g2_config_mgr.init('G2ConfigMgr', engine_config_json, False)
    g2_config_mgr.addConfig(config, 'Testing adding a config.', new_config_id)
    g2_config_mgr.setDefaultConfigID(new_config_id.decode())
    g2_config_mgr.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception) as ex:
    print(ex)
    sys.exit(-1)

print(f'Configuration added, new configuration ID: {new_config_id.decode()}')
