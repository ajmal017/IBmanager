
import config

from twilio.rest import Client


account_sid = config.twilio_cred['sid']
auth_token = config.twilio_cred['token']
client = Client(account_sid, auth_token)


def send(msg):
    message = client.messages.create(
                                  body=msg,
                                  from_='+441692252050',
                                  to=str(config.uk_number)
                              )

import controll


def send_msg_if_noconn(live):
    msg = 'Connection to IBGW Failed'
    if controll.isConn(4001) == False:
        if live ==True:
            send(msg)
        else: print(msg)
    else:
        pass



if __name__ == '__main__':
    send_msg_if_noconn(True)

    pass