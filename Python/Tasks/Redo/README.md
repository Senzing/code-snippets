# Redo Records
The redo snippets outline processing redo records. During normal processing of loading, deleting and replacing data the Senzing engine may determine additional work needs to be completed for an entity. There are times the Senzing engine will decide to defer this additional work. Examples of why this may happen include:
* Records loaded in parallel are clustering around the same entities causing contention
* Automatic corrections 
* Cleansing decisions made on attributes determined to no longer be useful for entity resolution

When an entity requires additional work a record is automatically created in the system indicating this requirement. These records are called redo records. Redo records need to be periodically or continuously checked for and processed. Periodically is suitable after manipulating smaller portions of data, for example, at the end of a batch load of data. In contrast, a continuous process checking for and processing redo records is suitable in a streaming system that is constantly manipulating data. In general, it is recommended to have a continuous redo process checking for any redo records to process and processing them.

## Snippets
* **Add10KWithRedo.py**
    * Read and load source records from a file and then process any redo records 
* **RedoContinuous.py**
    * Basic example of continously monitoring for redo records to process
* **RedoContinuousFutures.py**
    * Continously monitor for redo records to process using concurrent futures and multiple threads
* **RedoWithInfoContinuous.py**
    * Continously monitor for redo records to process
    * Collect the response from the [with info](../../../README.md#with-info) version of the API and write it to a file

## API Calls
* [processRedoRecord](../../../Python/APIs/G2Engine/Redo/processRedoRecord.py)
  * Retrieve and process a single redo record.
* [processRedoRecordWithInfo](../../../Python/APIs/G2Engine/Redo/processRedoRecordWithInfo.py)
    * Process a single redo record and returns information outlining any entities affected by the processing of the record. For further information see [With Info](../../../README.md#with-info)
