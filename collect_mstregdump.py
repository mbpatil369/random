#!/usr/bin/env python3

import argparse
from datetime import datetime
import os
import re
import subprocess
import sys
import time

parser = argparse.ArgumentParser(description='Collect 3 mstregdumps before and after an issue')
parser.add_argument('-p', '--pattern', help='pattern to search for issue occurence', required=True)
parser.add_argument('-l', '--logfile', help='logfile to search for pattern. Default is /var/log/messages', default='/var/log/messages')
parser.add_argument('-i', '--interval', help='interval between data collection', default='5')
parser.add_argument('-o', '--outdir', help='output directory for data collection', default='/tmp/mstregdumps')
parser.add_argument('-m', '--maxcount', help='collect data for maxcount occurences', default='1')
args = parser.parse_args()


def run_command(cmd):
	command = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	stdout, stderr = command.communicate()
	if (sys.version_info[0] == 3):
		stdout = stdout.decode("utf-8", 'ignore').strip()
	return stdout.strip()
#def run_command

date = datetime.now().strftime("%Y%m%d_%H%M%S")

#get devices
cmd = "lspci | grep -i mell | grep -iv virtual | cut -f 1 -d \ "
devices = run_command(cmd).split("\n")

print("zzz {}".format(date))
print("Devices={} interval={} outdir={}".format(devices, args.interval, args.outdir))
print("logfile={} pattern='{}' maxcount={}".format(args.logfile, args.pattern, args.maxcount))

if os.path.exists(args.outdir):
	os.rename(args.outdir, args.outdir + "_" + date)
os.mkdir(args.outdir)

def collect_mstregdump(suffix):
	date = datetime.now().strftime("%Y%m%d_%H%M%S")
	for dev in devices:
		if dev not in files_dict: files_dict[dev] = []
		files = files_dict[dev]

		#3 mstregdumps back to back
		for i in range(3):
			filename = "{}/mstregdump_{}_{}_{}{}".format(args.outdir, dev, date, suffix, i)
			cmd = "mstregdump {} > {}".format(dev, filename)
			run_command(cmd)
			files.append(filename)
		#for

		#keep last 6 files - 3 before and 3 after
		for filename in files[:-6]:
			os.remove(filename)

		#print("dev={} files={}".format(dev, files))
	#for dev
#def collect_mstregdump

def pattern_cnt():
	cmd = "grep -cE '{}' {}".format(args.pattern, args.logfile)
	return run_command(cmd)
#def

#main
files_dict = {}
init_cnt = pattern_cnt()
maxcount = int(args.maxcount)
while True:
	collect_mstregdump("before")
	time.sleep(int(args.interval))

	cnt = pattern_cnt()
	if cnt > init_cnt:
		print("{}: '{}' found in {}. init_cnt={} cnt={}".format(
			datetime.now(), args.pattern, args.logfile, init_cnt, cnt))
		collect_mstregdump("after")

		maxcount -= 1
		if maxcount:
			print("collecting data for next occurence of issue[{}]".format(int(args.maxcount)-maxcount+1))
			files_dict = {}
			init_cnt = pattern_cnt()
			continue
		break
	#if cnt
#while

print("collected data for {} occurences[outdir={}]".format(args.maxcount, args.outdir))
