#! /usr/bin/env python3

import concurrent.futures
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
    redo_record = bytearray()
    engine.processRedoRecord(redo_record)
    return redo_record


def engine_stats(engine):
    response = bytearray()
    try:
        engine.stats(response)
        print(f'\n{response.decode()}\n')
    except G2RetryableException as ex:
        mock_logger('WARN', ex)
    except (G2UnrecoverableException, G2Exception) as ex:
        mock_logger('CRITICAL', ex)
        raise


def redo_count(engine):
    redo_recs = None
    try:
        redo_recs = engine.countRedoRecords()
    except G2RetryableException as ex:
        mock_logger('WARN', ex)
    except (G2UnrecoverableException, G2Exception) as ex:
        mock_logger('CRITICAL', ex)
        raise

    return redo_recs


def redo_pause(success_recs):
    print(f'No redo records to process, pausing for 30 seconds. Total processed: {success_recs} (CTRL-C to exit)...')
    time.sleep(30)


def futures_redo(engine):
    success_recs = error_recs = 0
    redo_paused = False

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_redo, engine): _ for _ in range(executor._max_workers)}

        while futures:
            for f in concurrent.futures.as_completed(futures.keys()):
                try:
                    result = f.result()
                except G2BadInputException as ex:
                    mock_logger('ERROR', ex, futures[f])
                    error_recs += 1
                except G2RetryableException as ex:
                    mock_logger('WARN', ex, futures[f])
                    error_recs += 1
                except (G2UnrecoverableException, G2Exception) as ex:
                    mock_logger('CRITICAL', ex, futures[f])
                    raise
                else:
                    if result:
                        success_recs += 1

                        if success_recs % 100 == 0:
                            print(f'Processed {success_recs} redo records')

                        if success_recs % 2000 == 0:
                            engine_stats(engine)
                    else:
                        redo_paused = True if not redo_paused else redo_paused
                finally:
                    futures.pop(f)

                if redo_paused:
                    while not redo_count(engine):
                        redo_pause(success_recs)
                    redo_paused = False

                futures[executor.submit(process_redo, engine)] = None


try:
    g2_engine = G2Engine()
    g2_engine.init('G2Engine', engine_config_json, False)
    futures_redo(g2_engine)
    g2_engine.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception) as ex:
    print(ex)
    sys.exit(-1)
