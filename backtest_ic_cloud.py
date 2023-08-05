
''' THis is IChimoku Backtesting Module
    500 rs stoploss '''

import datetime

import pandas as pd
from datetime import date
import math

from ta.trend import trix

from ta.trend import ichimoku_base_line ,ichimoku_conversion_line,ichimoku_a,ichimoku_b

from ta.momentum import RSIIndicator,ultimate_oscillator,kama,pvo,rsi

def bot_ij(stock,df,BTGT,STGT):
    TRADE_CHART = []
    fund = 100000
    PNL = 0
    num_of_trades = 0
    df['I_B'] = ichimoku_conversion_line(df['High'],df['Low'])
    df['I_BB'] =ichimoku_base_line(df['High'],df['Low'])
    # df['claud_a'] =ichimoku_a(df.High,df.Low)
    # df['claud_b'] = ichimoku_b(df.High, df.Low)
    df['RSI'] = rsi(df['Close'])
    # df['kama'] = pvo(df.Volume)

    gain = 0
    lose = 0
    trade = 0
    exit_date = ''
    sell_price = 0.0
    signal  = 0
    target_exit = 0.0
    buy_price = 0.0
    stop_loss = 0.0
    quantity = 150
    entry_date = ''
    buy_sell = ''
    df['Entry'] = None
    df['Exit'] = None
    count = 1
    try:
        for num in range(len(df)):


            hr = 15
            condition_buy = [df['I_B'][num] > df['Open'][num] , df['I_B'][num] < df['Close'][num] ,
                    trade==0,df['Open'][num] < df['Close'][num]
                    ,df['Date'][num].hour != hr,df['I_BB'][num] <= df['I_B'][num],
                           df['RSI'][num] < 70] #
            condition_sell = [df['I_B'][num] > df['Close'][num] , df['I_B'][num] < df['Open'][num] ,
                     trade==0,df['Open'][num] > df['Close'][num]
                    ,df['Date'][num].hour != hr,df['I_BB'][num] >= df['I_B'][num],
                              df['RSI'][num] > 30]#,df['I_BB'][num] > df['I_B'][num]

            if all(condition_buy):
                buy_price = df['High'][num]
                stop_loss = df['Low'][num]
                target = buy_price * BTGT
                sl = target + target* 0.0
                brokerage_buy = buy_price*quantity *0.00026
                if df['High'][num+1] > df['High'][num]+0.5:
                    num_of_trades += 1
                    if abs(stop_loss-buy_price) > sl:
                        stop_loss = buy_price-target
                    quantity = math.floor(500/abs(stop_loss-buy_price))
                    if quantity > 15:
                        quantity = 15
                    target_exit = buy_price + target
                    entry_date = df['Date'][num + 1]

                    signal = True
                    trade = 1
                    buy_sell = 'BUY'
                    num1 = num

            elif all(condition_sell) :
                sell_price = df['Low'][num]
                stop_loss = df['High'][num]
                if df['Low'][num+1] < df['Low'][num]-0.5 :
                    num_of_trades += 1
                    target = sell_price*STGT
                    sl = target+target* 0.0
                    brokerage_sell = sell_price * quantity * 0.00026
                    if abs(stop_loss - sell_price) > sl:
                        stop_loss = sell_price +target
                    quantity = math.floor(500/abs(stop_loss-sell_price))

                    if quantity > 15:
                        quantity = 15
                    target_exit = sell_price - target
                    entry_date = df['Date'][num+1]

                    signal = True
                    trade = 1
                    buy_sell ='SELL'
                    num1 = num
                    # if df['Date'][num].hour == 9 and df['Date'][num].minute == 15 and abs(df['High'][num]-df['Low'][num]) > 50:
                    #     signal = False
                    #     trade = 0
                    #     count += 1

            elif signal and buy_sell== 'BUY' and num1 < num:
                if stop_loss > df['Close'][num] and buy_sell== 'BUY' and num1 < num:
                    exit_date = df['Date'][num]
                    sell_price = df['Close'][num]
                    brokerage_sell = sell_price * quantity * 0.00026
                    brokerage = brokerage_buy+brokerage_sell
                    PNL = PNL - (buy_price - sell_price) * quantity -brokerage
                    profit_loss = (sell_price - buy_price) * quantity -brokerage
                    fund = fund + profit_loss
                    lose += 1
                    trade_chart = [stock,num_of_trades, entry_date, buy_price, quantity,stop_loss ,exit_date, sell_price, lose,
                                   gain, PNL,profit_loss, fund,buy_sell]
                    TRADE_CHART.append(trade_chart)
                    signal = False
                    trade = 0
                if target_exit < df['High'][num]:
                    exit_date = df['Date'][num]
                    sell_price = target_exit
                    brokerage_sell = sell_price * quantity * 0.00026
                    brokerage = brokerage_buy+brokerage_sell
                    PNL = PNL - (buy_price - sell_price) * quantity -brokerage
                    profit_loss = (sell_price - buy_price) * quantity -brokerage
                    fund = fund + profit_loss
                    gain += 1
                    trade_chart = [stock,num_of_trades, entry_date, buy_price, quantity,stop_loss, exit_date, sell_price, lose,
                                   gain, PNL,profit_loss, fund,buy_sell]
                    TRADE_CHART.append(trade_chart)
                    signal = False
                    trade = 0
                if df['Date'][num].hour == 15 and df['Date'][num].minute == 15:
                    exit_date = df['Date'][num]
                    sell_price = df['Open'][num]
                    brokerage_sell = sell_price * quantity * 0.00026
                    brokerage = brokerage_buy+brokerage_sell
                    PNL = PNL - (buy_price - sell_price) * quantity - brokerage
                    profit_loss = (sell_price - buy_price) * quantity - brokerage
                    fund = fund + profit_loss
                    if profit_loss > 0:
                        gain += 1
                    else:
                        lose += 1
                    trade_chart = [stock,num_of_trades, entry_date, buy_price, quantity, stop_loss, exit_date, sell_price,
                                   lose,
                                   gain, PNL, profit_loss, fund, buy_sell]
                    TRADE_CHART.append(trade_chart)

                    signal = False
                    trade = 0


            elif signal and buy_sell== 'SELL' and num1 < num:
                if stop_loss < df['Close'][num] and buy_sell== 'SELL' and num1 < num:
                    exit_date = df['Date'][num]
                    buy_price = df['Close'][num]
                    brokerage_buy = buy_price * quantity * 0.00026
                    brokerage = brokerage_buy + brokerage_sell
                    PNL = PNL - (buy_price - sell_price) * quantity -brokerage
                    profit_loss = (sell_price - buy_price) * quantity -brokerage
                    fund = fund + profit_loss
                    lose += 1
                    trade_chart = [stock,num_of_trades, entry_date, buy_price, quantity,stop_loss ,exit_date, sell_price, lose,
                                   gain, PNL,profit_loss, fund,buy_sell]
                    TRADE_CHART.append(trade_chart)
                    signal = False
                    trade = 0
                if target_exit >= df['Low'][num]:
                    exit_date = df['Date'][num]
                    buy_price = target_exit
                    brokerage_buy = buy_price * quantity * 0.00026
                    brokerage = brokerage_buy + brokerage_sell
                    PNL = PNL - (buy_price - sell_price) * quantity -brokerage
                    profit_loss = (sell_price - buy_price) * quantity -brokerage
                    fund = fund + profit_loss
                    gain += 1
                    trade_chart = [stock,num_of_trades, entry_date, buy_price, quantity,stop_loss, exit_date, sell_price, lose,
                                   gain, PNL,profit_loss, fund,buy_sell]
                    TRADE_CHART.append(trade_chart)

                    signal = False
                    trade = 0

                if df['Date'][num].hour == 15 and df['Date'][num].minute == 15:
                    exit_date = df['Date'][num]
                    buy_price = df['Open'][num]
                    brokerage_buy = buy_price * quantity * 0.00026
                    brokerage = brokerage_buy + brokerage_sell
                    PNL = PNL - (buy_price - sell_price) * quantity - brokerage
                    profit_loss = (sell_price - buy_price) * quantity - brokerage
                    fund = fund + profit_loss
                    if profit_loss > 0:
                        gain += 1
                    else:
                        lose += 1
                    trade_chart = [stock,num_of_trades, entry_date, buy_price, quantity, stop_loss, exit_date, sell_price,
                                   lose,
                                   gain, PNL, profit_loss, fund, buy_sell]
                    TRADE_CHART.append(trade_chart)

                    signal = False
                    trade = 0
    except:
        pass
    data = pd.DataFrame(TRADE_CHART, columns=["stock",'trades', 'entry_date', 'buy_price',
                                              'quantity','Stop_loss', 'exit_date', 'sell_price', 'lose', 'gain', 'PNL',
                                              'ProfitLoss','Fund','BUY/SELL'])

    # print(PNL, "PROFIT")
    print((data.quantity.mean()))
    print((data.quantity.max()))
    print(gain, (gain/(gain+lose)),"SUCCESS")
    return  data

def backtest(df):
    df['Date'] = [datetime.datetime.strptime(df['Date'].iloc[x], "%Y-%m-%d %H:%M:%S") for x in range(len(df))]
    data = bot_ij(df)
    return data

    # import matplotlib.pyplot as plt
    # plt.style.use('fivethirtyeight')
    # plt.figure(figsize=(12.2, 4.5))
    # plt.title(stock)
    # plt.plot(data['Fund'], color='green')
    # # plt.scatter(df.index,df['Entry'],color='red',marker='v',alpha=1)
    # # plt.scatter(df.index, df['Exit'], color='green', marker='^', alpha=1)
    # plt.show()
    # # df.to_csv('datasets/rel.csv')
    # data.to_csv('datasets/backtest/baj_buy.csv')



if __name__ == '__main__':
    pass