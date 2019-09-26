
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection, message
import time
from ib.ext.EWrapper import EWrapper



#
# class MessageHandler(object):
#     ''' class for handling incoming messages '''
#
#     def __init__(self, tws):
#         ''' create class, provide ibConnection object as parameter '''
#         self.nextValidOrderId = None
#
#         tws.registerAll(self.debugHandler)
#         tws.register(self.nextValidIdHandler, 'NextValidId')
#
#     def nextValidIdHandler(self, msg):
#         ''' handles NextValidId messages '''
#         self.nextValidOrderId = msg.orderId
#         print(self.nextValidOrderId)
#         return self.nextValidOrderId
#
#     def debugHandler(self, msg):
#         """ function to print messages """
#         print(msg)

# def handle_order_id(msg):
#     global newOrderID
#     newOrderID = msg.orderId
#     print("inside handle_order_id: ", newOrderID)
#


def mod_id():
    with open('orderID', 'r') as file:
        orderID = int(file.read())


    with open('orderID', 'w') as file:
        newid = orderID + 1
        file.writelines(str(newid))
    return newid



def error_handler(msg):
    """Handles the capturing of error messages"""
    print ("Server Error: %s" % msg)

def reply_handler(msg):
    """Handles of server replies"""
    print ("Server Response: %s, %s" % (msg.typeName, msg))


def create_contract(symbol, sec_type, exch, prim_exch, curr):
    """Create a Contract object defining what will
    be purchased, at which exchange and in which currency.

    symbol - The ticker symbol for the contract
    sec_type - The security type for the contract ('STK' is 'stock')
    exch - The exchange to carry out the contract on
    prim_exch - The primary exchange to carry out the contract on
    curr - The currency in which to purchase the contract"""
    contract = Contract()
    contract.m_symbol = symbol
    contract.m_secType = sec_type
    contract.m_exchange = exch
    contract.m_primaryExch = prim_exch
    contract.m_currency = curr
    return contract

def create_order(order_type, quantity, action,lmt = None):
    """Create an Order object (Market/Limit) to go long/short.

    order_type - 'MKT', 'LMT' for Market or Limit orders
    quantity - Integral number of assets to order
    action - 'BUY' or 'SELL'"""
    order = Order()
    order.m_orderType = order_type
    order.m_totalQuantity = quantity
    order.m_action = action
    if lmt!=None :
        order.m_lmtPrice = lmt
    return order

def place_stk_order(ticker, ordertype,limit, quantity, buy_sell):
    # Connect to the Trader Workstation (TWS) running on the
    # usual port of 7496, with a clientId of 100
    # (The clientId is chosen by us and we will need
    # separate IDs for both the execution connection and
    # market data connection)
    global newOrderID
    global order_id


    ports_paper = {'TWS': 7497, 'IBGW': 4002}

    conn = Connection.create(port=ports_paper['TWS'], clientId=100)
    conn.connect()

    # Assign the error handling function defined above
    # to the TWS connection
    conn.register(error_handler, 'Error')

    # Assign all of the server reply messages to the
    # reply_handler function defined above
    conn.registerAll(reply_handler)

    # # Create an order ID which is 'global' for this session. This
    # # will need incrementing once new orders are submitted.
    # conn.register(handle_order_id, 'NextValidId')
    #
    # # Receive the new OrderID sequence from the IB Server
    # conn.reqIds(0)
    #
    # # Print the new OrderID that was sent by IB
    # print('here:  ',newOrderID)



    # Create a contract in GOOG stock via SMART order routing
    order_contract = create_contract(symbol = ticker,
                                    sec_type = 'STK',
                                    exch = 'SMART',
                                    prim_exch = 'ISLAND' or 'SMART',
                                    curr = 'USD')

    # Go long 100 shares of Google

    order_id = mod_id()

    if ordertype == 'MKT':
        order_details = create_order(ordertype, quantity, buy_sell)
        print('Placed MKT order with ID: ',order_id,' ', ticker)
    else:
        order_details = create_order(ordertype, quantity, buy_sell,limit)
        print('Placed LMT order with ID: ',order_id,' ',ticker)


    # Use the connection to the send the order to IB
    conn.placeOrder(contract=order_contract, order=order_details,id=order_id)

    # Disconnect from TWS
    conn.disconnect()
    time.sleep(1)
    print('Disconnected')




place_stk_order('F','LMT', 1,1,'BUY')
place_stk_order('MSFT','LMT', 1,1,'BUY')
place_stk_order('SPY','LMT', 1,1,'BUY')
place_stk_order('FB','LMT', 1,1,'BUY')
place_stk_order('AAPL','LMT', 1,1,'BUY')
place_stk_order('NFLX','LMT', 1,1,'BUY')

#time.sleep(5)
#place_stk_order('','MKT', None,1,'BUY')