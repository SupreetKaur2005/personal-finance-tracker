# BatchReclassifyRequest

Schema for batch reclassification

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**filter** | **Dict[str, str]** |  | 
**new_category** | **str** |  | 

## Example

```python
from finance_sdk.models.batch_reclassify_request import BatchReclassifyRequest

# TODO update the JSON string below
json = "{}"
# create an instance of BatchReclassifyRequest from a JSON string
batch_reclassify_request_instance = BatchReclassifyRequest.from_json(json)
# print the JSON string representation of the object
print(BatchReclassifyRequest.to_json())

# convert the object into a dict
batch_reclassify_request_dict = batch_reclassify_request_instance.to_dict()
# create an instance of BatchReclassifyRequest from a dict
batch_reclassify_request_from_dict = BatchReclassifyRequest.from_dict(batch_reclassify_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


