#! /usr/bin/env python3

import os
import sys
from senzing import G2ConfigMgr, G2BadInputException, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = os.getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)
CURRENT_CONFIG_ID = 1646704028
NEW_CONFIG_ID = 1888647012

try:
    g2_config_mgr = G2ConfigMgr()
    g2_config_mgr.init('G2ConfigMgr', engine_config_json, False)
    g2_config_mgr.replaceDefaultConfigID(CURRENT_CONFIG_ID, NEW_CONFIG_ID)
    g2_config_mgr.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception) as ex:
    print(ex)
    sys.exit(-1)

print(f'Previous config ID {CURRENT_CONFIG_ID} replaced with {NEW_CONFIG_ID}')
