# main.py

import os
import openai
import argparse
import requests
import json
import pandas as pd


def get_stock_data(ticker: str):
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    base_url = "https://www.alphavantage.co/query"

    # Fetch daily adjusted close prices
    function = "TIME_SERIES_DAILY_ADJUSTED"
    query = f"{base_url}?function={function}&symbol={ticker}&outputsize=full&apikey={api_key}"
    response = requests.get(query)
    data = response.json()

    # Check if Alpha Vantage returned an error
    if "Error Message" in data:
        print(f"Error fetching data from Alpha Vantage: {data['Error Message']}")
        exit(-1)

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")

    # Convert the '5. adjusted close' column to float
    df['5. adjusted close'] = df['5. adjusted close'].astype(float)

    # Get the closing price for today
    price = df["5. adjusted close"].iloc[0]

    # Calculate the 50-day and 200-day SMAs
    SMA_5 = df["5. adjusted close"].rolling(window=5).mean().iloc[4]
    SMA_200 = df["5. adjusted close"].rolling(window=200).mean().iloc[200]

    return price, SMA_5, SMA_200

def get_completion(messages):

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=[
            {
                "name": "get_stock_data",
                "description": "Get the price, 5-day SMA, and 200-day SMA of a stock",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "The stock ticker"
                        },
                    },
                    "required": ["ticker"],
                },
            },
        ]
    )

    return response




    

def main():

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Fetch stock data and analyze trend.')
    parser.add_argument('ticker', help='The stock ticker symbol')
    args = parser.parse_args()
    ticker = args.ticker
    
    # OpenAI Configuration
    openai.api_key = os.getenv("OPENAI_API_KEY")
    messages = [
        {"role": "user", "content": f"What's the trend of {ticker} stock?"},
    ]

    while True:
        response = get_completion(messages)

        if response.choices[0]["finish_reason"] == "stop":
            print(response.choices[0]["message"]["content"])
            break

        elif response.choices[0]["finish_reason"] == "function_call":
            fn_name = response.choices[0].message["function_call"].name
            arguments = response.choices[0].message["function_call"].arguments
            args = json.loads(response['choices'][0]['message']['function_call']['arguments'])

            function = globals()[fn_name]
            price, SMA_5, SMA_200 = function(**args)

            messages.append(
                {
                    "role": "assistant",
                    "content": None,
                    "function_call": {
                        "name": fn_name,
                        "arguments": arguments,
                    },
                }
            )

            messages.append(
                {
                    "role": "function", 
                    "name": fn_name, 
                    "content": f'{{"price": {price}, "SMA_5": {SMA_5}, "SMA_200": {SMA_200}}}'}
            )

            response = get_completion(messages)


if __name__ == "__main__":
    main()