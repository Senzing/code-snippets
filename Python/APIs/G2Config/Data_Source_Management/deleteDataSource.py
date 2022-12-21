#! /usr/bin/env python3

from os import getenv
from sys import exit
from senzing import G2Config, G2ConfigMgr, G2BadInputException, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)
add_response = bytearray()
current_config = bytearray()
current_config_id = bytearray()
new_config = bytearray()
new_config_id = bytearray()


try:
    g2_config = G2Config()
    g2_config_mgr = G2ConfigMgr()

    g2_config.init('G2Config', engine_config_json, False)
    g2_config_mgr.init('G2ConfigMgr', engine_config_json, False)

    g2_config_mgr.getDefaultConfigID(current_config_id)
    g2_config_mgr.getConfig(current_config_id, current_config)

    config_handle = g2_config.load(current_config)

    g2_config.deleteDataSource(config_handle, '{"DSRC_CODE": "MYTEST"}')
    g2_config.save(config_handle, new_config)
    g2_config.close(config_handle)

    g2_config_mgr.addConfig(new_config, f'Data source deleted', new_config_id)
    g2_config_mgr.setDefaultConfigID(new_config_id)

    g2_config.destroy()
    g2_config_mgr.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception) as ex:
    print(ex)
    exit(-1)

print(f'Datasource deleted, new default config ID: {new_config_id.decode()}')
