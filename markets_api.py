import json
import requests
from requests.auth import HTTPBasicAuth



def lists_limit_api(url, email, password, limit):
    ''' 
        Call /markets endpoint with a limit parameter, 
        Verify response code is 200 and number of records on the response is according to the parameter 
    '''
    markets_resp = requests.get(f'{url}/markets', auth=HTTPBasicAuth(email, password), params={'limit':limit})
    assert markets_resp.status_code == 200, f'{url}/markets endpoint response status code is not 200, it is {markets_resp.status_code}'
    response_json = markets_resp.json()
    number_of_response_records = len(response_json['result'])
    #Assert on the number of markets returned by markets API
    assert int(number_of_response_records) == int(limit), f'Number of records stated on limit parameter {limit} is different from actual records returned by the API {number_of_response_records}'



def details_exchange_api(url, email, password, exchange_to_retrieve):
    '''
    Call /markets/:exchange endpoint with a specific excgange parameter, 
    Verify response code is 200 and response exchange value is according to the exchange parameter
    '''
    markets_resp = requests.get(f'{url}/markets/{exchange_to_retrieve}', auth=HTTPBasicAuth(email, password))
    assert markets_resp.status_code == 200, f'{url}/markets/{exchange_to_retrieve} response status code is not 200, it is {markets_resp.status_code}'
    response_json = markets_resp.json()
    for i in response_json['result']:
        record_id = i.get('id')
        assert exchange_to_retrieve in i.get('exchange'), f'Record {record_id} exchange is not {exchange_to_retrieve} value' 


def details_pair_api(url, email, password, exchange_to_retrieve, pair_to_retrieve):
    '''
    Call /markets/:exchange/:pair endpoint with a specific excgange and pair parameters, 
    Verify response code is 200 and response exchange pair value is according to the pair parameter
    '''
    markets_resp = requests.get(f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}', auth=HTTPBasicAuth(email, password))
    assert markets_resp.status_code == 200, f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve} endpoint response status code is not 200, it is {markets_resp.status_code}'
    response_json = markets_resp.json()
    record_id = response_json['result']['id']
    pair_value = response_json['result']['pair']
    assert pair_value == pair_to_retrieve, f'Record {record_id} pair is not {pair_to_retrieve} value'

    
