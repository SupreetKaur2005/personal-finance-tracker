# TransactionUpdate

Schema for updating a transaction

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**category** | **str** |  | 

## Example

```python
from finance_sdk.models.transaction_update import TransactionUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionUpdate from a JSON string
transaction_update_instance = TransactionUpdate.from_json(json)
# print the JSON string representation of the object
print(TransactionUpdate.to_json())

# convert the object into a dict
transaction_update_dict = transaction_update_instance.to_dict()
# create an instance of TransactionUpdate from a dict
transaction_update_from_dict = TransactionUpdate.from_dict(transaction_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


