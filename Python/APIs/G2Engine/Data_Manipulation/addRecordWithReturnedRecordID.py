#! /usr/bin/env python3

import os
import sys
from senzing import G2BadInputException, G2Engine, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = os.getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)
record = '''{"RECORD_TYPE": "PERSON", 
             "PRIMARY_NAME_LAST": "Kusha", 
             "PRIMARY_NAME_FIRST": "Edward", 
             "DATE_OF_BIRTH": "3/1/1970", 
             "SSN_NUMBER": "294-66-9999", 
             "ADDR_TYPE": "HOME", "ADDR_LINE1": 
             "1304 Poppy Hills Dr", 
             "ADDR_CITY": "Blacklick", 
             "ADDR_STATE": "OH", 
             "ADDR_POSTAL_CODE": "43004", 
             "EMAIL_ADDRESS": "Kusha123@hmail.com", 
             "DATE": "1/7/18", 
             "STATUS": "Active", 
             "AMOUNT": "600"}'''
record_id = bytearray()

try:
    g2_engine = G2Engine()
    g2_engine.init('G2Engine', engine_config_json, False)
    g2_engine.addRecordWithReturnedRecordID('TEST', record_id, record)
    g2_engine.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception)as ex:
    print(ex)
    sys.exit(-1)

print(f'Record added, record ID: {record_id.decode()}')

