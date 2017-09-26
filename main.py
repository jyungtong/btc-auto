import automation as auto
import okcoin_ws_api as api
import hashlib
import json
import random
import requests
import websocket
from datetime import datetime

# API Key
api_key = 'YOUR_API_KEY'
secret_key = 'YOUR_SECRET_KEY'

# REST URL
ROOT_URL = 'https://www.okcoin.cn/api/v1'
TICKER = ROOT_URL + '/ticker.do'
ORDER_HISTORY = ROOT_URL + '/order_history.do'

# WebSocket
WSS_ROOT = 'wss://real.okcoin.cn:10440/websocket/okcoinapi'

"""
Websocket function
"""
def on_message(ws, message):
    data = json.loads(message)[0]['data']
    auto.load(data)

    last_rec_time = nowTs
    # nowTs = int(data['timestamp'])/1000

        # ma5 = calcMovAvg(price_rec, MA_SIZE_5, price_pointer)
        # ma20 = calcMovAvg(price_rec, MA_SIZE_20, price_pointer)
        # print '%.3f\t%.3f'%(ma5,ma20)

    # init with latest market price
    # if market_price < 0:

    # if nowTs - last_rec_time > WS_LIMIT:
    # buySellDecision(new_price)

def on_error(ws, error):
    print error

def on_close(ws):
    auto.printBal()

def on_open(ws):
    #subscribe okcoin.com spot ticker
    ws.send("{'event':'addChannel','channel':'ok_sub_spotcny_btc_ticker'}")

    # ws.send(userInfo(api_key, secret_key))
    # pass
"""
End Websocket function
"""


if __name__ == '__main__':
    # testTrade()
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(WSS_ROOT,
            on_message = on_message,
            on_error = on_error,
            on_close = on_close)

    ws.on_open = on_open
    ws.run_forever()
