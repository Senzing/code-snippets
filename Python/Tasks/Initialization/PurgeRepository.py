#! /usr/bin/env python3

import os
import sys
from senzing import (
    G2Engine,
    G2Exception,
)

engine_config_json = os.getenv("SENZING_ENGINE_CONFIGURATION_JSON", None)

purge_msg = """
********** WARNING **********
This example will purge all currently loaded data from the senzing database!
Before proceeding, all instances of senzing (custom code, rest api, redoer, etc.) must be shut down.
********** WARNING **********

Are you sure you want to continue and purge the senzing database? (y/n) """

if input(purge_msg) not in ["y", "Y", "yes", "YES"]:
    sys.exit()

try:
    g2_engine = G2Engine()
    g2_engine.init("G2Engine", engine_config_json, False)
    g2_engine.purgeRepository()
    print("Senzing repository purged")
    g2_engine.destroy()
except G2Exception as err:
    print(err)
