#! /usr/bin/env python3

from json import loads
from os import getenv
from sys import exit
from senzing import G2BadInputException, G2Engine, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)
stats = bytearray()

with open('../../../../Resources/Data/load-5K.json', 'r') as file:
    records = [next(file) for i in range(100)]

try:
    g2_engine = G2Engine()
    g2_engine.init('G2Engine', engine_config_json, False)

    for record in records:
        data_source = loads(record)['DATA_SOURCE']
        record_id = loads(record)['RECORD_ID']
        g2_engine.addRecord(data_source, record_id, record)

    g2_engine.stats(stats)

    g2_engine.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception) as ex:
    print(ex)
    exit(-1)

print(stats.decode())