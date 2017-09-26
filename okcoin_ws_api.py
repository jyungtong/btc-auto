"""
Okcoin API function
"""
def buildMySign(params,secretKey):
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) +'&'
    return  hashlib.md5((sign+'secret_key='+secretKey).encode("utf-8")).hexdigest().upper()

# retrieve user info
def userInfo(api_key, secretkey):
    channel = 'ok_spotcny_userinfo'
    params={
      'api_key': api_key
    }

    sign = buildMySign(params,secretkey)
    finalStr =  "{'event':'addChannel','channel':'"+channel+"','parameters':{'api_key':'"+api_key+"',\
                'sign':'"+sign+"'}}"
    return finalStr

# retrieve order info
def orderInfo(api_key, secretkey, order_id='', symbol='btc_cny'):
    channel = 'ok_spotcny_orderinfo'
    params = {
      'api_key': api_key,
      'symbol': symbol
    }

    if order_id:
        params['order_id'] = order_id
    sign = buildMySign(params,secretkey)
    finalStr =  "{'event':'addChannel','channel':'"+channel+"','parameters':{'api_key':'"+api_key+"',\
                'sign':'"+sign+"',\
                'symbol':'"+symbol+"',\
                'order_id':'"+order_id+"'}}"
    return finalStr
"""
End Okcoin API function
"""
