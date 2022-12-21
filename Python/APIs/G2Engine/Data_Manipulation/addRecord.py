#! /usr/bin/env python3

from os import getenv
from sys import exit
from senzing import G2BadInputException, G2Engine, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)
record = '''{"RECORD_TYPE": "PERSON",
             "PRIMARY_NAME_LAST": "Smith",
             "PRIMARY_NAME_FIRST": "Robert",
             "DATE_OF_BIRTH": "12/11/1978",
             "ADDR_TYPE": "MAILING", 
             "ADDR_LINE1": 
             "123 Main Street, Las Vegas NV 89132", 
             "PHONE_TYPE": "HOME", 
             "PHONE_NUMBER": "702-919-1300", 
             "EMAIL_ADDRESS": "bsmith@work.com", 
             "DATE": "1/2/18", 
             "STATUS": "Active", 
             "AMOUNT": "100"}'''

try:
    g2_engine = G2Engine()
    g2_engine.init('G2Engine', engine_config_json, False)
    g2_engine.addRecord('TEST', '1001', record)
    g2_engine.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception)as ex:
    print(ex)
    exit(-1)

print('Record added')
