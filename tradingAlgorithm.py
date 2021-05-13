import pandas as pd
import numpy as np
import os


def strategy_ret(ask_bid):  # 用strategy得到的return
    total_cost_in_function = 0
    max_cost_in_function = 0
    position_in_function = 0
    num_trans_in_function = 0
    for abt in ask_bid:
        if abt == 0:
            continue;
        elif abt > 0:
            position_in_function += 1000;
            total_cost_in_function += 1.0001 * 1000 * abt  # (1+换手率) * 1手 * ask
            num_trans_in_function += 1
        elif abt < 0:
            position_in_function -= 1000;
            total_cost_in_function += 0.9999 * 1000 * abt  # (1-换手率) * 1手 * bid
            num_trans_in_function += 1
        max_cost_in_function = max(max_cost_in_function, total_cost_in_function)
    return [total_cost_in_function, position_in_function, max_cost_in_function, num_trans_in_function]


def rolling_quantile(lst, rolling=300):
    long_in_function = (lst > lst.rolling(window=rolling).quantile(0.9)) & (lst > 0)
    short_in_function = (lst < lst.rolling(window=rolling).quantile(0.1)) & (lst < 0)
    return long_in_function, short_in_function


directory = "./Signal_588000"
lst_pnl = []
lst_rolling_window = []
for n in range(2, 100):
    total_gain = 0
    num_win = 0
    total_loss = 0
    num_loss = 0
    lst_max_cost = []
    lst_net_value = []
    lst_date = []
    lst_num_trans = []
    lst_sdv = []
    for filename in os.listdir(directory):
        lst_date.append(filename[0:8])
        file = directory + '/' + filename
        signal_temp = pd.read_pickle(file)
        ask = signal_temp['AskPrice1']
        bid = signal_temp['BidPrice1']
        long, short = rolling_quantile(signal_temp['PredictY'], n)
        net_ask_bid = ask * long - bid * short
        [total_cost, position, max_cost, num_trans] = strategy_ret(net_ask_bid)
        net_value = position * signal_temp['BidPrice1'][signal_temp.shape[0] - 1] * 0.9999 - total_cost
        lst_net_value.append(net_value)
        lst_max_cost.append(max_cost)
        lst_num_trans.append(num_trans)
        lst_sdv.append(np.std(signal_temp['Ret']))
        if net_value > 0:
            num_win += 1
            total_gain += net_value
        elif net_value <= 0:
            num_loss += 1
            total_loss -= net_value
    pnl = total_gain / num_win / (total_loss / num_loss)
    lst_pnl.append(pnl)
    lst_rolling_window.append(n)
    print(n)

pnl_df = pd.DataFrame({'rolling window': lst_rolling_window, 'pnl ratio': lst_pnl})
pnl_df = pnl_df.sort_values(by=['pnl ratio'])
pnl_df.to_csv('pnl_rolling.csv')
