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


def process_redo(engine, output_file):
    success_recs = error_recs = 0
    redo_record = with_info = bytearray()

    with open(output_file, "w") as out_file:
        try:
            while True:
                redo_record = bytearray()
                with_info = bytearray()
                engine.getRedoRecord(redo_record)

                if not redo_record:
                    print(
                        "No redo records to process, pausing for 30 seconds. Total"
                        f" processed {success_recs:,} . (CTRL-C to exit)..."
                    )
                    time.sleep(30)
                    continue

                engine.processWithInfo(redo_record, with_info)

                success_recs += 1
                out_file.write(f"{with_info.decode()}\n")

                if success_recs % 100 == 0:
                    print(
                        f"Processed {success_recs:,} redo records, with"
                        f" {error_recs:,} errors"
                    )
        except G2BadInputException as ex:
            mock_logger("ERROR", ex, redo_record)
            error_recs += 1
        except G2RetryableException as ex:
            mock_logger("WARN", ex, redo_record)
            error_recs += 1
        except (G2UnrecoverableException, G2Exception) as ex:
            mock_logger("CRITICAL", ex, redo_record)
            raise


try:
    g2_engine = G2Engine()
    g2_engine.init("G2Engine", engine_config_json, False)
    process_redo(g2_engine, "../../../Resources/Output/Redo_WithInfo_Continuous.json")
    g2_engine.destroy()
except G2Exception as err:
    mock_logger("CRITICAL", err)
