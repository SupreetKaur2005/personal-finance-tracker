# SuggestCategoryRequest

Schema for returning category recommendations

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** |  | 

## Example

```python
from finance_sdk.models.suggest_category_request import SuggestCategoryRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SuggestCategoryRequest from a JSON string
suggest_category_request_instance = SuggestCategoryRequest.from_json(json)
# print the JSON string representation of the object
print(SuggestCategoryRequest.to_json())

# convert the object into a dict
suggest_category_request_dict = suggest_category_request_instance.to_dict()
# create an instance of SuggestCategoryRequest from a dict
suggest_category_request_from_dict = SuggestCategoryRequest.from_dict(suggest_category_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


