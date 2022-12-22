#! /usr/bin/env python3

import os
import sys
from senzing import G2ConfigMgr, G2BadInputException, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = os.getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)
current_config_id = bytearray()
config = bytearray()

try:
    g2_config_mgr = G2ConfigMgr()
    g2_config_mgr.init('G2ConfigMgr', engine_config_json, False)
    g2_config_mgr.getDefaultConfigID(current_config_id)
    g2_config_mgr.getConfig(current_config_id.decode(), config)
    g2_config_mgr.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception) as ex:
    print(ex)
    sys.exit(-1)

print(config.decode())
