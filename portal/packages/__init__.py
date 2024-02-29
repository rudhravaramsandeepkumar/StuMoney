import requests
from urllib3.exceptions import InsecureRequestWarning
import json
from datetime import datetime
import requests
from urllib3.exceptions import InsecureRequestWarning


def Get_One_Year_Data():
    faang_tickers = ["META", "AAPL", "AMZN", "NFLX", "GOOGL"]

    # Common API parameters
    period1 = "1668245512"  # Replace with your desired start date in Unix timestamp format
    period2 = "1699781512"  # Replace with your desired end date in Unix timestamp format
    interval = "1mo"
    events = "history"
    include_adjusted_close = "true"

    # Loop through the ticker symbols and construct API links
    temp_ = {}
    try:

        for ticker in faang_tickers:
            api_link = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?" \
                       f"period1={period1}&period2={period2}&interval={interval}&" \
                       f"events={events}&includeAdjustedClose={include_adjusted_close}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
            }
            print(api_link)
            # Make an API request to retrieve data for the current company
            response = requests.get(api_link, verify=False, headers=headers)

            if response.status_code == 200:
                data = response.json()
                # Process and store the data as needed
                # Modify this part to suit your specific data processing requirements
                historical_data = data["chart"]["result"][0]["indicators"]["quote"][0]["close"]
                # print(f"Historical data for {ticker}: {historical_data}")
                temp_[ticker] = historical_data

            else:
                # print(f"Error fetching data for {ticker}")
                temp_[ticker] = []
    except:
        temp_ = {}
    return temp_


def get_cal_(period1, period2, ticker, initial_investment):
    date_string_start = period1
    date_object = datetime.strptime(date_string_start, "%Y-%m-%d")
    timestamp1 = int(date_object.timestamp())

    date_string_start2 = period2
    date_object2 = datetime.strptime(date_string_start2, "%Y-%m-%d")
    timestamp2 = int(date_object2.timestamp())

    print('timestamp1',timestamp1)
    print('timestamp2', timestamp2)

    period1 = timestamp1  # Replace with your desired start date in Unix timestamp format
    period2 = timestamp2  # Replace with your desired end date in Unix timestamp format
    interval = "1mo"
    events = "history"
    ticker = ticker
    include_adjusted_close = "true"
    api_link = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?" \
               f"period1={period1}&period2={period2}&interval={interval}&" \
               f"events={events}&includeAdjustedClose={include_adjusted_close}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    # Make an API request to retrieve data for the current company
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    response = requests.get(api_link, verify=False, headers=headers)
    if response.status_code == 200:
        data_json = response.json()
        # Process and store the data as needed
        # Modify this part to suit your specific data processing requirements
        historical_data = data_json["chart"]["result"][0]["indicators"]["quote"][0]["close"]
        print(f"Historical data for {ticker}: {historical_data}")
    else:
        print(f"Error fetching data for {ticker}")

    # Extract relevant data from JSON
    first_trade_date = data_json["chart"]["result"][0]["meta"]["firstTradeDate"]
    end_date_timestamp = data_json["chart"]["result"][0]["timestamp"][-1]
    initial_investment = float(initial_investment)

    # Convert timestamps to human-readable date and time
    start_date = datetime.utcfromtimestamp(first_trade_date).strftime('%Y-%m-%d %H:%M:%S')
    end_date = datetime.utcfromtimestamp(end_date_timestamp).strftime('%Y-%m-%d %H:%M:%S')

    # Find the closest timestamp to the start date
    timestamps = data_json["chart"]["result"][0]["timestamp"]
    start_date_index = min(range(len(timestamps)), key=lambda i: abs(timestamps[i] - first_trade_date))

    # Get the closing prices for the start and end dates
    start_date_price = data_json["chart"]["result"][0]["indicators"]["quote"][0]["high"][start_date_index]
    end_date_price = data_json["chart"]["result"][0]["indicators"]["quote"][0]["high"][-1]

    # Calculate the number of shares you can buy at the start date
    num_shares_bought = initial_investment / start_date_price

    # Calculate the final investment value at the end date
    final_investment_value = num_shares_bought * end_date_price

    # Calculate the profit or loss
    value = final_investment_value - initial_investment

    # Print the results with human-readable dates
    print("Company name " + data_json["chart"]["result"][0]["meta"]["symbol"])
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print(f"Number of shares bought at the start date: {num_shares_bought:.2f}")
    print(f"Final investment value at the end date: ${final_investment_value:.2f}")
    if value >= 0:
        {
            print(f"Profit is : {value}")
        }

    else:
        {
            print(f"Loss is : {value}")
        }

    print(f"initial_investment : {initial_investment}")
    print(f"final investment: {final_investment_value}")
    Company_name_=data_json["chart"]["result"][0]["meta"]["symbol"]
    return Company_name_,start_date,end_date,num_shares_bought,final_investment_value,initial_investment,round(final_investment_value,2),value
# temp_=Get_One_Year_Data()
# print('temp_',temp_)
