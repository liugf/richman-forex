# encoding: utf-8
#!/usr/bin/python

import sys, sqlite3, datetime, requests, json, time

print '---start---'

conn = sqlite3.connect('../var/database.db')
cursor = conn.cursor()

start_day = datetime.date.today();
end_day = start_day + datetime.timedelta(8) # 八天后

start_str = start_day.strftime('%Y-%m-%d')
end_str = end_day.strftime('%Y-%m-%d')

print 'From %s To %s' % (start_str, end_str)

base_url = 'http://api.markets.wallstreetcn.com/v1/calendar.json'

client = requests.Session();
args = {'params':{'start':start_str, 'end':end_str}}

response = client.get(base_url, **args)
content = response.content.decode('utf-8')
content = json.loads(content)

if not content['count']:
	sys.exit(0)

cursor.execute('delete from events where timestamp >= ? and timestamp < ?', 
	(time.mktime(start_day.timetuple()), time.mktime((end_day+ datetime.timedelta(1)).timetuple())))

events = content['results']

for event in events:
	sql = '''INSERT INTO events (timestamp, local_time, importance, title, previous, revised, forecast, \
	actual, country, currency, event_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
	'''
	cursor.execute(sql, (event['timestamp'], event['localDateTime'], event['importance'], event['title'], 
		event['previous'], event['revised'], event['forecast'], event['actual'], 
		event['country'], event['currency'], event['calendarType']))

print 'insert %d events' % len(events)

conn.commit()
conn.close()

print '---end---'