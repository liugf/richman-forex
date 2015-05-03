# encoding: utf-8
#!/usr/bin/python

import sys, sqlite3, datetime, requests, json

conn = sqlite3.connect('../var/database.db')
cursor = conn.cursor()

start_time = datetime.datetime.utcnow();
end_time = start_time + datetime.timedelta(8) # 八天后

start_str = start_time.strftime('%Y-%m-%d')
end_str = end_time.strftime('%Y-%m-%d')

base_url = 'http://api.markets.wallstreetcn.com/v1/calendar.json'

client = requests.Session();
args = {'params':{'start':start_str, 'end':end_str}}

response = client.get(base_url, **args)
content = response.content.decode('utf-8')
content = json.loads(content)

if not content['count']:
	sys.exit(0)

events = content['results']

for event in events:
	sql = '''INSERT INTO events (timestamp, local_time, importance, tilte, previous, revised, forecast, \
	actual, country, currency, data_name, event_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	'''
	cursor.execute(sql, (event['timestamp'], event['localDateTime'], event['importance'], event['title'], 
					event['previous'], event['revised'], event['forecast'], event['actual'], 
					event['country'], event['currency'], event['event_attr_id'], event['calendarType']))

print 'insert %d events' % content['count']

conn.commit()
conn.close()