# ChatGPT-Functions
Experimenting with ChatGPT [Function Calling](https://openai.com/blog/function-calling-and-other-api-updates)

Python script that accepts a stock ticker symbol as a command-line argument. It fetches the stock's price, 5-day Simple Moving Average (SMA), and 200-day SMA from the Alpha Vantage API, and then asks the AI to analyze the trend based on this data.

# Setup Environment

## Python dependencies

``` shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## API keys
[Alpha Vantage](https://www.alphavantage.co/):
Export as `ALPHA_VANTAGE_API_KEY` environment variable.

[OpenAI](https://platform.openai.com/):
Export as `OPENAI_API_KEY` environment variable.

# Execute program
``` shell
$ python main.py {TICKER}
```

``` shell
$ python main.py VTI 

The trend of VTI stock is currently showing a slight downward movement. The current price is $218.18, which is slightly lower than the 5-day Simple Moving Average (SMA) of $218.48. However, it is still higher than the 200-day SMA of $197.93, indicating a long-term upward trend.
```

