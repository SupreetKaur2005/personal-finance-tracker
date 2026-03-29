# finance_sdk.TransactionsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**batch_reclassify_transactions_batch_reclassify_patch**](TransactionsApi.md#batch_reclassify_transactions_batch_reclassify_patch) | **PATCH** /transactions/batch/reclassify | Batch Reclassify
[**bulk_import_transactions_transactions_batch_import_post**](TransactionsApi.md#bulk_import_transactions_transactions_batch_import_post) | **POST** /transactions/batch/import | Bulk Import Transactions
[**create_transaction_transactions_post**](TransactionsApi.md#create_transaction_transactions_post) | **POST** /transactions | Create Transaction
[**delete_transaction_transactions_transaction_id_delete**](TransactionsApi.md#delete_transaction_transactions_transaction_id_delete) | **DELETE** /transactions/{transaction_id} | Delete Transaction
[**get_financial_insights_transactions_analytics_insights_get**](TransactionsApi.md#get_financial_insights_transactions_analytics_insights_get) | **GET** /transactions/analytics/insights | Get Financial Insights
[**get_summary_transactions_summary_get**](TransactionsApi.md#get_summary_transactions_summary_get) | **GET** /transactions/summary | Get Summary
[**list_transactions_transactions_get**](TransactionsApi.md#list_transactions_transactions_get) | **GET** /transactions | List Transactions
[**reclassify_transaction_transactions_transaction_id_reclassify_patch**](TransactionsApi.md#reclassify_transaction_transactions_transaction_id_reclassify_patch) | **PATCH** /transactions/{transaction_id}/reclassify | Reclassify Transaction
[**suggest_category_transactions_suggest_category_post**](TransactionsApi.md#suggest_category_transactions_suggest_category_post) | **POST** /transactions/suggest-category | Suggest Category
[**update_transaction_status_transactions_transaction_id_status_patch**](TransactionsApi.md#update_transaction_status_transactions_transaction_id_status_patch) | **PATCH** /transactions/{transaction_id}/status | Update Transaction Status


# **batch_reclassify_transactions_batch_reclassify_patch**
> object batch_reclassify_transactions_batch_reclassify_patch(batch_reclassify_request)

Batch Reclassify

Bulk reclassify transactions that match criteria.

### Example


```python
import finance_sdk
from finance_sdk.models.batch_reclassify_request import BatchReclassifyRequest
from finance_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = finance_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with finance_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = finance_sdk.TransactionsApi(api_client)
    batch_reclassify_request = finance_sdk.BatchReclassifyRequest() # BatchReclassifyRequest | 

    try:
        # Batch Reclassify
        api_response = api_instance.batch_reclassify_transactions_batch_reclassify_patch(batch_reclassify_request)
        print("The response of TransactionsApi->batch_reclassify_transactions_batch_reclassify_patch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->batch_reclassify_transactions_batch_reclassify_patch: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **batch_reclassify_request** | [**BatchReclassifyRequest**](BatchReclassifyRequest.md)|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **bulk_import_transactions_transactions_batch_import_post**
> object bulk_import_transactions_transactions_batch_import_post(file)

Bulk Import Transactions

Import multiple transactions from CSV.
CSV format: date, description, amount, type

### Example


```python
import finance_sdk
from finance_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = finance_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with finance_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = finance_sdk.TransactionsApi(api_client)
    file = 'file_example' # str | 

    try:
        # Bulk Import Transactions
        api_response = api_instance.bulk_import_transactions_transactions_batch_import_post(file)
        print("The response of TransactionsApi->bulk_import_transactions_transactions_batch_import_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->bulk_import_transactions_transactions_batch_import_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **str**|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_transaction_transactions_post**
> TransactionResponse create_transaction_transactions_post(transaction_create)

Create Transaction

### Example


```python
import finance_sdk
from finance_sdk.models.transaction_create import TransactionCreate
from finance_sdk.models.transaction_response import TransactionResponse
from finance_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = finance_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with finance_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = finance_sdk.TransactionsApi(api_client)
    transaction_create = finance_sdk.TransactionCreate() # TransactionCreate | 

    try:
        # Create Transaction
        api_response = api_instance.create_transaction_transactions_post(transaction_create)
        print("The response of TransactionsApi->create_transaction_transactions_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->create_transaction_transactions_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_create** | [**TransactionCreate**](TransactionCreate.md)|  | 

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_transaction_transactions_transaction_id_delete**
> delete_transaction_transactions_transaction_id_delete(transaction_id)

Delete Transaction

### Example


```python
import finance_sdk
from finance_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = finance_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with finance_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = finance_sdk.TransactionsApi(api_client)
    transaction_id = 56 # int | 

    try:
        # Delete Transaction
        api_instance.delete_transaction_transactions_transaction_id_delete(transaction_id)
    except Exception as e:
        print("Exception when calling TransactionsApi->delete_transaction_transactions_transaction_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_financial_insights_transactions_analytics_insights_get**
> Dict[str, object] get_financial_insights_transactions_analytics_insights_get()

Get Financial Insights

Get comprehensive financial insights

### Example


```python
import finance_sdk
from finance_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = finance_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with finance_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = finance_sdk.TransactionsApi(api_client)

    try:
        # Get Financial Insights
        api_response = api_instance.get_financial_insights_transactions_analytics_insights_get()
        print("The response of TransactionsApi->get_financial_insights_transactions_analytics_insights_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->get_financial_insights_transactions_analytics_insights_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**Dict[str, object]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_summary_transactions_summary_get**
> Dict[str, object] get_summary_transactions_summary_get(year=year, month=month)

Get Summary

### Example


```python
import finance_sdk
from finance_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = finance_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with finance_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = finance_sdk.TransactionsApi(api_client)
    year = 56 # int |  (optional)
    month = 56 # int |  (optional)

    try:
        # Get Summary
        api_response = api_instance.get_summary_transactions_summary_get(year=year, month=month)
        print("The response of TransactionsApi->get_summary_transactions_summary_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->get_summary_transactions_summary_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **year** | **int**|  | [optional] 
 **month** | **int**|  | [optional] 

### Return type

**Dict[str, object]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_transactions_transactions_get**
> List[TransactionResponse] list_transactions_transactions_get(skip=skip, limit=limit)

List Transactions

### Example


```python
import finance_sdk
from finance_sdk.models.transaction_response import TransactionResponse
from finance_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = finance_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with finance_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = finance_sdk.TransactionsApi(api_client)
    skip = 0 # int |  (optional) (default to 0)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # List Transactions
        api_response = api_instance.list_transactions_transactions_get(skip=skip, limit=limit)
        print("The response of TransactionsApi->list_transactions_transactions_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->list_transactions_transactions_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **skip** | **int**|  | [optional] [default to 0]
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**List[TransactionResponse]**](TransactionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reclassify_transaction_transactions_transaction_id_reclassify_patch**
> TransactionResponse reclassify_transaction_transactions_transaction_id_reclassify_patch(transaction_id, transaction_update)

Reclassify Transaction

### Example


```python
import finance_sdk
from finance_sdk.models.transaction_response import TransactionResponse
from finance_sdk.models.transaction_update import TransactionUpdate
from finance_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = finance_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with finance_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = finance_sdk.TransactionsApi(api_client)
    transaction_id = 56 # int | 
    transaction_update = finance_sdk.TransactionUpdate() # TransactionUpdate | 

    try:
        # Reclassify Transaction
        api_response = api_instance.reclassify_transaction_transactions_transaction_id_reclassify_patch(transaction_id, transaction_update)
        print("The response of TransactionsApi->reclassify_transaction_transactions_transaction_id_reclassify_patch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->reclassify_transaction_transactions_transaction_id_reclassify_patch: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_id** | **int**|  | 
 **transaction_update** | [**TransactionUpdate**](TransactionUpdate.md)|  | 

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **suggest_category_transactions_suggest_category_post**
> Dict[str, object] suggest_category_transactions_suggest_category_post(suggest_category_request)

Suggest Category

Real-time category suggestions via ML-ready categorizer

### Example


```python
import finance_sdk
from finance_sdk.models.suggest_category_request import SuggestCategoryRequest
from finance_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = finance_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with finance_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = finance_sdk.TransactionsApi(api_client)
    suggest_category_request = finance_sdk.SuggestCategoryRequest() # SuggestCategoryRequest | 

    try:
        # Suggest Category
        api_response = api_instance.suggest_category_transactions_suggest_category_post(suggest_category_request)
        print("The response of TransactionsApi->suggest_category_transactions_suggest_category_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->suggest_category_transactions_suggest_category_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **suggest_category_request** | [**SuggestCategoryRequest**](SuggestCategoryRequest.md)|  | 

### Return type

**Dict[str, object]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_transaction_status_transactions_transaction_id_status_patch**
> object update_transaction_status_transactions_transaction_id_status_patch(transaction_id, status_update_request)

Update Transaction Status

Update transaction status with state machine validation.

Valid transitions:
PENDING -> CATEGORIZED, ARCHIVED
CATEGORIZED -> VERIFIED, PENDING, ARCHIVED
VERIFIED -> RECONCILED, CATEGORIZED, ARCHIVED
RECONCILED -> ARCHIVED

### Example


```python
import finance_sdk
from finance_sdk.models.status_update_request import StatusUpdateRequest
from finance_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = finance_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with finance_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = finance_sdk.TransactionsApi(api_client)
    transaction_id = 56 # int | 
    status_update_request = finance_sdk.StatusUpdateRequest() # StatusUpdateRequest | 

    try:
        # Update Transaction Status
        api_response = api_instance.update_transaction_status_transactions_transaction_id_status_patch(transaction_id, status_update_request)
        print("The response of TransactionsApi->update_transaction_status_transactions_transaction_id_status_patch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TransactionsApi->update_transaction_status_transactions_transaction_id_status_patch: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_id** | **int**|  | 
 **status_update_request** | [**StatusUpdateRequest**](StatusUpdateRequest.md)|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

