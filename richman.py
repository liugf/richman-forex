# encoding: utf-8
#!/usr/bin/python

import sys, logging, sqlite3, datetime, time, order
from threading import Timer

'''循环获取最新的事件，设置定时任务'''

reload(sys)
sys.setdefaultencoding('utf-8')

# 创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('var/richman.log')
fh.setLevel(logging.DEBUG)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter('[%(levelname)s] %(asctime)s  %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)


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

	logger.info('MainThead going to sleep')
	sys.stdout.flush()
	time.sleep(3599*3) # 约停止3小时
	logger.info('MainThead wake up')
