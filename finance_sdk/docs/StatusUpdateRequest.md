# StatusUpdateRequest

Schema for updating transaction status

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**new_status** | **str** |  | 
**user_id** | **str** |  | [optional] [default to 'system']

## Example

```python
from finance_sdk.models.status_update_request import StatusUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of StatusUpdateRequest from a JSON string
status_update_request_instance = StatusUpdateRequest.from_json(json)
# print the JSON string representation of the object
print(StatusUpdateRequest.to_json())

# convert the object into a dict
status_update_request_dict = status_update_request_instance.to_dict()
# create an instance of StatusUpdateRequest from a dict
status_update_request_from_dict = StatusUpdateRequest.from_dict(status_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


