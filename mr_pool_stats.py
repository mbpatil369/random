#!/usr/bin/python

'''
Usage: mr_pool_stats.py <interval-in-secs> <max-loops>
sample run
'''

import commands, time, re, sys

INTERVAL = 1 #seconds
MAXLOOPS = 10

if len(sys.argv) == 3:
	INTERVAL = int(sys.argv[1])
	MAXLOOPS = int(sys.argv[2])
elif len(sys.argv) == 2:
	INTERVAL = int(sys.argv[1])

date = commands.getoutput('date').split("\n")
print("zzz - %s INTERVAL=%d secs MAXLOOPS=%d")%(date, INTERVAL, MAXLOOPS)

loop = 0;
prev_stats = {}
while True:
	if loop % 100 == 0: # print header once in a while
		print("%-8s %-10s %-10s %-10s %-10s %-10s %-10s %-10s %-10s %-10s %-10s %-10s %-10s ")%\
			("Time", "8k_alloc", "free", "used", "pl_flush", "pl_wait", "pl_dpltd",\
			"1M_alloc", "free", "used", "pl_flush", "pl_wait", "pl_dpltd");

	loop += 1
	now = commands.getoutput('date +%H%M%S').split("\n")
	print("%s :")%now[0],
	for line in commands.getoutput('rds-info -c | grep ib_rdma_mr').split("\n"):
		z = re.match("(\w+)\s+(\d+)", line.strip())
		if z:
			typ, cur = z.group(1), int(z.group(2))
			if typ not in prev_stats:
				prev_stats[typ] = 0
			
			print ("%-10d")%(cur - prev_stats[typ]),
			prev_stats[typ] = cur
		#if z
	#for line

	print("")
	if MAXLOOPS != -1 and loop >= MAXLOOPS:
		break

	time.sleep(INTERVAL);
#while
