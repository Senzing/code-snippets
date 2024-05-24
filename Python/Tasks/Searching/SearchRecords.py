#! /usr/bin/env python3

import json
import os
import sys

from senzing import (
    G2BadInputException,
    G2Engine,
    G2EngineFlags,
    G2Exception,
    G2RetryableException,
    G2UnrecoverableException,
)

engine_config_json = os.getenv("SENZING_ENGINE_CONFIGURATION_JSON", None)

search_records = [
    {
        "NAME_FULL": "Susan Moony",
        "DATE_OF_BIRTH": "15/6/1998",
        "SSN_NUMBER": "521212123",
    },
    {
        "NAME_FIRST": "Robert",
        "NAME_LAST": "Smith",
        "ADDR_FULL": "123 Main Street Las Vegas NV 89132",
    },
    {
        "NAME_FIRST": "Makio",
        "NAME_LAST": "Yamanaka",
        "ADDR_FULL": "787 Rotary Drive Rotorville FL 78720",
    },
]


def mock_logger(level, exception, error_rec=None):
    print(f"\n{level}: {exception}", file=sys.stderr)
    if error_rec:
        print(f"{error_rec}", file=sys.stderr)


def searcher(engine):
    for rec_to_search in search_records:
        try:
            rec_str = json.dumps(rec_to_search)
            search_response = bytearray()
            engine.searchByAttributes(
                rec_str,
                search_response,
                G2EngineFlags.G2_SEARCH_BY_ATTRIBUTES_MINIMAL_ALL,
            )
        except (G2BadInputException, json.JSONDecodeError) as err:
            mock_logger("ERROR", err, rec_str)
        except G2RetryableException as err:
            mock_logger("WARN", err, rec_str)
        except (G2UnrecoverableException, G2Exception) as err:
            mock_logger("CRITICAL", err, rec_str)
            raise
        else:
            response_str = search_response.decode()
            response_dict = json.loads(response_str)
            response_entities = response_dict.get("RESOLVED_ENTITIES", None)

            print("-" * 100)
            if response_entities:
                print(f"Result for {rec_str}:\n\n{response_str}\n")
            else:
                print(f"No result for {rec_str}\n")


try:
    g2_engine = G2Engine()
    g2_engine.init("G2Engine", engine_config_json, False)
    searcher(g2_engine)
    g2_engine.destroy()
except G2Exception as err:
    mock_logger("CRITICAL", err)
