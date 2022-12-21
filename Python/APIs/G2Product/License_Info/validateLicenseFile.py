#! /usr/bin/env python3

from os import getenv
from sys import exit
from senzing import G2Product, G2BadInputException, G2Exception, G2RetryableException, G2UnrecoverableException

engine_config_json = getenv('SENZING_ENGINE_CONFIGURATION_JSON', None)
valid_license_file = '../../../../Resources/License/g2.lic_Valid_File'
invalid_license_file = '../../../../Resources/License/g2.lic_Invalid_File'

try:
    g2_product = G2Product()
    g2_product.init('G2Product', engine_config_json, False)

    return_code_valid = g2_product.validateLicenseFile(valid_license_file)
    return_code_invalid = g2_product.validateLicenseFile(invalid_license_file)

    print(f'License file {valid_license_file} is {"valid" if return_code_valid == 0 else "not valid"}')
    print(f'\nLicense file {invalid_license_file} is {"valid" if return_code_invalid == 0 else "not valid"}')

    g2_product.destroy()
except (G2BadInputException, G2RetryableException, G2UnrecoverableException, G2Exception) as ex:
    print(ex)
    exit(-1)
