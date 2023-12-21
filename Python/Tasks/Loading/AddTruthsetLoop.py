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


def mock_logger(level, exception, error_rec=None):
    print(f"\n{level}: {exception}", file=sys.stderr)
    if error_rec:
        print(f"{error_rec}", file=sys.stderr)


def add_records_from_file(engine, input_file):
    success_recs = error_recs = 0

    with open(input_file, "r") as file:
        print(f"\nAdding records from {input_file}")

        for rec_to_add in file:
            try:
                record_dict = json.loads(rec_to_add)
                data_source = record_dict.get("DATA_SOURCE", None)
                record_id = record_dict.get("RECORD_ID", None)
                engine.addRecord(data_source, record_id, rec_to_add)
            except (G2BadInputException, json.JSONDecodeError) as err:
                mock_logger("ERROR", err, rec_to_add)
                error_recs += 1
            except G2RetryableException as err:
                mock_logger("WARN", err, rec_to_add)
                error_recs += 1
            except (G2UnrecoverableException, G2Exception) as err:
                mock_logger("CRITICAL", err, rec_to_add)
                raise
            else:
                success_recs += 1

            if success_recs % 500 == 0:
                print(f"Processed {success_recs:,} adds, with {error_recs:,} errors")

    print(f"Successfully loaded {success_recs:,} records, with {error_recs:,} errors")


try:
    g2_engine = G2Engine()
    g2_engine.init("G2Engine", engine_config_json, False)
    add_records_from_file(g2_engine, "../../../Resources/Data/truth/customers.json")
    add_records_from_file(g2_engine, "../../../Resources/Data/truth/reference.json")
    add_records_from_file(g2_engine, "../../../Resources/Data/truth/watchlist.json")
    g2_engine.destroy()
except G2Exception as err:
    print(err)
