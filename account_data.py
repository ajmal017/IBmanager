from __future__ import (absolute_import, division, print_function,)
#                        unicode_literals)
import config
import collections
import sys

if sys.version_info.major == 2:
    import Queue as queue
    import itertools
    map = itertools.imap

else:  # >= 3
    import queue


import ib.opt
import ib.ext.Contract

import pandas as pd


import logging

logging.basicConfig(level=None)


pd.set_option('display.max_columns', 500)

from datetime import datetime,date


from ib_insync import *


from os import path



class IbManager(object):
    def __init__(self, timeout=20, **kwargs):
        self.q = queue.Queue()
        self.timeout = 20
        self.port = object
        self.con = ib.opt.ibConnection(**kwargs)
        self.con.registerAll(self.watcher)

        self.msgs = {
            ib.opt.message.error: self.errors,
            ib.opt.message.updatePortfolio: self.acct_update,
            ib.opt.message.accountDownloadEnd: self.acct_update,
        }

        # Skip the registered ones plus noisy ones from acctUpdate
        self.skipmsgs = tuple(self.msgs.keys()) + (
            ib.opt.message.updateAccountValue,
            ib.opt.message.updateAccountTime)

        for msgtype, handler in self.msgs.items():
            self.con.register(handler, msgtype)

        self.con.connect()

    def watcher(self, msg):
        if isinstance(msg, ib.opt.message.error):
            if msg.errorCode > 2000:  # informative message
                print('-' * 10, msg)

        elif not isinstance(msg, self.skipmsgs):
            print('-' * 10, msg)

    def errors(self, msg):
        if msg.id is None:  # something is very wrong in the connection to tws
            self.q.put((True, -1, 'Lost Connection to TWS'))
        elif msg.errorCode < 1000:
            self.q.put((True, msg.errorCode, msg.errorMsg))

    def acct_update(self, msg):
        self.q.put((False, -1, msg))

    def get_account_update(self):
        self.con.reqAccountUpdates(True, 'D999999')

        portfolio = list()
        while True:
            try:
                err, mid, msg = self.q.get(block=True, timeout=self.timeout)
            except queue.Empty:
                err, mid, msg = True, -1, "Timeout receiving information"
                break

            if isinstance(msg, ib.opt.message.accountDownloadEnd):
                break

            if isinstance(msg, ib.opt.message.updatePortfolio):
                c = msg.contract

                entry = collections.OrderedDict(msg.items())

                # Don't do this if contract object needs to be referenced later
                # entry['contract'] = None
                entry['ticker'] = c.m_symbol  # replace object with the ticker
                entry['secType'] = c.m_secType  # replace object with the ticker
                entry['strike'] = c.m_strike  # replace object with the ticker
                entry['expiry'] = c.m_expiry  # replace object with the ticker
                entry['multiplyer'] = c.m_multiplier
                entry['kind'] = c.m_right




                portfolio.append(entry)

                portfoliodf = pd.DataFrame.from_dict(portfolio)
        return portfolio,portfoliodf, err, mid, msg


def get_account_value(port):
    ib = IB()
    ib.connect('127.0.0.1', port, clientId=1)

    summary = ib.accountSummary()

    dict = {'liquidation_value':summary[20][2],'total_cash':summary[22][2]}

    # list = []
    # for i in summary:
    #     list.append(i[1])
    # print(list)

    return dict


ports_paper = {'TWS': 7497,'IBGW':4002}


ports_live = {'TWS': 7497 , 'IBGW':4001 }

# # #
ibm = IbManager(port=ports_live['TWS'])
# #
df = ibm.get_account_update()[1]
# # #
# print(df)
# p_l_total = df['unrealizedPNL'].sum()
#
#
# # #
# # val = get_account_value(ports_paper['TWS'])
val = get_account_value(ports_live['TWS'])
print(val)
# print(p_l_total)


def save_pos_csv(path = config.db_path+'/IBKR', df = df,acc = 'NaN'):

    df.to_csv(path+'/Positions'+datetime.today().strftime(format="%Y-%m-%d-")+acc+'.csv')


def line_prepender(acc= '2530531'):


    PATH = path.join(config.db_path, 'mysql_db_csv/portfolio_value/',acc+'.csv')
    df = pd.read_csv(PATH)
    print(df.tail())
    new_row=pd.DataFrame([[date.today().strftime('%Y-%m-%d'),val["liquidation_value"],2,int(acc),float(val["liquidation_value"])-float(val["total_cash"]),val["total_cash"],'USD']],columns=['Date','total_value','broker_id','account_number','portfolio_value','cash','currency'])
    new_row=new_row.reset_index(drop=True)
    df=df.reset_index(drop=True)
    print(new_row)
    df=df.append(new_row.reset_index(drop=True))

    df=df.reset_index(drop=True)
    df['entry']=0
    print(df.tail(10))
    df.to_csv(PATH, index=False)


# save_pos_csv()

line_prepender()
sys.exit(0)  # Ensure ib thread is terminated