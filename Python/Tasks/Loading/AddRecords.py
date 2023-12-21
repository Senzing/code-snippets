#! /usr/bin/env python3

import json
import os
from senzing import G2Engine, G2Exception

engine_config_json = os.getenv("SENZING_ENGINE_CONFIGURATION_JSON", None)
records = [
    {
        "DATA_SOURCE": "TEST",
        "RECORD_ID": "1001",
        "RECORD_TYPE": "PERSON",
        "PRIMARY_NAME_LAST": "Smith",
        "PRIMARY_NAME_FIRST": "Robert",
        "DATE_OF_BIRTH": "12/11/1978",
        "ADDR_TYPE": "MAILING",
        "ADDR_LINE1": "123 Main Street, Las Vegas NV 89132",
        "PHONE_TYPE": "HOME",
        "PHONE_NUMBER": "702-919-1300",
        "EMAIL_ADDRESS": "bsmith@work.com",
        "DATE": "1/2/18",
        "STATUS": "Active",
        "AMOUNT": "100",
    },
    {
        "DATA_SOURCE": "TEST",
        "RECORD_ID": "1002",
        "RECORD_TYPE": "PERSON",
        "PRIMARY_NAME_LAST": "Smith II",
        "PRIMARY_NAME_FIRST": "Bob",
        "DATE_OF_BIRTH": "11/12/1978",
        "ADDR_TYPE": "HOME",
        "ADDR_LINE1": "1515 Adela Lane",
        "ADDR_CITY": "Las Vegas",
        "ADDR_STATE": "NV",
        "ADDR_POSTAL_CODE": "89111",
        "PHONE_TYPE": "MOBILE",
        "PHONE_NUMBER": "702-919-1300",
        "DATE": "3/10/17",
        "STATUS": "Inactive",
        "AMOUNT": "200",
    },
    {
        "DATA_SOURCE": "TEST",
        "RECORD_ID": "1003",
        "RECORD_TYPE": "PERSON",
        "PRIMARY_NAME_LAST": "Smith",
        "PRIMARY_NAME_FIRST": "Bob",
        "PRIMARY_NAME_MIDDLE": "J",
        "DATE_OF_BIRTH": "12/11/1978",
        "EMAIL_ADDRESS": "bsmith@work.com",
        "DATE": "4/9/16",
        "STATUS": "Inactive",
        "AMOUNT": "300",
    },
    {
        "DATA_SOURCE": "TEST",
        "RECORD_ID": "1004",
        "RECORD_TYPE": "PERSON",
        "PRIMARY_NAME_LAST": "Smith",
        "PRIMARY_NAME_FIRST": "B",
        "ADDR_TYPE": "HOME",
        "ADDR_LINE1": "1515 Adela Ln",
        "ADDR_CITY": "Las Vegas",
        "ADDR_STATE": "NV",
        "ADDR_POSTAL_CODE": "89132",
        "EMAIL_ADDRESS": "bsmith@work.com",
        "DATE": "1/5/15",
        "STATUS": "Inactive",
        "AMOUNT": "400",
    },
    {
        "DATA_SOURCE": "TEST",
        "RECORD_ID": "1005",
        "RECORD_TYPE": "PERSON",
        "PRIMARY_NAME_LAST": "Smith",
        "PRIMARY_NAME_FIRST": "Rob",
        "PRIMARY_NAME_MIDDLE": "E",
        "DRIVERS_LICENSE_NUMBER": "112233",
        "DRIVERS_LICENSE_STATE": "NV",
        "ADDR_TYPE": "MAILING",
        "ADDR_LINE1": "123 E Main St",
        "ADDR_CITY": "Henderson",
        "ADDR_STATE": "NV",
        "ADDR_POSTAL_CODE": "89132",
        "DATE": "7/16/19",
        "STATUS": "Active",
        "AMOUNT": "500",
    },
]

try:
    g2_engine = G2Engine()
    g2_engine.init("G2Engine", engine_config_json, False)

    for record in records:
        data_source = record["DATA_SOURCE"]
        record_id = record["RECORD_ID"]
        g2_engine.addRecord(data_source, record_id, json.dumps(record))
        print(f"Record {record_id} added")

    g2_engine.destroy()
except G2Exception as err:
    print(err)