def price_api(url, email, password, exchange_to_retrieve, pair_to_retrieve):
    '''
    Call /markets/:exchange/:pair/price endpoint with a specific excgange and pair parameters, 
    Verify response code is 200 and response price value is integer or float
    '''
    markets_resp = requests.get(f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/price', auth=HTTPBasicAuth(email, password))
    assert markets_resp.status_code == 200, f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/price endpoint response status code is not 200, it is {markets_resp.status_code}'
    response_json = markets_resp.json()
    price = response_json['result']['price']
    assert type(price) is int or type(price) is float, f'Record price value of {price} is not numeric'
    return price

def prices_api(url, email, password):
    '''
    Call /markets/prices endpoint, 
    Verify response code is 200 and response price values is integer or float for all the records
    '''
    markets_resp = requests.get(f'{url}/markets/prices', auth=HTTPBasicAuth(email, password))
    assert markets_resp.status_code == 200, f'{url}/markets/prices endpoint response status code is not 200, it is {markets_resp.status_code}'
    response_json = markets_resp.json()
    for key, value in response_json['result'].items():
        assert type(value) is int or type(value) is float, f'Record {key}, value of {value} is not numeric'

def trades_api(url, email, password, exchange_to_retrieve, pair_to_retrieve):
    '''
    Call /markets/:exchange/:pair/trades endpoint, 
    Verify response code is 200 and response id, time_stamp, price and amount values exists and numeric
    '''
    markets_resp = requests.get(f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/trades', auth=HTTPBasicAuth(email, password))
    assert markets_resp.status_code == 200, f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/trades endpoint response status code is not 200, it is {markets_resp.status_code}'
    response_json = markets_resp.json()
    for i in response_json['result']:
        record_id = i[0]
        time_stamp = i[1]
        price = i[2]
        amount = i[3]
        assert type(record_id) is int or type(record_id) is float, f'Record id missing value'
        assert type(time_stamp) is int or type(time_stamp) is float, f'Record {record_id} missing time stamp value'
        assert type(price) is int or type(price) is float, f'Record {record_id} missing price value'
        assert type(amount) is int or type(amount) is float, f'Record {record_id} missing amount value'

def trades_limit_api(url, email, password, exchange_to_retrieve, pair_to_retrieve, integer_above_limit):
    '''
    Call /markets/:exchange/:pair/trades endpoint with limit parameter, 
    Verify response code is 200 and response number of records not exceed the parameter value
    '''
    markets_resp = requests.get(f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/trades', auth=HTTPBasicAuth(email, password), params={'limit':integer_above_limit})
    assert markets_resp.status_code == 200, f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/trades endpoint response status code is not 200, it is {markets_resp.status_code}'
    response_json = markets_resp.json()
    int(integer_above_limit) < len(response_json['result']), f'Number of trade records returned by API should not exceed {integer_above_limit}'

def hour_summary_api(url, email, password, exchange_to_retrieve, pair_to_retrieve):
    '''
    Call /markets/:exchange/:pair/summary endpoint, 
    Verify response code is 200 and response low value is smaller from high value
    '''
    markets_resp = requests.get(f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/summary', auth=HTTPBasicAuth(email, password))
    assert markets_resp.status_code == 200, f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/trades endpoint response status code is not 200, it is {markets_resp.status_code}'
    response_json = markets_resp.json()
    low_price = response_json['result']['price']['low']
    high_price = response_json['result']['price']['high']
    assert low_price < high_price, f'Low price - {low_price} is larger than high price - {high_price}'

def hour_markets_summaries_api(url, email, password, exchange):
    '''
    Call /markets/summaries endpoint, 
    Verify response code is 200 and find a records of an exchange parameter from response, verify there is more than 1 record and return a records list
    '''
    res_number_of_records = 0
    summary_records = []
    markets_resp = requests.get(f'{url}/markets/summaries', auth=HTTPBasicAuth(email, password))
    assert markets_resp.status_code == 200, f'{url}/markets/trades endpoint response status code is not 200, it is {markets_resp.status_code}'
    response_json = markets_resp.json()
    for i in response_json['result']:
        if exchange in i:
            res_number_of_records += 1
            summary_records.append(response_json['result'].get(i))
    assert res_number_of_records > 0, f'The api endpoint {url}/markets/summaries response missing records for {exchange} market'
    return summary_records

def order_book_api(url, email, password, exchange_to_retrieve, pair_to_retrieve, limit):
    '''
    Call /markets/:exchange/:pair/orderbook endpoint with limit aprameter, 
    Verify response code is 200 and response number of asks and bids records is equal to limit parameter
    '''
    markets_resp = requests.get(f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/orderbook', auth=HTTPBasicAuth(email, password), params={'limit':limit})
    assert markets_resp.status_code == 200, f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/orderbook endpoint response status code is not 200, it is {markets_resp.status_code}'
    response_json = markets_resp.json()
    number_of_asks = len(response_json['result']['asks'])
    number_of_bids = len(response_json['result']['bids'])
    assert number_of_asks == int(limit), f'Number of asks is {number_of_asks} which is not according to limit value of {limit}'
    assert number_of_bids == int(limit), f'Number of bids is {number_of_bids} which is not according to limit value of {limit}'

def specific_time_range_api(url, email, password, exchange_to_retrieve, pair_to_retrieve, before, after, periods):
    '''
    Call /markets/:exchange/:pair/ohlc endpoint with limit aprameter, 
    Verify response code is 200 and return response of a specific period
    '''
    markets_resp = requests.get(f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/ohlc', auth=HTTPBasicAuth(email, password), params={'before':before, 'after':after, 'periods':periods})
    assert markets_resp.status_code == 200, f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/ohlc endpoint response status code is not 200, it is {markets_resp.status_code}'
    response_json = markets_resp.json()
    return response_json['result'].values()
