#! /usr/bin/env python3

from datetime import datetime
import os
import sys
from senzing import G2BadInputException, G2Engine, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = os.getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)
last_mod_time = bytearray()

try:
    g2_engine = G2Engine()
    g2_engine.init('G2Engine', engine_config_json, False)
    g2_engine.getRepositoryLastModifiedTime(last_mod_time)
    g2_engine.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception) as ex:
    print(ex)
    sys.exit(-1)

print(f'Timestamp: {last_mod_time.decode()}')
print(f'Date time: {datetime.fromtimestamp(int(int(last_mod_time.decode()) / 1000))}')
