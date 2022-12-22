#! /usr/bin/env python3

import os
import sys
from senzing import G2BadInputException, G2Engine, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = os.getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)
fetch_next_response = bytearray()
CSV_HEADERS= 'RESOLVED_ENTITY_ID,RESOLVED_ENTITY_NAME,RELATED_ENTITY_ID,MATCH_LEVEL,MATCH_KEY,IS_DISCLOSED,IS_AMBIGUOUS,DATA_SOURCE,RECORD_ID,JSON_DATA,LAST_SEEN_DT,NAME_DATA,ATTRIBUTE_DATA,IDENTIFIER_DATA,ADDRESS_DATA,PHONE_DATA,RELATIONSHIP_DATA,ENTITY_DATA,OTHER_DATA'


def fetch_next(handle, response):
    """ Fetch the next export record from the handle"""

    try:
        g2_engine.fetchNext(handle, response)
    except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception) as ex:
        print(ex)
        sys.exit(-1)

    return response.decode()


try:
    g2_engine = G2Engine()
    g2_engine.init('G2Engine', engine_config_json, False)

    export_handle = g2_engine.exportCSVEntityReport(CSV_HEADERS)

    with open('../../../../Resources/Output/exportCSVEntityReport.json', 'w') as export_out:

        export_record = fetch_next(export_handle, fetch_next_response)

        while export_record:
            try:
                export_out.write(export_record)
            except IOError as ex:
                print(ex)
                sys.exit(-1)

            export_record = fetch_next(export_handle, fetch_next_response)

    g2_engine.closeExport(export_handle)
    g2_engine.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception) as ex:
    print(ex)
    sys.exit(-1)

print('CSV export report complete')
