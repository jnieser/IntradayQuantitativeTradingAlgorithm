# IntradayQuantitativeTradingAlgorithm
Clean Data - Get RAW Tick data from stock exchange and clean it to be able to input into XGBoost Model
GetSignalFromDataByXGBoost - Using XGBoost model to regress cleaned tick data on the stock price movement, and obtain the dim N * 1 signal to be input into trading algorithm
TradingAlgorithm - Trade on the signals extracted, with large positive signal, it means we need to buy; while with large negative signal, it means we need to well. If absolute value of the signal is relatively small we do nothing.

The tick data is not uploaded.
