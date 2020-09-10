# Arima-model
## Description
The goal of this project is to create an Arima machine learning model to predict the direction of a Forex currency price for binary options. 

## Disclamer 
Past performance is no guarantee of future results. Don't assume an investment will continue to do well in the future simply because it's done well in the past.
This program is for learning purposes only do not take it as investment advice. I made this for fun please do not sue me. 

## How to use
### Enviroment
- Make sure all dependencies are installed
- Open an Oanda account and get an API key
- Store the key in your bash_profile or bashrc ex: `export APIKEY_OANDA = YOUR_API_KEY`
- Install Conda - https://docs.conda.io/projects/conda/en/latest/user-guide/index.html
- conda create -n pmdarima --yes python=3.5 scipy numpy scikit-learn pandas statsmodels
- conda activate pmdarima
- pip install pyoanda

### Run 
Make sure your conda enviroment is active and you are in the correct directory.
- chmod +x script.py
- ./script.py
- use a correct ticker format ex: `EUR_USD`

## Make adjustments within the code
- The `timeframe` can be changed to any of Oandas candlestick timeframes. eg: `S15` `S30` `M1` `M5` `M15`; Default is M1 (1 minute)
- `minutes` is the amount of time to run the program (in minutes)
- `SLEEP` is the amount of time the program waits before making another call. Default is 6 seconds
- `n_periods_ahead` is the number of candlesticks we are trying to look ahead. Default is 5
- `ACCESS_TOKEN` is your API_KEY (string)
