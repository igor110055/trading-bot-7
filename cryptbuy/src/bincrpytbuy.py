#!/usr/bin/env python

from tradingview_ta import *
from datetime import date,datetime
from time import sleep
from binance.client import Client
from binance import ThreadedWebsocketManager
from binance.exceptions import BinanceAPIException, BinanceOrderException
import tradingview_ta,time,os,logging


def exitPos(entryprice):
    posExit=TA_Handler(
        symbol=currency,
        exchange='BINANCE',
        screener='CRYPTO',
        interval=Interval.INTERVAL_5_MINUTES
        )
    while True:
        ema20 = posExit.get_analysis().indicators["EMA20"]
        closeprice = posExit.get_analysis().indicators["close"]
        diff = closeprice - ema20
        logger.info (f"In Buy Position => ema20 = {str(round(ema20,2))} closeprice= {str(round(closeprice,2))} diff= {str(round(diff,2))}")
        time.sleep(30)
        if (diff < stoploss):
            logger.info("postion Exit")
            try:
                market_order = client.futures_create_order(symbol=currency,side='SELL',type='MARKET',quantity=qty)
                logger.info(market_order)
                exitprice = posExit.get_analysis().indicators["close"]
                profit = round(entryprice,2)-round(exitprice,2)
                now = datetime.now()
                logger.warning(f"Entry Price:  {str(round(entryprice,2))} Exit price: {str(round(exitprice,2))} Profit: {str(round(profit,2))} at {str(now)}")
                orderLogger.warning(f"Entry Price:  {str(round(entryprice,2))} Exit price: {str(round(exitprice,2))} Profit: {str(round(profit,2))} at {str(now)}")
                #send notification
                break
            except BinanceAPIException as e:
                # error handling goes here
                logger.exception(e)
            except BinanceOrderException as e:
                # error handling goes here
                logger.exception(e)


#start of main program

#init variables from env
coin = os.environ.get('coin') #BTC
currency = coin + 'USDT'
 
qty = os.environ.get('qty')
hist = float(os.environ.get('hist'))
stoploss = float(os.environ.get('stoploss'))

#print(tradingview_ta.__version__)
#create logger
logger = logging.getLogger(__name__)
#set log level
logger.setLevel(logging.INFO)

orderLogger = logging.getLogger('orderlog')
orderLogger.setLevel(logging.WARNING)

#define file handler and set formatter
logFilePath = "./logs"
logFileName = logFilePath + '/' + coin + 'buy.log'
if(not os.path.exists(logFilePath)):
    os.makedirs(logFilePath)
orderFileName = logFilePath + '/' + coin + 'order.log'

file_handler = logging.FileHandler(logFileName)
order_handler = logging.FileHandler(orderFileName)
formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
order_handler.setFormatter(formatter)

logger.addHandler(file_handler)
orderLogger.addHandler(order_handler)

orderLogger.warning(f'Initalize Orderlog')

# init
api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')
client = Client(api_key, api_secret)
#client.API_URL = 'https://testnet.binance.vision/api'
#client.API_URL = os.environ.get('API_URL')

#verify account
#print(client.get_account())
#logger.info(client.get_asset_balance(asset=coin))

# get balances for futures account
#print(client.futures_account_balance())

# get latest price from Binance API
#curr_price = client.get_symbol_ticker(symbol=currency)
# print full output (dictionary)
#logger.info(curr_price)

while True:
    #Instantiate TA_Handler
    posHandler=TA_Handler(
        symbol=currency,
        exchange='BINANCE',
        screener='CRYPTO',
        interval=Interval.INTERVAL_15_MINUTES
        )

    while True:
        macd = posHandler.get_analysis().indicators["MACD.macd"]
        signal = posHandler.get_analysis().indicators["MACD.signal"]
        histval = macd - signal
        logger.info (f"Taking Position => MACD = {str(round(macd,2))}  Signal={str(round(signal,2))} Histogram=  {str(round(histval,2))}")
        time.sleep(30)
        if (histval > hist):
            closeprice = posHandler.get_analysis().indicators["close"]
            try:
                market_order = client.futures_create_order(symbol=currency,side='BUY',type='MARKET',quantity=qty)
                logger.info(market_order)
                now = datetime.now()
                logger.warning(f"Buy order executed at closeprice: {str(closeprice)} at {str(now)}")
                orderLogger.warning(f"Buy order executed at closeprice: {str(closeprice)} at {str(now)}")
                exitPos(closeprice)
                #send notification
                #exit position
                break
            except BinanceAPIException as e:
                # error handling goes here
                logger.error(e)
            except BinanceOrderException as e:
                # error handling goes here
                logger.error(e)

