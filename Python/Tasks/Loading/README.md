# Loading Data
The loading snippets outline adding new source records. Adding source records ingests [mapped](https://senzing.zendesk.com/hc/en-us/articles/231925448-Generic-Entity-Specification-JSON-CSV-Mapping) JSON data, completes the entity resolution process and persists outcomes in the Senzing repository. Adding a source record with the same data source code and record ID as an existing record will replace it.  

## Snippets
* **AddxKFutures.py**
    * Read and load source records from a file using multiple threads
    * x is the number of source records in the file, see [Input Load File Sizes.](../../../README.md#input-load-file-sizes)
* **Add5KLoop.py**
    * Basic read and load source records from a file
* **Add10KQueue.py**
    * Read and load source records using a queue
* **Add50KWithInfoFutures.py**
    * Read and load source records from a file using multiple threads
    * Collect the response from the [with info](../../../README.md#with-info) version of the API and write it to a file
* **AddRecords.py**
    * Basic iteration over a few records, adding each one
* **AddTruthsetLoop.py** 
    * Read and load from multiple source files, adding a sample truth set

## API Calls
* [addRecord](../../../Python/APIs/G2Engine/Data_Manipulation/addRecord.py)
  * Adds a single record
* [addRecordWithInfo](../../../Python/APIs/G2Engine/Data_Manipulation/addRecordWithInfo.py)
  * Adds a single record and returns information outlining any entities affected by the addition of the record. For further information see [With Info](../../../README.md#with-info)
