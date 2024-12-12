#!/usr/bin/env python3

'''
Howto Run:
$ ./date_fix.py -i dmesg -b 1606543024 -t PST -o /tmp/dmesg_date.out

btime=`cat /proc/stat | grep btime | awk '{print $2}'`

<sosreport> $ cat ./proc/stat | grep btime | awk '{print $2}'
1606543024

$ cat dmesg
[918685.152095] clib0: cm send completion: id 162, status: 0
[918685.152614] clib0: sending packet: head 0x4c0ca3 length 319 connection 0x201d
[918685.152640] clib0: cm send completion: id 163, status: 0
[918685.152682] clib0: cm recv completion: id 1521, status: 0

$ ./date_fix.py -i dmesg -b 1606543024 -t PST -o /tmp/dmesg_date.out

$ cat /tmp/dmesg_date.out
[2020-12-08 13:08:29 PST -0800] [918685.152095] clib0: cm send completion: id 162, status: 0
[2020-12-08 13:08:29 PST -0800] [918685.152614] clib0: sending packet: head 0x4c0ca3 length 319 connection 0x201d
[2020-12-08 13:08:29 PST -0800] [918685.152640] clib0: cm send completion: id 163, status: 0
[2020-12-08 13:08:29 PST -0800] [918685.152682] clib0: cm recv completion: id 1521, status: 0
'''

import argparse
from datetime import datetime
import re
import pytz
import sys

timezones = {
	"AEST"	: "Australia/Sydney",
	"IST"	: "Asia/Kolkata",
	"CEST"	: "Europe/Berlin",
	"UTC"	: "UTC",
	"GMT"	: "GMT",
	"EST"	: "America/New_York",
	"PST"	: "America/Los_Angeles",
	"PDT"	: "America/Los_Angeles",
	"AKDT"	: "US/Alaska",
    "JST"   : "Asia/Tokyo",
    "MYT"   : "Asia/Kuala_Lumpur",
}

parser = argparse.ArgumentParser(description='Generate timestamps for dmesg and ftrace logs')
parser.add_argument('-i', '--infile', help='input filename')
parser.add_argument('-b', '--btime', help='boot time of env')
parser.add_argument('-t', '--timezone', help='output timezone')
parser.add_argument('-l', '--list_tzs', help='list currently supported timezones', action="store_true")
parser.add_argument('-o', '--outfile', help='output filename') 
args = parser.parse_args()

orig_stdout = sys.stdout
if args.outfile:
	out_fd = open(args.outfile, "w")
	sys.stdout = out_fd

if args.list_tzs:
	for tz in timezones.keys():
		print("{:<5s} {}".format(tz, timezones[tz]))
	sys.exit()

TZ = "UTC"
if args.timezone:
	if args.timezone in timezones:
		TZ = timezones[args.timezone]
	else:
		print("{} not supported. Switching to UTC".format(args.timezone))

if not args.infile or not args.btime:
	print("missing input file or boot time. Try with -h option")
	sys.exit()

with open(args.infile, "r") as f:
	for line in f.readlines():
		line = line.strip()

		z = re.match(".* (\d+)\.(\d+): (.*)",line) # 1088.495716: <ftrace>
		if not z:
			z = re.match(".(\d+).(\d+). .*", line) #[918685.152095] <dmesg>
		if z:
			secs_4m_epoch = int(args.btime) + int(z.group(1))
			date = datetime.fromtimestamp(secs_4m_epoch, pytz.timezone('UTC'))
			date = date.astimezone(pytz.timezone(TZ))
			date_str = date.strftime("%Y-%m-%d %H:%M:%S %Z %z")
			print("[{}]".format(date_str), end=' ')
		print(line)
	#for line
#with open
