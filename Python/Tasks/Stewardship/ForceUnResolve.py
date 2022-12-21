#! /usr/bin/env python3

import json
import os
import sys

from senzing import G2BadInputException, G2Engine, G2EngineFlags, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = os.getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)

try:
    g2_engine = G2Engine()
    g2_engine.init('G2Engine', engine_config_json, False)

    records = [
        {"DATA_SOURCE": "TEST", "RECORD_ID": "4", "PRIMARY_NAME_FULL": "Elizabeth Jonas", "ADDR_FULL": "202 Rotary Dr, Rotorville, RI, 78720", "SSN_NUMBER": "767-87-7678", "DATE_OF_BIRTH": "1/12/1990"},
        {"DATA_SOURCE": "TEST", "RECORD_ID": "5", "PRIMARY_NAME_FULL": "Beth Jones", "ADDR_FULL": "202 Rotary Dr, Rotorville, RI, 78720", "SSN_NUMBER": "767-87-7678", "DATE_OF_BIRTH": "1/12/1990"},
        {"DATA_SOURCE": "TEST", "RECORD_ID": "6", "PRIMARY_NAME_FULL": "Betsey Jones", "ADDR_FULL": "202 Rotary Dr, Rotorville, RI, 78720", "PHONE_NUMBER": "202-787-7678"},
    ]
    get_ent_response = bytearray()
    get1_rec_response = bytearray()
    get2_rec_response = bytearray()

    g2_engine.purgeRepository()

    for record in records:
        data_source = record['DATA_SOURCE']
        record_id = record['RECORD_ID']
        g2_engine.addRecord(data_source, record_id, json.dumps(record))
        print(f'Record {record_id} added...')

    print()
    for record_id in ('4', '5', '6'):
        g2_engine.getEntityByRecordID('TEST', record_id, get_ent_response, G2EngineFlags.G2_ENTITY_BRIEF_DEFAULT_FLAGS)
        get_json = json.loads(get_ent_response)
        print(f'Record {record_id} currently resolves to entity {get_json["RESOLVED_ENTITY"]["ENTITY_ID"]}')

    print(f'\nUpdating records...\n')
    g2_engine.getRecord('TEST', '4', get1_rec_response)
    g2_engine.getRecord('TEST', '6', get2_rec_response)
    get1_json = json.loads(get1_rec_response)
    get2_json = json.loads(get2_rec_response)
    get1_json["JSON_DATA"].update({"TRUSTED_ID_NUMBER": "TEST_R4-TEST_R6", "TRUSTED_ID_TYPE": "FORCE_UNRESOLVE"})
    get2_json["JSON_DATA"].update({"TRUSTED_ID_NUMBER": "TEST_R6-TEST_R4", "TRUSTED_ID_TYPE": "FORCE_UNRESOLVE"})
    g2_engine.replaceRecord('TEST', '4', json.dumps(get1_json["JSON_DATA"]))
    g2_engine.replaceRecord('TEST', '6', json.dumps(get2_json["JSON_DATA"]))

    for record_id in ('4', '5', '6'):
        g2_engine.getEntityByRecordID('TEST', record_id, get_ent_response, G2EngineFlags.G2_ENTITY_BRIEF_DEFAULT_FLAGS)
        get_json = json.loads(get_ent_response)
        print(f'Record {record_id} now resolves to entity {get_json["RESOLVED_ENTITY"]["ENTITY_ID"]}')

    g2_engine.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception, json.JSONDecodeError) as ex:
    print(ex)
    sys.exit(-1)
