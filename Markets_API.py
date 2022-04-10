import json
import requests
from requests.auth import HTTPBasicAuth



def lists_limit_api(url, email, password, limit):
    #Testing https://api.cryptowat.ch/markets endpoint
    r = requests.get(f'{url}/markets', auth=HTTPBasicAuth(email, password), params={'limit':limit})
    assert r.status_code == 200, f'{url}/markets endpoint response status code is not 200, it is {r.status_code}'
    response_json = r.json()
    number_of_response_records = len(response_json['result'])
    #Assert on the number of markets returned by markets API
    print(number_of_response_records)
    assert int(number_of_response_records) == int(limit), f'Number of records stated on limit parameter {limit} is different from actual records returned by the API {number_of_response_records}'



def details_exchange_api(url, email, password, exchange_to_retrieve):
    #Testing https://api.cryptowat.ch/markets/:exchange endpoint
    r = requests.get(f'{url}/markets/{exchange_to_retrieve}', auth=HTTPBasicAuth(email, password))
    assert r.status_code == 200, f'{url}/markets/{exchange_to_retrieve} response status code is not 200, it is {r.status_code}'
    response_json = r.json()
    for i in response_json['result']:
        record_id = i.get('id')
        assert i.get('exchange') == exchange_to_retrieve, f'Record {record_id} exchange is not {exchange_to_retrieve} value'  #Assert on exchange values should be according to exchange parameter path


def details_pair_api(url, email, password, exchange_to_retrieve, pair_to_retrieve):
    #Testing https://api.cryptowat.ch/markets/:exchange/:pair endpoint
    r = requests.get(f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}', auth=HTTPBasicAuth(email, password))
    assert r.status_code == 200, f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve} endpoint response status code is not 200, it is {r.status_code}'
    response_json = r.json()
    record_id = response_json['result']['id']
    pair_value = response_json['result']['pair']
    assert pair_value == pair_to_retrieve, f'Record {record_id} pair is not {pair_to_retrieve} value'  #Assert on pair value should be according to pair parameter path

    
def price_api(url, email, password, exchange_to_retrieve, pair_to_retrieve):
    #Testing https://api.cryptowat.ch/markets/:exchange/:pair/price endpoint
    r = requests.get(f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/price', auth=HTTPBasicAuth(email, password))
    assert r.status_code == 200, f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/price endpoint response status code is not 200, it is {r.status_code}'
    response_json = r.json()
    price = response_json['result']['price']
    assert type(price) is int or type(price) is float, f'Record price value of {price} is not numeric'  #Assert on price value is numeric
    return price

def prices_api(url, email, password):
    #Testing https://api.cryptowat.ch/markets/prices endpoint
    r = requests.get(f'{url}/markets/prices', auth=HTTPBasicAuth(email, password))
    assert r.status_code == 200, f'{url}/markets/prices endpoint response status code is not 200, it is {r.status_code}'
    response_json = r.json()
    for key, value in response_json['result'].items():
        assert type(value) is int or type(value) is float, f'Record {key}, value of {value} is not numeric'  #Assert on price value is numeric for all the markets

def trades_api(url, email, password, exchange_to_retrieve, pair_to_retrieve):
    #Testing https://api.cryptowat.ch/markets/:exchange/:pair/trades endpoint
    r = requests.get(f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/trades', auth=HTTPBasicAuth(email, password))
    assert r.status_code == 200, f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/trades endpoint response status code is not 200, it is {r.status_code}'
    response_json = r.json()
    for i in response_json['result']:
        #Testing values of id, time_stamp, price and amount have numeric value
        record_id = i[0]
        time_stamp = i[1]
        price = i[2]
        amount = i[3]
        assert type(record_id) is int or type(record_id) is float, f'Record id missing value'
        assert type(time_stamp) is int or type(time_stamp) is float, f'Record {record_id} missing time stamp value'
        assert type(price) is int or type(price) is float, f'Record {record_id} missing price value'
        assert type(amount) is int or type(amount) is float, f'Record {record_id} missing amount value'

def trades_limit_api(url, email, password, exchange_to_retrieve, pair_to_retrieve, integer_above_limit):
    #Testing https://api.cryptowat.ch/markets/:exchange/:pair/trades/?limit: endpoint
    r = requests.get(f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/trades', auth=HTTPBasicAuth(email, password), params={'limit':integer_above_limit})
    assert r.status_code == 200, f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/trades endpoint response status code is not 200, it is {r.status_code}'
    response_json = r.json()
    int(integer_above_limit) < len(response_json['result']), 'Number of trade records returned by API should not exceed 1000'

def hour_summary_api(url, email, password, exchange_to_retrieve, pair_to_retrieve):
    #Testing https://api.cryptowat.ch/markets/:exchange/:pair/summary endpoint
    r = requests.get(f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/summary', auth=HTTPBasicAuth(email, password))
    assert r.status_code == 200, f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/trades endpoint response status code is not 200, it is {r.status_code}'
    response_json = r.json()
    low_price = response_json['result']['price']['low']
    high_price = response_json['result']['price']['high']
    assert low_price < high_price, f'Low price - {low_price} is larger than high price - {high_price}'

def hour_markets_summaries_api(url, email, password, exchange):
    #Testing https://api.cryptowat.ch/markets/summaries endpoint
    res_number_of_records = 0
    summary_records = []
    r = requests.get(f'{url}/markets/summaries', auth=HTTPBasicAuth(email, password))
    assert r.status_code == 200, f'{url}/markets/trades endpoint response status code is not 200, it is {r.status_code}'
    response_json = r.json()
    for i in response_json['result']:
        if exchange in i:
            res_number_of_records += 1
            summary_records.append(response_json['result'].get(i))
    assert res_number_of_records > 0, f'The api endpoint {url}/markets/summaries response missing records for {exchange} market'
    return summary_records

def order_book_api(url, email, password, exchange_to_retrieve, pair_to_retrieve, limit):
    #Testing https://api.cryptowat.ch/markets/:exchange/:pair/orderbook endpoint
    r = requests.get(f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/orderbook', auth=HTTPBasicAuth(email, password), params={'limit':limit})
    assert r.status_code == 200, f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/orderbook endpoint response status code is not 200, it is {r.status_code}'
    response_json = r.json()
    number_of_asks = len(response_json['result']['asks'])
    number_of_bids = len(response_json['result']['bids'])
    assert number_of_asks == int(limit), f'Number of asks is {number_of_asks} which is not according to limit value of {limit}'
    assert number_of_bids == int(limit), f'Number of bids is {number_of_bids} which is not according to limit value of {limit}'

def specific_time_range_api(url, email, password, exchange_to_retrieve, pair_to_retrieve, before, after, periods):
    #Testing https://api.cryptowat.ch/markets/:exchange/:pair/ohlc endpoint
    r = requests.get(f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/ohlc', auth=HTTPBasicAuth(email, password), params={'before':before, 'after':after, 'periods':periods})
    assert r.status_code == 200, f'{url}/markets/{exchange_to_retrieve}/{pair_to_retrieve}/ohlc endpoint response status code is not 200, it is {r.status_code}'
    response_json = r.json()
    return response_json['result'].values()
