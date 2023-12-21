#! /usr/bin/env python3

import concurrent.futures
import itertools
import json
import os
import sys
import time
from collections import Counter
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


def search_record(engine, rec_to_search):
    search_response = bytearray()
    engine.searchByAttributes(rec_to_search, search_response)
    return search_response


def engine_stats(engine):
    response = bytearray()
    try:
        engine.stats(response)
        print(f"\n{response.decode()}\n")
    except G2RetryableException as err:
        mock_logger("WARN", err)
    except G2Exception as err:
        mock_logger("CRITICAL", err)
        raise


def record_stats(success, error, prev_time):
    print(
        f"Processed {success:,} searches,"
        f" {int(1000 / (time.time() - prev_time)):,} records per second,"
        f" {error} errors"
    )
    return time.time()


def search_results(result, record, out_file):
    response_dict = json.loads(result.decode())
    response_entities = response_dict.get("RESOLVED_ENTITIES", None)

    if response_entities:
        results_str = []
        results_count = Counter(
            k
            for entity in response_entities
            for k in entity.keys()
            if k.startswith("MATCH_INFO")
        )
        results_str.append(f'\n{results_count["MATCH_INFO"]} results for {record}')

        for idx, entity in enumerate(response_entities, start=1):
            results_str.append(f"\n  Result {idx}")
            results_str.append(
                "\n    Entity ID:      "
                f" {entity['ENTITY']['RESOLVED_ENTITY']['ENTITY_ID']}"
            )
            results_str.append(
                "\n    Entity name:    "
                f" {entity['ENTITY']['RESOLVED_ENTITY']['ENTITY_NAME']}"
            )
            results_str.append(
                f'\n    Match key:       {entity["MATCH_INFO"]["MATCH_KEY"]}'
            )
            results_str.append("\n    Records summary: ")
            for record_summary in entity["ENTITY"]["RESOLVED_ENTITY"]["RECORD_SUMMARY"]:
                results_str.append(
                    f'{record_summary["DATA_SOURCE"]}: {record_summary["RECORD_COUNT"]}'
                    + "    "
                )
            results_str.append("\n")

        out_file.write("".join(results_str))
    else:
        out_file.write(f"\nNo result for {record}\n")


def futures_search(engine, input_file, output_file):
    prev_time = time.time()
    success_recs = error_recs = 0

    with open(output_file, "w") as out_file:
        with open(input_file, "r") as in_file:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(search_record, engine, record): record
                    for record in itertools.islice(in_file, executor._max_workers)
                }

                while futures:
                    done, _ = concurrent.futures.wait(
                        futures, return_when=concurrent.futures.FIRST_COMPLETED
                    )
                    for f in done:
                        try:
                            result = f.result()
                        except (G2BadInputException, json.JSONDecodeError) as err:
                            mock_logger("ERROR", err, futures[f])
                            error_recs += 1
                        except G2RetryableException as err:
                            mock_logger("WARN", err, futures[f])
                            error_recs += 1
                        except (G2UnrecoverableException, G2Exception) as err:
                            mock_logger("CRITICAL", err, futures[f])
                            raise
                        else:
                            record = in_file.readline()
                            if record:
                                futures[
                                    executor.submit(search_record, engine, record)
                                ] = record

                            success_recs += 1
                            if success_recs % 1000 == 0:
                                prev_time = record_stats(
                                    success_recs, error_recs, prev_time
                                )

                            if success_recs % 10000 == 0:
                                engine_stats(engine)

                            search_results(result, futures[f], out_file)
                        finally:
                            del futures[f]

                print(
                    f"\nSuccessfully searched {success_recs:,} records, with"
                    f" {error_recs:,} errors"
                )
                print(f"Search results are located in: {output_file}")


try:
    g2_engine = G2Engine()
    g2_engine.init("G2Engine", engine_config_json, False)
    futures_search(
        g2_engine,
        "../../../Resources/Data/search-5K.json",
        "../../../Resources/Output/search_file.out",
    )
    g2_engine.destroy()
except G2Exception as err:
    mock_logger("CRITICAL", err)
