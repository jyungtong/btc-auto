def testTrade():
    rate = 4000
    print_bal(rate)

    tradeNow(rate, 1, 'buy')
    print_bal(rate)

    rate = 4020
    tradeNow(rate, 0.5, 'sell')
    print_bal(rate)

    rate = 3980
    tradeNow(rate, 2, 'buy')
    print_bal(rate)

    rate = 4000
    tradeNow(rate, 2, 'sell')
    print_bal(rate)
