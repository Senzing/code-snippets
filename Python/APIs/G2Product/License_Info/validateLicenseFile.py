#! /usr/bin/env python3

import os
import sys
from senzing import G2Product, G2BadInputException, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = os.getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)
VALID_LICENSE_FILE = '../../../../Resources/License/g2.lic_Valid_File'
INVALID_LICENSE_FILE = '../../../../Resources/License/g2.lic_Invalid_File'

try:
    g2_product = G2Product()
    g2_product.init('G2Product', engine_config_json, False)

    return_code_valid = g2_product.validateLicenseFile(VALID_LICENSE_FILE)
    return_code_invalid = g2_product.validateLicenseFile(INVALID_LICENSE_FILE)

    print(f'License file {VALID_LICENSE_FILE} is {"valid" if return_code_valid == 0 else "not valid"}')
    print(f'\nLicense file {INVALID_LICENSE_FILE} is {"valid" if return_code_invalid == 0 else "not valid"}')

    g2_product.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception) as ex:
    print(ex)
    sys.exit(-1)
