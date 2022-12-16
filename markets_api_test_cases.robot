*** Settings ***
Library    markets_api.py

*** Variables ***
${url}    https://api.cryptowat.ch
${email}    yeyoxo4705@dni8.com
${password}    CryptoKing1234$#@!
${limit}    10
${exchange to retrieve}    coinbase
${pair_to_retrieve}    btceur



*** Test Cases ***
1. API test case - Check number of markets on API response is according to limit param value
    [Documentation]    Testing https://api.cryptowat.ch/markets with limit parameter value
    lists_limit_api    url=${url}    email=${email}    password=${password}    limit=${limit}

2. API test case - Check exchange retrievel according to specific exchange value
    [Documentation]    Testing https://api.cryptowat.ch/markets/:exchange and checking returned records according to exchange value
    details_exchange_api    url=${url}    email=${email}    password=${password}    exchange_to_retrieve=${exchange to retrieve}

3. API test case - Check exchange rerievel according to specific exchange and pair values
    [Documentation]    Testing https://api.cryptowat.ch/markets/:exchange/:pair and checking returned records according to exchange and pair values
    details_pair_api    url=${url}    email=${email}    password=${password}    exchange_to_retrieve=${exchange to retrieve}    pair_to_retrieve=${pair_to_retrieve}

4. API test case - Check price value of specific exchange and pair is numeric
    [Documentation]    Testing https://api.cryptowat.ch/markets/:exchange/:pair/price and checking price value for a specific exchange and pair is numeric
    ${price}=    price_api    url=${url}    email=${email}    password=${password}    exchange_to_retrieve=${exchange to retrieve}    pair_to_retrieve=${pair_to_retrieve}
    Log    For exchange ${exchange to retrieve} and pair ${pair_to_retrieve}, the price is ${price}

5. API test case - Check price values for all exchanges is numeric
    [Documentation]    Testing https://api.cryptowat.ch/markets/prices and checking price values for all exchanges is numeric
    prices_api    url=${url}    email=${email}    password=${password}

6. API test case - Check fields response are numeric for trades endpoint in a specific exchange and pair
    [Documentation]    Testing https://api.cryptowat.ch/markets/:exchange/:pair/trades and checking id, timestamp, price and amount are numeric in the 
                ...    response for a specific exchange and pair
    trades_api    url=${url}    email=${email}    password=${password}    exchange_to_retrieve=${exchange to retrieve}    pair_to_retrieve=${pair_to_retrieve}

7. API test case - Verify response max record limit for trades is 1000
    [Documentation]    Testing https://api.cryptowat.ch/markets/:exchange/:pair/trades/?limit and checking response number of records will not exceed 1000
    ${integer above 1000}    Set Variable    1001
    trades_limit_api    url=${url}    email=${email}    password=${password}    exchange_to_retrieve=${exchange to retrieve}    pair_to_retrieve=${pair_to_retrieve}    integer_above_limit=${integer above 1000}

8. API test case - Check specific exchange and pair low and high prices and validate values match names
    [Documentation]    Testing https://api.cryptowat.ch/markets/:exchange/:pair/summary and checking low price value is smaller than high price value for 
                ...    a specific exchange and pair
    hour_summary_api    url=${url}    email=${email}    password=${password}    exchange_to_retrieve=${exchange to retrieve}    pair_to_retrieve=${pair_to_retrieve}

9. API test case - Return records of exchange that contains specific string
    [Documentation]    Testing https://api.cryptowat.ch/markets/summaries  and printing the summary records of exchange contains specific string
    ${exchange string}    Set Variable    binance
    ${summary records}=    hour_markets_summaries_api    url=${url}    email=${email}    password=${password}    exchange=${exchange string}
    Log    ${summary records}

10. API test case - Check orderbook api and verify number of asks and bid according to limit
    [Documentation]    Testing https://api.cryptowat.ch/markets/:exchange/:pair/orderbook  and check number of asks and bid according to limit 
                ...    for a specific exchange and pair
    order_book_api    url=${url}    email=${email}    password=${password}    exchange_to_retrieve=${exchange to retrieve}    pair_to_retrieve=${pair_to_retrieve}    limit=${limit}

11. API test case - Check ohlc returned data according to specific time range
    [Documentation]    Testing https://api.cryptowat.ch/markets/:exchange/:pair/ohlc and check if data ohlc data returned according to the time range
    ${before}    Set Variable    1649534894
    ${after}    Set Variable    1649448494
    ${periods}    Set Variable    3600
    ${ohlc data}=    specific_time_range_api    url=${url}    email=${email}    password=${password}    exchange_to_retrieve=${exchange to retrieve}    pair_to_retrieve=${pair_to_retrieve}    before=${before}    after=${after}    periods=${periods}
    Log    ${ohlc data}

