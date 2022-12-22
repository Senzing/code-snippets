#! /usr/bin/env python3

import os
import sys
from senzing import G2BadInputException, G2Engine, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = os.getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)
RECORD = '''{"RECORD_TYPE": "PERSON",
             "PRIMARY_NAME_LAST": "Kusha",
             "PRIMARY_NAME_FIRST": "Eddie",
             "DATE_OF_BIRTH": "Mar 1 1970",
             "ADDR_TYPE": "HOME",
             "ADDR_LINE1": "1304 Poppy Hills Dr",
             "ADDR_CITY": "Blacklick",
             "ADDR_STATE": "OHIO",
             "DATE": "1/8/16",
             "STATUS": "Inactive",
             "AMOUNT": "700"}'''
record_id = bytearray()
with_info = bytearray()

try:
    g2_engine = G2Engine()
    g2_engine.init('G2Engine', engine_config_json, False)
    g2_engine.addRecordWithInfoWithReturnedRecordID('TEST', RECORD, record_id, with_info)
    g2_engine.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception)as ex:
    print(ex)
    sys.exit(-1)

print(f'Record ID: {record_id.decode()}')
print(f'With Info: {with_info.decode()}')
