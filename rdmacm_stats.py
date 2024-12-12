#!/usr/bin/env python3

'''
How to run:
[root@XXXX scripts]# ./rdmacm_stats.py -h
usage: rdmacm_stats.py [-h] [-i INTERVAL] [-d DEVICES [DEVICES ...]]
		       [-p PORTS [PORTS ...]] [-s STATS [STATS ...]] [-D] [-l]
		       [-e EXPRESSION]

Show rdma cm stats

optional arguments:
  -h, --help	    show this help message and exit
  -i INTERVAL, --interval INTERVAL
			interval between iterations
  -d DEVICES [DEVICES ...], --devices DEVICES [DEVICES ...]
			space separated device names (mlx5_0 mlx5_1)
  -p PORTS [PORTS ...], --ports PORTS [PORTS ...]
			space separated HCA ports (1 2)
  -s STATS [STATS ...], --stats STATS [STATS ...]
			space separated stats
  -D, --diffs	   show counter difference with previous value
  -l, --list_stats      show available devices, ports and counters
  -e EXPRESSION, --expression EXPRESSION
			Regular expression of pattern to be searched in path

Example:
[root@XXXX scripts]# ./rdmacm_stats.py -d mlx5_0 -p 1 -i 5 -s req rep rtu dreq drep -D
zzz - Wed May  8 16:44:15 PDT 2024 interval=5 secs
--count=1--
mlx5_0_1_rx_drep        :18          [0]
mlx5_0_1_tx_drep        :10          [0]
mlx5_0_1_rx_dreq        :10          [0]
mlx5_0_1_tx_dreq        :18          [0]
mlx5_0_1_rx_rep         :7           [0]
mlx5_0_1_tx_rep         :38          [0]
mlx5_0_1_rx_req         :283493      [0]
mlx5_0_1_tx_req         :286437      [0]
mlx5_0_1_rx_rtu         :38          [0]
mlx5_0_1_tx_rtu         :6           [0]
--count=2--
mlx5_0_1_rx_drep        :18          [0]
mlx5_0_1_tx_drep        :10          [0]
mlx5_0_1_rx_dreq        :10          [0]
mlx5_0_1_tx_dreq        :18          [0]
mlx5_0_1_rx_rep         :7           [0]
mlx5_0_1_tx_rep         :38          [0]
mlx5_0_1_rx_req         :283494      [1]
mlx5_0_1_tx_req         :286437      [0]
mlx5_0_1_rx_rtu         :38          [0]
mlx5_0_1_tx_rtu         :6           [0]
'''

import argparse
from datetime import datetime
import re
import time
import subprocess

parser = argparse.ArgumentParser(description='Show rdma cm stats')
parser.add_argument('-i', '--interval', help='interval between iterations', default=5)
parser.add_argument('-d', '--devices', help='space separated device names (mlx5_0 mlx5_1)', nargs='+')
parser.add_argument('-p', '--ports', help='space separated HCA ports (1 2)', nargs='+')
parser.add_argument('-s', '--stats', help='space separated stats', nargs='+')
parser.add_argument('-D', '--diffs', help='show counter difference with previous value', action="store_true")
parser.add_argument('-l', '--list_stats', help='show available devices, ports and counters', action="store_true")
parser.add_argument('-e', '--expression', help='Regular expression of pattern to be searched in path')
args = parser.parse_args()

paths = subprocess.Popen('find /sys/devices/ -iname cm_[tr]x_msgs', stdout=subprocess.PIPE, shell=True)
paths = paths.stdout.read().decode('utf-8').split('\n')

devices = {}
for path in paths:
	pat = "/sys/devices/.*/(mlx\d+_\d+)/ports/(\d+)/cm_([tr]x)_msgs"
	z = re.match(pat, path)
	if z:
		device = z.group(1)
		port = z.group(2)
		rx_tx = z.group(3)

		if device not in devices: devices[device] = {}
		if port not in devices[device]: devices[device][port] = {}
		if rx_tx not in devices[device][port]: devices[device][port][rx_tx] = []
		devices[device][port][rx_tx].append(path)
#for path

stats = subprocess.Popen("ls " + paths[0], stdout=subprocess.PIPE, shell=True)
stats = stats.stdout.read().decode('utf-8').split()

if args.list_stats:
	print("Avialable device, port and stats")
	for device in devices.keys():
		for port in devices[device].keys():
			print("device={:8} port={:4}".format(device, port))
		#for port
	#for device

	print("stats={}".format(" ".join(stats)))
	exit(0)
#if args.list_stats

prev_counters = {}
def process_stat(device, port, stat):
	for rx_tx in devices[device][port].keys():
		for path in devices[device][port][rx_tx]:
			path = path + "/" + stat
			if args.expression and not re.search(args.expression, path): continue;

			counter = subprocess.Popen("cat " + path, stdout=subprocess.PIPE, shell=True)
			counter = int(counter.stdout.read().decode('utf-8').split()[0])
			counter_name = "{}_{}_{}_{}".format(device, port, rx_tx, stat)
			print("{:24}:{:<12}".format(counter_name, counter), end='')

			if args.diffs:
				if path not in prev_counters: prev_counters[path] = counter
				print("[{}]".format(counter-prev_counters[path]), end=''),
				prev_counters[path] = counter
			print()
		#for path
	#for rx_tx
#def process_stat(device, port, stat):

def print_date():
	date = subprocess.Popen('date', stdout=subprocess.PIPE, shell=True)
	date = date.stdout.read().decode('utf-8').strip()
	print("zzz - {} interval={} secs".format(date, args.interval))
#def print_date

print_date()
count = 1
while True:
	print("--count={}--".format(count))
	for device in devices.keys():
		if args.devices and device not in args.devices: continue
		for port in devices[device].keys():
			if args.ports and port not in args.ports: continue
			for stat in stats:
				if args.stats and stat not in args.stats: continue
				process_stat(device, port, stat)
			#for stats
		#for port
	#for device

	count += 1
	time.sleep(int(args.interval))
#while True
