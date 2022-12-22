#! /usr/bin/env python3

import os
import sys
from senzing import G2BadInputException, G2Engine, G2EngineFlags, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = os.getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)
find_response = bytearray()

try:
    g2_engine = G2Engine()
    g2_engine.init('G2Engine', engine_config_json, False)
    g2_engine.findPathExcludingByRecordID('CUSTOMERS',
                                          '1019',
                                          'CUSTOMERS',
                                          '1020',
                                          2,
                                          '{"ENTITIES": [{"ENTITY_ID": "6"}]}',
                                          find_response,
                                          flags=G2EngineFlags.G2_FIND_PATH_DEFAULT_FLAGS)
    g2_engine.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception) as ex:
    print(ex)
    sys.exit(-1)

print(find_response.decode())
