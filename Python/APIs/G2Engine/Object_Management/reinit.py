#! /usr/bin/env python3

from os import getenv
from sys import exit
from senzing import G2Engine, G2ConfigMgr, G2BadInputException, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)
new_config_id = bytearray()


def config_ids():
    active_id = bytearray()
    config_id = bytearray()

    g2_engine.getActiveConfigID(active_id)
    g2_config_mgr.getDefaultConfigID(config_id)
    print(f'Active ID: {active_id.decode()} - Default ID: {config_id.decode()}')


with open('../../../../Resources/Configs/Test_Config2.json', 'r') as file:
    config = file.read().strip()

try:
    g2_engine = G2Engine()
    g2_engine.init('G2Engine', engine_config_json, False)
    g2_config_mgr = G2ConfigMgr()
    g2_config_mgr.init('G2ConfigMgr', engine_config_json, False)

    config_ids()

    g2_config_mgr.addConfig(config, 'Testing reinit.', new_config_id)
    g2_config_mgr.setDefaultConfigID(new_config_id)

    config_ids()

    g2_engine.reinit(new_config_id)

    config_ids()

    g2_engine.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception) as ex:
    print(ex)
    exit(-1)
