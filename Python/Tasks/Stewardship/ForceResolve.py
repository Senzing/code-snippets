#! /usr/bin/env python3

import json
import os
import sys
from senzing import (
    G2Engine,
    G2EngineFlags,
    G2Exception,
)

engine_config_json = os.getenv("SENZING_ENGINE_CONFIGURATION_JSON", None)
get_ent_response = bytearray()
get1_rec_response = bytearray()
get2_rec_response = bytearray()
purge_msg = """
********** WARNING **********
This example will purge all currently loaded data from the senzing database!
Before proceeding, all instances of senzing (custom code, rest api, redoer, etc.) must be shut down.
********** WARNING **********

Are you sure you want to continue and purge the senzing database? (y/n) """
response = bytearray()
records = [
    {
        "DATA_SOURCE": "TEST",
        "RECORD_ID": "1",
        "PRIMARY_NAME_FULL": "Patrick Smith",
        "AKA_NAME_FULL": "Paddy Smith",
        "ADDR_FULL": "787 Rotary Dr, Rotorville, RI, 78720",
        "PHONE_NUMBER": "787-767-2688",
        "DATE_OF_BIRTH": "1/12/1990",
    },
    {
        "DATA_SOURCE": "TEST",
        "RECORD_ID": "2",
        "PRIMARY_NAME_FULL": "Patricia Smith",
        "ADDR_FULL": "787 Rotary Dr, Rotorville, RI, 78720",
        "PHONE_NUMBER": "787-767-2688",
        "DATE_OF_BIRTH": "5/4/1994",
    },
    {
        "DATA_SOURCE": "TEST",
        "RECORD_ID": "3",
        "PRIMARY_NAME_FULL": "Pat Smith",
        "ADDR_FULL": "787 Rotary Dr, Rotorville, RI, 78720",
        "PHONE_NUMBER": "787-767-2688",
    },
]

if input(purge_msg) not in ["y", "Y", "yes", "YES"]:
    sys.exit()

try:
    g2_engine = G2Engine()
    g2_engine.init("G2Engine", engine_config_json, False)

    g2_engine.purgeRepository()

    for record in records:
        data_source = record["DATA_SOURCE"]
        record_id = record["RECORD_ID"]
        g2_engine.addRecord(data_source, record_id, json.dumps(record))
        print(f"Record {record_id} added")

    g2_engine.getEntityByRecordID("TEST", "3", response)

    response_json = json.loads(response.decode())
    print(
        f'\nEntity {response_json["RESOLVED_ENTITY"]["ENTITY_ID"]} -'
        f' {response_json["RESOLVED_ENTITY"]["ENTITY_NAME"]} is currently related to:'
    )

    for rel_entity in response_json["RELATED_ENTITIES"]:
        print(
            f'  Entity {rel_entity["ENTITY_ID"]} - {rel_entity["ENTITY_NAME"]} as'
            f' {rel_entity["MATCH_LEVEL_CODE"]} with {rel_entity["MATCH_KEY"]}'
        )

    print()
    for record_id in ("1", "2", "3"):
        g2_engine.getEntityByRecordID(
            "TEST",
            record_id,
            get_ent_response,
            G2EngineFlags.G2_ENTITY_BRIEF_DEFAULT_FLAGS,
        )
        get_json = json.loads(get_ent_response)
        print(
            f"Record {record_id} currently resolves to entity"
            f" {get_json['RESOLVED_ENTITY']['ENTITY_ID']}"
        )

    print("\nUpdating records...\n")
    g2_engine.getRecord("TEST", "1", get1_rec_response)
    g2_engine.getRecord("TEST", "3", get2_rec_response)
    get1_json = json.loads(get1_rec_response)
    get2_json = json.loads(get2_rec_response)
    get1_json["JSON_DATA"].update(
        {"TRUSTED_ID_NUMBER": "TEST_R1-TEST_R3", "TRUSTED_ID_TYPE": "FORCE_RESOLVE"}
    )
    get2_json["JSON_DATA"].update(
        {"TRUSTED_ID_NUMBER": "TEST_R1-TEST_R3", "TRUSTED_ID_TYPE": "FORCE_RESOLVE"}
    )
    g2_engine.replaceRecord("TEST", "1", json.dumps(get1_json["JSON_DATA"]))
    g2_engine.replaceRecord("TEST", "3", json.dumps(get2_json["JSON_DATA"]))

    for record_id in ("1", "2", "3"):
        g2_engine.getEntityByRecordID(
            "TEST",
            record_id,
            get_ent_response,
            G2EngineFlags.G2_ENTITY_BRIEF_DEFAULT_FLAGS,
        )
        get_json = json.loads(get_ent_response)
        print(
            f"Record {record_id} now resolves to entity"
            f" {get_json['RESOLVED_ENTITY']['ENTITY_ID']}"
        )

    g2_engine.destroy()
except G2Exception as err:
    print(err)
