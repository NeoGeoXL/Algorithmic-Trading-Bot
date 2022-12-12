
# Algorithmic Trading Bot
This Python project use the Yahoo Finance and Interactive Brokers API’s. This program has 2 trading bots that analyze the market in real time. The first bot analyzes a given list of stocks tickers and creates a trading signal based on the programmed strategy, using Triple Exponential Moving Average (TEMA) and Relative Strength Index (RSI). The second bot analyzes all the stocks listed on the NASDAQ and processes their information one by one to finally have a trading signal in Long or Short, then store in a database which of these stocks are more probable to continue their trend, for this purpose the Average Directional Index (ADX) and the difference between the TEMAS are used. Finally, the code creates a daily report of all open trades, profits or losses for the day. The indicators, strategies, data extraction and processing are programmed in Python, feel free to use this code in your projects.
## Disclaimer
This project is only for educational purposes and is not intended to be a financial recommendation; so use it at your own risk.

## Authors

- [@NeoGeoXL](https://www.github.com/NeoGeoXL)


## Licenses

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)


## Installation
To run this program, it is necessary to install all the libraries used in this project using the command:
```bash
  pip install –r requirements.txt
```
The libraries that will be installed are necessary for data processing such as pandas, numpy, as well as other libraries for graphing such as matplotlib or seaborn, also libraries for API’s connection such as yfinance or ib_insync to connect to Interactive Brokers.

To check the correct installation of the libraries will execute the command from the console:

```bash
  pip freeze
```
And check if the libraries are installed, to run this program in the command console will execute the command:
```bash
  python main.py
```
The developed trading program will be executed, and the following menu will be displayed to choose the desired option:

![menu](https://user-images.githubusercontent.com/76502399/207106448-354f4b5c-bbf7-4aef-97f6-0c40341ff63f.png)


## Guide
The values of the variables are in the config.py file where you can change the temporality of the stock, the list of stocks that you want to process, the capital, the risk and profit per operation, and the variables necessary for the calculation of trading indicators. To calculate the indicators, the time frame used for the TEMAS is 10, 50 and 100, as well as 14 for the RSI. These variables are located in this file to easily store them in a database and be able to perform a machine learning process.

![variables](https://user-images.githubusercontent.com/76502399/207113332-865cb55c-9bdf-4c3b-bb9b-e6fcb7fa3b0e.png)

The stock data price is extracted from the Yahoo Finance API, and a script was developed that allows the download of the data given only the ticker and the temporality. The data is processed in the “signals” created library that contains the programmed indicators, as well as the conditionals and the strategy to obtain a trade entry signal.


The strategy uses 3 TEMAS of 10, 50 and 100. If the TEMA of 10 is greater than the TEMA of 50 and the price is above the TEMA of 100 it indicates an upward trend, which is confirmed if the value of the RSI is greater than 50, otherwise it is a downtrend.

![uptrend](https://user-images.githubusercontent.com/76502399/207119157-bbe50091-5d9d-4f8b-a4be-87466c4c2d1d.png)

The trading bot library uses all these programmed resources to perform an analysis of the list of stocks that the user provides or the processing of all NASDAQ tickers. For the processing of the NASDAQ tickers, a csv file is used that has the information of the ticker and the sector to which it belongs, the strategy used is to determine which sector has a greater percent change and analyze if the index of this sector is in an upward trend, if it exists, all the tickers of this sector are filtered and processed with the same strategy programmed.

When the trading signals have been processed, to open operations in a broker, it is necessary to create a paper trading account at Interactive Brokers, because it provides $1M to test our trading bot, once the account is created, download and install Trading Workstation and login with the created account.

![login](https://user-images.githubusercontent.com/76502399/207127141-cd39f705-ddc5-4cf3-aaba-f92f0132aed4.png)

Once the account is configured, the program will automatically connect to Interactive Brokers. To open trades automatically the program will order the stocks with the highest ADX and open 10 trades with the highest ADX. The entry prices, stop loss and take profit are calculated in the program given the profit:loss ratio by the user.

![orders](https://user-images.githubusercontent.com/76502399/207128395-393aeabf-4b33-4200-bac7-fc3f30ed81d1.png)

## Daily Report

The program also creates a daily report of all the operations open in the day, for this the fpdf, matplotlib and seaborn libraries are used, in the initial part of the report it shows how much has been won or lost in the day followed by a graph of bars that show the daily open operations and how much has been won or lost in each of them.

![report1](https://user-images.githubusercontent.com/76502399/207123903-b0f5877e-1a66-4ef3-a948-f8560a698288.png)

The report also contains a pie graph of the won money in relation to the lost money, also show the relationship of the trades in Long and Short. Finally, the report shows in a bar graph of profit and lost in the Long and Short operations.

![report2](https://user-images.githubusercontent.com/76502399/207124957-27c7989c-ff30-48be-8932-60f4d6b0a9b4.png)


## Feedback

If you have any feedback, please reach out to my at ggarcia9539@gmail.com