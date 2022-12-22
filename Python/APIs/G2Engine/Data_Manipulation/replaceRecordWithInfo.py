#! /usr/bin/env python3

import os
import sys
from senzing import G2BadInputException, G2Engine, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = os.getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)
RECORD = '''{"RECORD_TYPE": "PERSON",
             "PRIMARY_NAME_LAST": "Smith",
             "PRIMARY_NAME_FIRST": "Robert",
             "DATE_OF_BIRTH": "12/11/1978",
             "GENDER": "M",
             "ADDR_TYPE": "MAILING", 
             "ADDR_LINE1": 
             "123 Main Street, Las Vegas NV 89132", 
             "PHONE_TYPE": "HOME", 
             "PHONE_NUMBER": "702-919-1300", 
             "EMAIL_ADDRESS": "bsmith@work.com", 
             "DATE": "1/2/18", 
             "STATUS": "Active", 
             "AMOUNT": "100"}'''
with_info = bytearray()

try:
    g2_engine = G2Engine()
    g2_engine.init('G2Engine', engine_config_json, False)
    g2_engine.replaceRecordWithInfo('TEST', '1001', RECORD, with_info)
    g2_engine.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception)as ex:
    print(ex)
    sys.exit(-1)

print(with_info.decode())
