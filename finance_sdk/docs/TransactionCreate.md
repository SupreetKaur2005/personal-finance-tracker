# TransactionCreate

Schema for creating a transaction

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** |  | 
**amount** | **float** |  | 
**transaction_type** | **str** |  | 
**category** | **str** |  | [optional] 
**timestamp** | **datetime** |  | [optional] 

## Example

```python
from finance_sdk.models.transaction_create import TransactionCreate

# TODO update the JSON string below
json = "{}"
# create an instance of TransactionCreate from a JSON string
transaction_create_instance = TransactionCreate.from_json(json)
# print the JSON string representation of the object
print(TransactionCreate.to_json())

# convert the object into a dict
transaction_create_dict = transaction_create_instance.to_dict()
# create an instance of TransactionCreate from a dict
transaction_create_from_dict = TransactionCreate.from_dict(transaction_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


