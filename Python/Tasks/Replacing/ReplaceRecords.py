#! /usr/bin/env python3

import json
import os
import sys
from senzing import (
    G2BadInputException,
    G2Engine,
    G2Exception,
    G2RetryableException,
    G2UnrecoverableException,
)

engine_config_json = os.getenv("SENZING_ENGINE_CONFIGURATION_JSON", None)

replace_records = [
    {
        "DATA_SOURCE": "TEST",
        "SOCIAL_HANDLE": "flavour",
        "DATE_OF_BIRTH": "4/8/1983",
        "ADDR_STATE": "LA",
        "ADDR_POSTAL_CODE": "71232",
        "SSN_NUMBER": "053-39-3251",
        "GENDER": "F",
        "srccode": "MDMPER",
        "CC_ACCOUNT_NUMBER": "5534202208773608",
        "RECORD_ID": "386820964",
        "ADDR_CITY": "Delhi",
        "DRIVERS_LICENSE_STATE": "DE",
        "PHONE_NUMBER": "225-671-9087",
        "NAME_LAST": "SEAMAN",
        "ADDR_LINE1": "772 Armstrong RD",
    },
    {
        "DATA_SOURCE": "TEST",
        "DATE_OF_BIRTH": "6/2/1952",
        "ADDR_STATE": "TX",
        "ADDR_POSTAL_CODE": "75215",
        "SSN_NUMBER": "501-27-9836",
        "GENDER": "M",
        "srccode": "MDMPER",
        "CC_ACCOUNT_NUMBER": "50185881568895705",
        "RECORD_ID": "181734352",
        "ADDR_CITY": "Dlalas",
        "DRIVERS_LICENSE_NUMBER": "V995121498988",
        "DRIVERS_LICENSE_STATE": "MD",
        "PHONE_NUMBER": "347-4506",
        "NAME_LAST": "THOMPSON",
        "ADDR_LINE1": "788 Alma ST",
    },
    {
        "DATA_SOURCE": "TEST",
        "DATE_OF_BIRTH": "5/5/1946",
        "ADDR_STATE": "TX",
        "ADDR_POSTAL_CODE": "75234",
        "SSN_NUMBER": "299-21-8788",
        "NAME_FIRST": "AUNA",
        "GENDER": "F",
        "srccode": "MDMPER",
        "RECORD_ID": "314249610",
        "ADDR_CITY": "DalXlas",
        "DRIVERS_LICENSE_STATE": "AL",
        "PHONE_NUMBER": "682-282-9435",
        "NAME_LAST": "HAUPTMAN",
        "ADDR_LINE1": "1438 Albemarle DR",
    },
    {
        "DATA_SOURCE": "TEST",
        "ADDR_STATE": "CA",
        "ADDR_POSTAL_CODE": "90012",
        "SSN_NUMBER": "202-09-1656",
        "NAME_FIRST": "JEREMY",
        "GENDER": "M",
        "srccode": "MDMPER",
        "CC_ACCOUNT_NUMBER": "374561958104783",
        "RECORD_ID": "399059018",
        "ADDR_CITY": "Los Angles",
        "DRIVERS_LICENSE_NUMBER": "419243052",
        "DRIVERS_LICENSE_STATE": "KO",
        "PHONE_NUMBER": "213-862-0665",
        "NAME_LAST": "WHITE",
        "ADDR_LINE1": "2292 1st ST",
    },
    {
        "DATA_SOURCE": "TEST",
        "ADDR_STATE": "NY",
        "ADDR_POSTAL_CODE": "14626",
        "NAME_FIRST": "KYLE",
        "GENDER": "M",
        "srccode": "MDMPER",
        "RECORD_ID": "441460361",
        "ADDR_CITY": "Rotchester",
        "DRIVERS_LICENSE_NUMBER": "928877314",
        "PHONE_NUMBER": "669-1853",
        "NAME_LAST": "WILLIAMS",
        "NAME_SUFFIX": "IV",
        "ADDR_LINE1": "1874 Brooks AVE",
    },
]


def mock_logger(level, exception, error_rec=None):
    print(f"\n{level}: {exception}", file=sys.stderr)
    if error_rec:
        print(f"{error_rec}", file=sys.stderr)


def replacer(engine):
    for rec_to_replace in replace_records:
        try:
            data_source = rec_to_replace.get("DATA_SOURCE", None)
            record_id = rec_to_replace.get("RECORD_ID", None)
            engine.replaceRecord(data_source, record_id, json.dumps(rec_to_replace))
        except (G2BadInputException, json.JSONDecodeError) as err:
            mock_logger("ERROR", err, rec_to_replace)
        except G2RetryableException as err:
            mock_logger("WARN", err, rec_to_replace)
        except (G2UnrecoverableException, G2Exception) as err:
            mock_logger("CRITICAL", err, rec_to_replace)
            raise
        else:
            print(
                f"\nRecord replaced - data source = {data_source} - record id ="
                f" {record_id}"
            )


try:
    g2_engine = G2Engine()
    g2_engine.init("G2Engine", engine_config_json, False)
    replacer(g2_engine)
    g2_engine.destroy()
except G2Exception as err:
    mock_logger("CRITICAL", err)
