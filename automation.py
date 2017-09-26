import util

# Mock test value
cash_bal = 10000.00
btc_bal = 0.00

# Trading constant
PRICE_HISTORY_LEN = 20
MA_SIZE_5 = 5
MA_SIZE_20 = 20
WS_LIMIT = 5 # 5secs rate limit for websocket
RISK = 0.00008 # RISK THRESHOLD
CALLBACK = 1.0000205
MA_TOUCH = 1.00006
CAPITAL = 10000.00

# Trading variable
buy_sell_state = 'buy'
market_price = -1
highest_market_price = -1
lowest_market_price = -1
highest_ma_5 = -1
lowest_ma_5 = -1
last_buy_price = 0.0
last_sell_price = 0.0
last_rec_time = 0

price_rec = []
moving_avg_5 = []
moving_avg_20 = []
price_pointer = 0

# print accout balance
def printBal():
    asset = cash_bal + (btc_bal*market_price)
    print 'Rate: %f/B, Cash: $ %f, BTC: B %f, Total Assets: $ %f'%(market_price, cash_bal, btc_bal, asset)
    print ''

def buy(rate, amount):
    btc_amount = int(amount/rate*100)/100.00 # to round down for all amount
    final_buy_price = btc_amount*rate
    if cash_bal >= final_buy_price:
        setAccountBalance(cash_bal - final_buy_price, btc_bal + btc_amount)
        print 'Bought %f B at %f'%(btc_amount, rate)
    else:
        print 'Insufficient amount of cash balance'

def sell(rate, amount):
    sell_price = rate*amount
    if btc_bal >= amount:
        setAccountBalance(cash_bal + sell_price, btc_bal - amount)
        print 'Sold %f B at %f'%(amount, rate)
    else:
        print 'Insufficient amount of BTC balance'

# trade function
def tradeNow(rate, amount, trade_type='buy'):
    options = {
        'buy': buy,
        'sell': sell
    }

    options[trade_type](rate, amount)

# alter account balance
def setAccountBalance(cash, btc):
    global cash_bal
    global btc_bal
    cash_bal, btc_bal = cash, btc

# feeding data
def feedData(new_price):
    global price_rec
    global moving_avg_5
    global moving_avg_20

    # feed data into price records
    if len(price_rec) < PRICE_HISTORY_LEN:
        progress = float(len(price_rec))/PRICE_HISTORY_LEN * 100
        if progress % 10 == 0:
            print 'feeding data...%d%%'%(progress)

        price_rec.append(new_price)

        # once done feeding generate all moving average
        if len(price_rec) >= PRICE_HISTORY_LEN:
            for index,value in enumerate(price_rec):
                ma5 = util.calcMovAvg(price_rec, MA_SIZE_5, index)
                ma20 = util.calcMovAvg(price_rec, MA_SIZE_20, index)
                moving_avg_5.append(ma5)
                moving_avg_20.append(ma20)
    else: # loop feeding data
        ma5 = util.calcMovAvg(price_rec, MA_SIZE_5, price_pointer)
        ma20 = util.calcMovAvg(price_rec, MA_SIZE_20, price_pointer)
        price_rec[price_pointer] = new_price
        moving_avg_5[price_pointer] = ma5
        moving_avg_20[price_pointer] = ma20

# move price pointer forward
def movePointer():
    global price_pointer
    price_pointer += 1 # move pointer forward after recorded latest price
    if price_pointer >= PRICE_HISTORY_LEN:
        price_pointer = 0 # reset pointer to head again

# record lowest and highest price
def recordLowHighPoint(new_price):
    global lowest_market_price
    global highest_market_price
    global lowest_ma_5
    global highest_ma_5

    if lowest_market_price < 0 or lowest_market_price > new_price:
        lowest_market_price = new_price

    if highest_market_price < 0 or highest_market_price < new_price:
        highest_market_price = new_price

    new_ma_5 = moving_avg_5[price_pointer]
    if lowest_ma_5 < 0 or lowest_ma_5 > new_ma_5:
        lowest_ma_5 = new_ma_5

    if highest_ma_5 < 0 or highest_ma_5 < new_ma_5:
        highest_ma_5 = new_ma_5

# feed real time data
def load(data):
    global market_price
    new_price = float(data['last'])

    # feed data at init
    if len(price_rec) < PRICE_HISTORY_LEN:
        feedData(new_price)
    else:
        feedData(new_price)
        buySellDecision(new_price)
        # recordLowHighPoint(new_price)
        movePointer()
        print new_price

    market_price = new_price

# buy rule
def isBuyRuleSatisfy():
    prev_price = price_rec[price_pointer-1]
    current_price = price_rec[price_pointer]
    prev_ma5_price = moving_avg_5[price_pointer-1]
    ma5_price = moving_avg_5[price_pointer]
    ma20_price = moving_avg_20[price_pointer]

    # check if MA5 is declining
    # and almost nearly hit the MA20
    if ma5_price < prev_ma5_price \
    and ma5_price <= ma20_price*MA_TOUCH:
        return False

    if current_price > ma5_price:
        print 'because: current price is higher than ma5'
        return True

    # if there is callback in MA5
    if ma5_price >= prev_ma5_price*CALLBACK \
    and ma5_price > prev_ma5_price:
        print 'because: callback in ma5'
        return True

    return False

# sell rule
def isSellRuleSatisfy():
    prev_price = price_rec[price_pointer-1]
    current_price = price_rec[price_pointer]
    prev_ma5_price = moving_avg_5[price_pointer-1]
    ma5_price = moving_avg_5[price_pointer]
    ma20_price = moving_avg_20[price_pointer]

    # first to check stop loss
    # if current price is lower than last buy price
    if current_price <= last_buy_price*(1-RISK):
        print 'because of stop loss'
        return True

    # check if MA5 is declining
    # and almost nearly hit the MA20
    if ma5_price < prev_ma5_price \
    and ma5_price <= ma20_price*MA_TOUCH:
        print 'because of ma5 almost hit ma20'
        return True

    # check if current price is lower than MA5
    if current_price <= ma5_price:
        print 'because of current price is lower than ma5'
        return True

    # check if current price has sharp drop compared to previous price
    if prev_price*(1-RISK) >= current_price:
        print 'because of sharp drop'
        return True

    return False

# buy/sell algorithm here
def buySellDecision(new_price):
    global buy_sell_state
    global last_buy_price
    global last_sell_price

    # print 'new_price: %f, market_price: %f, market_price_callback: %f'%(new_price, market_price, market_price*CALLBACK)
    # print ''

    # decide whether this trade is sell or buy
    if buy_sell_state == 'buy':
        if isBuyRuleSatisfy():
            tradeNow(new_price, CAPITAL if cash_bal >= CAPITAL else cash_bal, 'buy')
            buy_sell_state = 'sell'
            last_buy_price = new_price
            printBal()

    elif buy_sell_state == 'sell':
        if isSellRuleSatisfy():
            tradeNow(new_price, btc_bal, 'sell')
            buy_sell_state = 'buy'
            last_sell_price = new_price
            printBal()

    # default action by setting latest market price
    market_price = new_price

