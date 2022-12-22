#! /usr/bin/env python3

import os
import sys
from senzing import G2Product, G2BadInputException, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = os.getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)

try:
    g2_product = G2Product()
    g2_product.init('G2Product', engine_config_json, False)

    g2_product.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception) as ex:
    print(ex)
    sys.exit(-1)

print(g2_product.version())
