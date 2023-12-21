#! /usr/bin/env python3

import json
import os
import sys
from collections import Counter
from senzing import (
    G2BadInputException,
    G2Engine,
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
            search_response = bytearray()
            engine.searchByAttributes(json.dumps(rec_to_search), search_response)
        except (G2BadInputException, json.JSONDecodeError) as err:
            mock_logger("ERROR", err, rec_to_search)
        except G2RetryableException as err:
            mock_logger("WARN", err, rec_to_search)
        except (G2UnrecoverableException, G2Exception) as err:
            mock_logger("CRITICAL", err, rec_to_search)
            raise
        else:
            response_dict = json.loads(search_response.decode())
            response_entities = response_dict.get("RESOLVED_ENTITIES", None)

            if response_entities:
                results_str = []
                results_count = Counter(
                    k
                    for entity in response_entities
                    for k in entity.keys()
                    if k.startswith("MATCH_INFO")
                )
                results_str.append(
                    f'\n{results_count["MATCH_INFO"]} results for'
                    f" {json.dumps(rec_to_search)}\n"
                )

                for idx, result in enumerate(response_entities, start=1):
                    results_str.append(f"\n  Result {idx}")
                    results_str.append(
                        "\n    Entity ID:      "
                        f" {result['ENTITY']['RESOLVED_ENTITY']['ENTITY_ID']}"
                    )
                    results_str.append(
                        "\n    Entity name:    "
                        f" {result['ENTITY']['RESOLVED_ENTITY']['ENTITY_NAME']}"
                    )
                    results_str.append(
                        f'\n    Match key:       {result["MATCH_INFO"]["MATCH_KEY"]}'
                    )
                    results_str.append("\n    Records summary: ")
                    for record_summary in result["ENTITY"]["RESOLVED_ENTITY"][
                        "RECORD_SUMMARY"
                    ]:
                        results_str.append(
                            f'{record_summary["DATA_SOURCE"]}:'
                            f' {record_summary["RECORD_COUNT"]}'
                            + "    "
                        )
                    results_str.append("\n")

                print("".join(results_str))
            else:
                print(f"\nNo result for {json.dumps(rec_to_search)}\n")


try:
    g2_engine = G2Engine()
    g2_engine.init("G2Engine", engine_config_json, False)
    searcher(g2_engine)
    g2_engine.destroy()
except G2Exception as err:
    mock_logger("CRITICAL", err)
