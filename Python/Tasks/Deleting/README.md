# Deleting Data
The deletion snippets outline deleting previously added source records. Deleting source records removes the previously added source record from the system, completes the entity resolution process and persists outcomes in the Senzing repository. 

Deleting a record only requires the data source code and record ID for the record to be deleted.

## Snippets
* **DeleteFutures.py**
    * Read and delete source records from a file using multiple threads
* **DeleteLoop.py**
    * Basic read and delete source records from a file
* **DeleteWithInfoFutures.py**
    * Read and delete source records from a file using multiple threads
    * Collect the response from the [with info](../../../README.md#with-info) version of the API and write it to a file

## API Calls
* [deleteRecord](https://github.com/antaenc/senzing-code-snippets/blob/f2556a2152a4524780f63c1e66a868f53419dd60/Python/APIs/G2Engine/Data_Manipulation/deleteRecord.py)
  * Deletes a single record
* [deleteRecordWithInfo](https://github.com/antaenc/senzing-code-snippets/blob/f2556a2152a4524780f63c1e66a868f53419dd60/Python/APIs/G2Engine/Data_Manipulation/deleteRecordWithInfo.py)
  * Deletes a single record and returns information outlining any entities affected by the deletion of the record. For further information see [with info](../../../README.md#with-info)
