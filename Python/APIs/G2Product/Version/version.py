#! /usr/bin/env python3

from os import getenv
from senzing import G2Product, G2BadInputException, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)

try:
    g2_product = G2Product()
    g2_product.init('G2Product', engine_config_json, False)

    g2_product.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception):
    raise

print(g2_product.version())
