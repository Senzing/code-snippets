#! /usr/bin/env python3

import concurrent.futures
import json
import os
import sys
import time
from multiprocessing import Process, Queue
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


def add_record(engine, rec_to_add):
    record_dict = json.loads(rec_to_add)
    data_source = record_dict.get("DATA_SOURCE", None)
    record_id = record_dict.get("RECORD_ID", None)
    engine.addRecord(data_source, record_id, rec_to_add)


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
        f"Processed {success:,} adds,"
        f" {int(1000 / (time.time() - prev_time)):,} records per second,"
        f" {error} errors"
    )
    return time.time()


def producer(input_file, queue):
    with open(input_file, "r") as file:
        for record in file:
            queue.put(record, block=True)

    print(f"All records read from {input_file}")


def consumer(engine, queue):
    prev_time = time.time()
    success_recs = error_recs = 0

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(add_record, engine, queue.get()): _
            for _ in range(executor._max_workers)
        }

        while futures:
            done, _ = concurrent.futures.wait(
                futures, return_when=concurrent.futures.FIRST_COMPLETED
            )
            for f in done:
                try:
                    f.result()
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
                    if not queue.empty():
                        record = queue.get()
                        futures[executor.submit(add_record, engine, record)] = record

                    success_recs += 1
                    if success_recs % 1000 == 0:
                        prev_time = record_stats(success_recs, error_recs, prev_time)

                    if success_recs % 10000 == 0:
                        engine_stats(engine)
                finally:
                    del futures[f]

        print(
            f"Successfully loaded {success_recs:,} records, with {error_recs:,} errors"
        )


load_file = "../../../Resources/Data/load-10K.json"

try:
    g2_engine = G2Engine()
    g2_engine.init("G2Engine", engine_config_json, False)

    input_queue = Queue(maxsize=200)
    producer_proc = Process(
        target=producer,
        args=(
            load_file,
            input_queue,
        ),
    )
    producer_proc.start()
    consumer_proc = Process(
        target=consumer,
        args=(
            g2_engine,
            input_queue,
        ),
    )
    consumer_proc.start()
    producer_proc.join()
    consumer_proc.join()

    g2_engine.destroy()
except G2Exception as err:
    mock_logger("CRITICAL", err)
