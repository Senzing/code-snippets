#! /usr/bin/env python3

import concurrent.futures
import itertools
import json
import os
import sys
import time
from collections import Counter
from senzing import G2BadInputException, G2Engine, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = os.getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)


def mock_logger(level, exception, error_rec=None):
    print(f'\n{level}: {exception}', file=sys.stderr)
    if error_rec:
        print(f'{error_rec}', file=sys.stderr)


def search_record(engine, rec_to_search):
    search_response = bytearray()
    engine.searchByAttributes(rec_to_search, search_response)
    return search_response


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
    print(f'Processed {success_recs} searches, {int(1000 / (time.time() - prev_time))} records per second')
    return time.time()


def search_results(result, record, out_file):
    response_dict = json.loads(result.decode())
    response_entities = response_dict.get('RESOLVED_ENTITIES', None)

    if response_entities:
        results_str = []
        results_count = Counter(k for entity in response_entities for k in entity.keys() if k.startswith('MATCH_INFO'))
        results_str.append(f'\n{results_count["MATCH_INFO"]} results for {record}')

        for idx, entity in enumerate(response_entities, start=1):
            results_str.append(f'\n  Result {idx}')
            results_str.append(f'\n    Entity ID:       {entity["ENTITY"]["RESOLVED_ENTITY"]["ENTITY_ID"]}')
            results_str.append(f'\n    Entity name:     {entity["ENTITY"]["RESOLVED_ENTITY"]["ENTITY_NAME"]}')
            results_str.append(f'\n    Match key:       {entity["MATCH_INFO"]["MATCH_KEY"]}')
            results_str.append('\n    Records summary: ')
            for record_summary in entity["ENTITY"]["RESOLVED_ENTITY"]["RECORD_SUMMARY"]:
                results_str.append(f'{record_summary["DATA_SOURCE"]}: {record_summary["RECORD_COUNT"]}' + '    ')
            results_str.append('\n')

        out_file.write(''.join(results_str))
    else:
        out_file.write(f'\nNo result for {record}\n')


def futures_search(engine, input_file, output_file):
    prev_time = time.time()
    success_recs = error_recs = 0

    with open(output_file, 'w') as out_file:
        with open(input_file, 'r') as in_file:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(search_record, engine, record): record for record in itertools.islice(in_file, executor._max_workers)}

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
                        except json.JSONDecodeError as ex:
                            mock_logger('ERROR', ex, futures[f])
                            error_recs += 1
                        else:
                            success_recs += 1

                            if success_recs % 1000 == 0:
                                prev_time = record_stats(success_recs, prev_time)

                            if success_recs % 10000 == 0:
                                engine_stats(engine)

                            search_results(result, futures[f], out_file)
                        finally:
                            futures.pop(f)

                        record = in_file.readline()
                        if record:
                            futures[executor.submit(search_record, engine, record)] = record

                print(f'\nSuccessfully searched {success_recs} records, with {error_recs} errors')
                print(f'Search results are located in: {output_file}')


try:
    g2_engine = G2Engine()
    g2_engine.init('G2Engine', engine_config_json, False)
    futures_search(
        g2_engine,
        '../../../Resources/Data/search-5K.json',
        '../../../Resources/Output/search_file.out')
    g2_engine.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception) as ex:
    print(ex)
    sys.exit(-1)
