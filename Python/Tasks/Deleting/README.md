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

