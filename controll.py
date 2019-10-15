
from ib_insync import ibcontroller
from ib_insync import connection
from ib_insync import *

import config

ports_paper = {'TWS': 7497,'IBGW':4002}


ports_live = {'TWS': 7497 , 'IBGW':4001 }


gtw = ibcontroller.IBC(twsVersion= 972,gateway=True, tradingMode='live',userid=config.ib_usr,password=config.ib_pw)

ib = IB()
# ib.connect('127.0.0.1', 4001, clientId=1, readonly=True)

def start_ib_send_msg(port):
    print(ib.isConnected())

start_ib_send_msg(ports_live['IBGW'])


gtw.start()
IB.run()