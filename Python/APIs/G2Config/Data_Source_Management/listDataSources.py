#! /usr/bin/env python3

import os
import sys
from senzing import G2Config, G2ConfigMgr, G2BadInputException, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = os.getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)
current_config = bytearray()
current_config_id = bytearray()
data_sources = bytearray()

try:
    g2_config = G2Config()
    g2_config_mgr = G2ConfigMgr()

    g2_config.init('G2Config', engine_config_json, False)
    g2_config_mgr.init('G2ConfigMgr', engine_config_json, False)

    g2_config_mgr.getDefaultConfigID(current_config_id)
    g2_config_mgr.getConfig(current_config_id, current_config)
    config_handle = g2_config.load(current_config)

    g2_config.listDataSources(config_handle, data_sources)
    g2_config.close(config_handle)

    g2_config.destroy()
    g2_config_mgr.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception) as ex:
    print(ex)
    sys.exit(-1)

print(data_sources.decode())
