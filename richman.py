# encoding: utf-8
#!/usr/bin/python

import sys, sqlite3, datetime, time, order
from threading import Timer

'''循环获取最新的事件，设置定时任务'''

reload(sys)
sys.setdefaultencoding('utf-8')

last_event_time = 0;

while True:
	now = datetime.datetime.utcnow()
	start = time.mktime(now.timetuple())
	end = time.mktime((now + datetime.timedelta(0, 3600*5)).timetuple())

	conn = sqlite3.connect('./var/database.db')
	conn.row_factory = sqlite3.Row
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM events WHERE importance >=2 and currency="USD" and timestamp >= ? and timestamp < ? order by timestamp asc', (start, end))
	events = cursor.fetchall()
	conn.close()

	for event in events:
		if event['timestamp'] < last_event_time + 300:
			continue

		last_event_time = event['timestamp']
		time_diff = event['timestamp'] - time.mktime(datetime.datetime.utcnow().timetuple())
		Timer(time_diff-60, order.create, (event['timestamp'], event['title'])).start()

	print 'MainThead going to sleep'
	sys.stdout.flush()
	time.sleep(3599*3) # 约停止3小时
	print 'MainThead wake up'
