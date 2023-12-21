#! /usr/bin/env python3

import os
import sys
import time
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


def process_redo(engine):
    success_recs = error_recs = 0

    while True:
        try:
            redo_record = bytearray()
            engine.getRedoRecord(redo_record)

            if not redo_record:
                print(
                    "No redo records to process, pausing for 30 seconds. Total"
                    f" processed {success_recs:,} . (CTRL-C to exit)..."
                )
                time.sleep(30)
                continue

            engine.process(redo_record.decode())

            success_recs += 1
            if success_recs % 100 == 0:
                print(
                    f"Processed {success_recs:,} redo records, with"
                    f" {error_recs:,} errors"
                )
        except G2BadInputException as err:
            mock_logger("ERROR", err)
            error_recs += 1
        except G2RetryableException as err:
            mock_logger("WARN", err)
            error_recs += 1
        except (G2UnrecoverableException, G2Exception) as err:
            mock_logger("CRITICAL", err)
            raise


try:
    g2_engine = G2Engine()
    g2_engine.init("G2Engine", engine_config_json, False)
    process_redo(g2_engine)
    g2_engine.destroy()
except G2Exception as err:
    mock_logger("CRITICAL", err)
