# Stewardship
The stewardship snippets outline forced resolution and un-resolution of records from entities. Stewardship provides the ability to force records to resolve or un-resolve when, for example, Senzing doesn't have enough information at a point in time, but you may have knowledge outside of Senzing to override a decision Senzing has made. Basic stewardship utilizes the `TRUSTED_ID` feature to influence entity resolution. See the [Entity Specification](https://senzing.zendesk.com/hc/en-us/articles/231925448-Generic-Entity-Specification-JSON-CSV-Mapping) for additional details. 

In these examples, the current JSON data for a record is first retrieved and additional `TRUSTED_ID` attributes are appended before replacing the records and completing entity resolution, now taking into account the influence of the `TRUSTED_ID` attributes: 

* TRUSTED_ID_NUMBER - when the values across records is the same the records resolve to the same entity. If the values used across records differ, the records will not resolve to the same entity.
* TRUSTED_ID_TYPE - an arbitrary value to indicate the use of the TRUSTED_ID_NUMBER.

## Snippets
* **ForceResolve.py**
    * Force resolve records together to a single entity
* **ForceUnResolve.py**
    * Force un-resolve a record from an entity into a new entity


## Example Usage
### Force Resolve
Force resolve first adds 3 records and details 1 of the resulting entities has 2 [ambiguous](https://senzing.zendesk.com/hc/en-us/articles/360016288734-What-Is-An-Ambiguous-Entity-) relationships to the other 2 entities created. The 2 ambiguous relationships occur because entity 3 could resolve with either entity 1 or 2. Entity 3 doesn't have a date of birth whereas entity 1 and 2 have different dates of birth. At this point Senzing doesn't know if entity 3 should resolve to entity 1 or 2; it can't resolve to both. 

With additional knowledge not represented in Senzing you know record 3 "Pat Smith" represents the same person as record 1 "Patrick Smith". To force resolve these 2 records to the same entity, first fetch the current representation of each record with getRecord. Next add `TRUSTED_ID_NUMBER` and `TRUSTED_ID_TYPE` attributes to each of the retrieved records. `TRUSTED_ID_NUMBER` uses the same value to indicate these records should always be considered the same entity and resolve together. In this example the data source of the records and their record IDs are used to create `TRUSTED_ID_NUMBER`. `TRUSTED_ID_TYPE` is set as FORCE_RESOLVE as an indicator they were forced together.   
### Force UnResolve
Force UnResolve first adds 3 records and details all records resolved to the same entity. 

With additional knowledge not represented in Senzing you know record 6 "Betsey Jones" is not the same as records 4 and 5; Betsey is a twin to "Elizabeth Jones". To force unresolve Betsey from the Elizabeth entity, first fetch the current representation of each record with getRecord. Next add `TRUSTED_ID_NUMBER` and `TRUSTED_ID_TYPE` attributes to each of the retrieved records. `TRUSTED_ID_NUMBER` uses a different value to indicate these records should always be considered different entities and not resolve together. In this example the data source of the records and their record IDs are used to create `TRUSTED_ID_NUMBER`. `TRUSTED_ID_TYPE` is set as FORCE_UNRESOLVE as an indicator they were forced apart.   
