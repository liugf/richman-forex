import logging, oandapy, datetime, message

logger = logging.getLogger()

def create(timestamp, reason = ''):
	oanda = oandapy.API(environment="practice", access_token="90c9fea896069cec944d4b03404a4725-3665345b9d5b4cc4cea8711349587903")
	account_id = 767708

	prices = oanda.get_prices(instruments='XAU_USD')
	xau_price = prices['prices'][0]
	xau_mid_price = (xau_price['ask'] + xau_price['bid']) / 2

	expiry_time = (datetime.datetime.utcnow() + datetime.timedelta(0,300)).isoformat('T')
	upper_order = oanda.create_order(account_id, instrument="XAU_USD", units=1, side="buy", type="stop", price=xau_price['ask']+0.5, expiry=expiry_time, trailingStop=200)
	lower_order = oanda.create_order(account_id, instrument="XAU_USD", units=1, side="sell", type="stop", price=xau_price['bid']-0.5, expiry=expiry_time, trailingStop=200)

	time_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
	msg = 'New order around %.3f; Reason: %s %s' % (xau_mid_price, time_str, reason)
	logger.info(msg)
	message.send(msg)
