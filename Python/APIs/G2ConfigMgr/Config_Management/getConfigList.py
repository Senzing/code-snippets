#! /usr/bin/env python3

import os
import sys
from senzing import G2ConfigMgr, G2BadInputException, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = os.getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)
config_list = bytearray()

try:
    g2_config_mgr = G2ConfigMgr()
    g2_config_mgr.init('G2ConfigMgr', engine_config_json, False)
    g2_config_mgr.getConfigList(config_list)
    g2_config_mgr.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception) as ex:
    print(ex)
    sys.exit(-1)

print(config_list.decode())
