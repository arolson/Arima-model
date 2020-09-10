from pyoanda import Client, PRACTICE
from pmdarima.arima import ARIMA, auto_arima
from datetime import timedelta
import datetime as dt
import pandas as pd
import numpy as np
import warnings
import time
import math
import os

SLEEP = 6
minutes = 5

timeframe = "M1"
n_periods_ahead = 5

CLOSE = 'close'
ADJCLOSE = 'adjclose'
OPEN = 'open'
HIGH = 'high'
LOW  = 'low'
VOLUME = 'volume'
ACCESS_TOKEN = os.environ['APIKEY_OANDA']

def run():
	symbol = input("Enter ticker symbol: ")
	
	now = dt.datetime.now()
	timeFinish = now + dt.timedelta(minutes=minutes)

	while (now < timeFinish):
		try:
			now = dt.datetime.now()

			client = Client(
			    environment=PRACTICE,
			    account_id="",
			    access_token=ACCESS_TOKEN
			)

			json_data = []

			json_data = client.get_instrument_history(
			    instrument=symbol,
			    granularity=timeframe,
			    candle_format="midpoint",
			    count=1440)
			json_data = json_data['candles']
			df = pd.DataFrame(json_data)

			data = df.copy()
			data = data.set_index('time')[['closeMid']]
			data = data.set_index(pd.to_datetime(data.index))
			data.columns = [CLOSE]

			# Rescale data
			lnprice = np.log(data)

			# Create and fit the model
			model_temp = auto_arima(lnprice.values, start_p=1, start_q=1,
                           max_p=1, max_q=1, m=4,
                           start_P=0, seasonal=False,
                           d=1, D=1, trace=True,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)
			
			model = ARIMA(order=model_temp.order)
			fit = model.fit(lnprice.values)

			# Predict
			future_forecast = fit.predict(n_periods=n_periods_ahead)
			future_forecast = np.exp(future_forecast)

			# Calculations
			lowest = min(future_forecast[0], future_forecast[-1])
			highest = max(future_forecast[0], future_forecast[-1])
			current = data[CLOSE].iloc[-1]
			x = ((future_forecast[0] - future_forecast[-1]) / future_forecast[0] ) * 100
			slope = (future_forecast[0] - future_forecast[-1]) / n_periods_ahead
			degree = math.degrees(math.atan(slope))

			# Trending
			if (x > 0): 
				trending = "Positivly / Call"
			else:
				trending = "Negativaly / Put"
			
			# View
			print("==========================")
			print("Current Price: ", current)
			print("Highest price: ", highest)
			print("Lowest Price: ", lowest)
			print("Trending: ", trending)
			print("Degrees: ", degree)
			print("==========================" + "\n")
		except Exception as e:
			print(e)
			
		time.sleep(SLEEP)
	
	return 0

if __name__ == "__main__":
	
	run()
	
