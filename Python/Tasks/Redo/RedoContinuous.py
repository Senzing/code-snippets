#! /usr/bin/env python3

import os
import sys
import time
from senzing import G2BadInputException, G2Engine, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = os.getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)


def mock_logger(level, exception, error_rec=None):
    print(f'\n{level}: {exception}', file=sys.stderr)
    if error_rec:
        print(f'{error_rec}', file=sys.stderr)


def process_redo(engine):
    success_recs = 0

    try:
        while True:
            redo_record = bytearray()
            engine.processRedoRecord(redo_record)

            if not redo_record:
                print(f'No redo records to process, pausing for 30 seconds. Total processed {success_recs} . (CTRL-C to exit)...')
                time.sleep(30)
                continue

            success_recs += 1

            if success_recs % 100 == 0:
                print(f'Processed {success_recs} redo records')
    except G2BadInputException as ex:
        mock_logger('ERROR', ex)
    except G2RetryableException as ex:
        mock_logger('WARN', ex)
    except (G2UnrecoverableException, G2Exception) as ex:
        mock_logger('CRITICAL', ex)
        raise


try:
    g2_engine = G2Engine()
    g2_engine.init('G2Engine', engine_config_json, False)
    process_redo(g2_engine)
    g2_engine.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception) as ex:
    print(ex)
    sys.exit(-1)
