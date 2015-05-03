CREATE TABLE `events` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `timestamp` int(11) NOT NULL,
  `local_time` varchar(255) NOT NULL DEFAULT '',
  `importance` int(11) NOT NULL,
  `tilte` varchar(255) NOT NULL DEFAULT '',
  `previous` float DEFAULT '0',
  `revised` float DEFAULT '0',
  `forecast` float DEFAULT '0',
  `actual` float DEFAULT '0',
  `country` varchar(255) NOT NULL DEFAULT '',
  `currency` varchar(255) NOT NULL DEFAULT '',
  `data_name` varchar(255) DEFAULT '',
  `event_type` varchar(255) NOT NULL
);

CREATE INDEX timestamp_idx ON `events` (`timestamp`);