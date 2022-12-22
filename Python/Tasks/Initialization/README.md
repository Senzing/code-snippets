# Initialization

## Snippets
* G2ModuleIniToJson.py
    * The snippets herein utilize the `SENZING_ENGINE_CONFIGURATION_JSON` environment variable for Senzing engine object initialization
    * If you are familiar with working with a Senzing project you will be aware the same configuration data is held in the G2Module.ini file
    * Example to check for `SENZING_ENGINE_CONFIGURATION_JSON` and if not present convert a G2Module.ini file to JSON to use on engine object initialization calls
