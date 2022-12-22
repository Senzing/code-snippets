# Replacing Data
The replacement snippets outline replacing (updating) previously loaded source records. Replacing source records replaces the [mapped](https://senzing.zendesk.com/hc/en-us/articles/231925448-Generic-Entity-Specification-JSON-CSV-Mapping) JSON data, completes the entity resolution process and persists outcomes in the Senzing repository. 

To replace an existing loaded record use the same data source code and record ID and modify the JSON data for the record to reflect the changes. If a record with the data source code and record ID does not currently exist it will be added. 

## Snippets
* **Replace5kFutures.py**
    * Read and replace source records from a file using multiple threads
* **Replace5KWithInfoFutures.py**
    * Read and replace source records from a file using multiple threads
    * Collect the response from the with info version of the API and write it to a file 
* **ReplaceRecords.py** 
    * Basic iteration over a few records, replacing each one

## API Calls
* [replaceRecord](../../../Python/APIs/G2Engine/Data_Manipulation/replaceRecord.py)
  * Replaces a single record
* [replaceRecordWithInfo](../../../Python/APIs/G2Engine/Data_Manipulation/replaceRecordWithInfo.py)
  * Replaces a single record and returns information outlining any entities affected by the replacement of the record. For further information see [With Info](../../../README.md#with-info)
