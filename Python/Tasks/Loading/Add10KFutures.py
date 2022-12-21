#! /usr/bin/env python3

import concurrent.futures
import itertools
import json
import os
import sys
import time
from senzing import G2BadInputException, G2Engine, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = os.getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)


def mock_logger(level, exception, error_rec=None):
    print(f'\n{level}: {exception}', file=sys.stderr)
    if error_rec:
        print(f'{error_rec}', file=sys.stderr)


def add_record(engine, rec_to_add):
    record_dict = json.loads(rec_to_add)
    data_source = record_dict.get('DATA_SOURCE', None)
    record_id = record_dict.get('RECORD_ID', None)
    engine.addRecord(data_source, record_id, rec_to_add)


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


def record_stats(success_recs, prev_time):
    print(f'Processed {success_recs} adds, {int(1000 / (time.time() - prev_time))} records per second')
    return time.time()


def futures_add(engine, input_file):
    prev_time = time.time()
    success_recs = error_recs = 0

    with open(input_file, 'r') as file:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(add_record, engine, record): record for record in itertools.islice(file, executor._max_workers)}

            while futures:
                for f in concurrent.futures.as_completed(futures.keys()):
                    try:
                        f.result()
                    except G2BadInputException as ex:
                        mock_logger('ERROR', ex, futures[f])
                        error_recs += 1
                    except G2RetryableException as ex:
                        mock_logger('WARN', ex, futures[f])
                        error_recs += 1
                    except (G2UnrecoverableException, G2Exception) as ex:
                        mock_logger('CRITICAL', ex, futures[f])
                        raise
                    except json.JSONDecodeError as ex:
                        mock_logger('ERROR', ex, futures[f])
                        error_recs += 1
                    else:
                        success_recs += 1

                        if success_recs % 1000 == 0:
                            prev_time = record_stats(success_recs, prev_time)

                        if success_recs % 10000 == 0:
                            engine_stats(engine)
                    finally:
                        futures.pop(f)

                    record = file.readline()
                    if record:
                        futures[executor.submit(add_record, engine, record)] = record

            print(f'Successfully loaded {success_recs} records, with {error_recs} errors')


try:
    g2_engine = G2Engine()
    g2_engine.init('G2Engine', engine_config_json, False)
    futures_add(g2_engine, '../../../Resources/Data/load-10K.json')

    g2_engine.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception) as ex:
    print(ex)
    sys.exit(-1)
