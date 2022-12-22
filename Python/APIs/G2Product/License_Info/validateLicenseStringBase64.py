#! /usr/bin/env python3

import os
import sys
from senzing import G2Product, G2BadInputException, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = os.getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)

with open('../../../../Resources/License/g2lic_Valid_base64.txt', 'r') as file:
    valid_license_string = file.read().strip()

INVALID_LICENSE_STRING = 'this_isnt_valid_for_a_license_string!'

try:
    g2_product = G2Product()
    g2_product.init('G2Product', engine_config_json, False)

    return_code_invalid = g2_product.validateLicenseStringBase64(INVALID_LICENSE_STRING)
    return_code_valid = g2_product.validateLicenseStringBase64(valid_license_string)

    print(f'License string is {"valid" if return_code_invalid == 0 else "not valid"}')
    print(f'\nLicense string is {"valid" if return_code_valid == 0 else "not valid"}')

    g2_product.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception) as ex:
    print(ex)
    sys.exit(-1)
