from ib.opt import ibConnection, Connection, message
import sys

# newOrderID = int
#
# def handle_order_id(msg):
#     global newOrderID
#     newOrderID = msg.orderId
#     print("Test")


#
# f= open("orderID","r")
#
# orderID =f.read()
# print(orderID)
#
# f.close()

# a= open("orderID",'w')
# print(a,'a')
# for line in a:
#     newid = int(orderID) +5
#     line.replace(str(orderID), str(newid))
#     print("OrderID: ", orderID,'newid',newid)
# a.close()



with open('orderID', 'r') as file:
    orderID = int(file.read())
    print('old id:',orderID)


with open('orderID', 'w') as file:
    newid =  orderID+ 2
    print('new id:', newid)
    file.writelines(str(newid))



# Main code

# Create the connection to IBGW with client socket id=123
# ibConnection = Connection.create
# ibgw_conTradeChannel = ibConnection(port=4001,clientId=123)
ibgw_conTradeChannel = Connection.create(port=7497,clientId=100)
ibgw_conTradeChannel.connect()

# Handle Order ID sent by Server
#ibgw_conTradeChannel.register(handle_order_id, 'NextValidId')

# Receive the new OrderID sequence from the IB Server
ibgw_conTradeChannel.reqIds(0)

# Print the new OrderID that was sent by IB
print("This is the new OrderID sent by IB Server:", newid)

print("disconnected", ibgw_conTradeChannel.disconnect())