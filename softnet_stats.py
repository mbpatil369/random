#!/usr/bin/env python3

'''
[mbpatil@XXXX scripts]$ ./softnet_stats.py
zzz 2023-06-24 11:44:47.929166 file=/proc/net/softnet_stat interval=5
[FIELD           ] TOTAL        CPU:VALUE CPU:VALUE ...
[processed       ] 671664879    0:4647854 1:1609 2:7618393 .. 
..
'''
import argparse
from datetime import datetime
import re
import time

parser = argparse.ArgumentParser(description='Show SOFTNET related stats')
parser.add_argument('-i', '--infile', help='input filename', default='/proc/net/softnet_stat')
parser.add_argument('-t', '--time', help='time between iterations', default='5')
parser.add_argument('-o', '--onetime', help='run for one iteration', action="store_true")
parser.add_argument('-c', '--cpuwise', help='show stats cpuwise', action="store_true")
args = parser.parse_args()

'''
seq_printf(seq,
    "%08x %08x %08x %08x %08x %08x %08x %08x %08x %08x %08x\n",
    sd->processed, sd->dropped, sd->time_squeeze, 0,
    0, 0, 0, 0, /* was fastroute */
    0,   /* was cpu_collision */
    sd->received_rps, flow_limit_count);
'''
FIELDS = {
    'processed' : 0,
    'dropped' : 1,
    'time_squeeze' : 2,
    'received_rps': 9,
    'flow_limit_count': 10
}

prev_stats = {}
def process_line(line, stats, cpu, cpuwise):
    fields = line.split()
    
    for field in FIELDS.keys():
        idx = FIELDS[field]
        cur_value = 0
        try: cur_value = int(fields[idx], 16) #hex to int
        except ValueError: continue
        if not cur_value: continue

        if cpuwise: key = str(cpu) + field
        else: key =  field + str(cpu)
        if key not in prev_stats:
            prev_stats[key] = 0

        value = cur_value - prev_stats[key]
        if not value: continue
        prev_stats[key] = cur_value

        if cpuwise:
            if cpu not in stats:
                stats[cpu] = 0
                stats[key] = 0
            stats[cpu] += value
        else:
            if field not in stats:
                stats[field] = 0
                stats[key] = 0
            stats[field] += value
        #else
        stats[key] = value
#def

def print_stats(stats, cnt_cnt, cpuwise):
    if cpuwise:
        for cpu in range(cpu_cnt):
            if cpu not in stats or not stats[cpu]: continue
            print("{:4} {:<12}".format(cpu, stats[cpu]), end=' ')
            for field in FIELDS.keys():
                key = str(cpu) + field
                if key not in stats or not stats[key]: continue
                print("{}:{}".format(field, stats[key]), end=' ')
            print()
        #for cpu
    else:
        for field in FIELDS.keys():
            if field not in stats or not stats[field]: continue
            print("[{:<16}] {:<12}".format(field, stats[field]), end=' ')
            for cpu in range(cpu_cnt):
                key = field + str(cpu)
                if key not in stats or not stats[key]: continue
                print("{}:{}".format(cpu, stats[key]), end=' ')
            print()
        #for field
#def

while True:
    now = datetime.now()
    print("zzz {} file={} interval={}".format(now, args.infile, args.time))

    if args.cpuwise:
        print("{:4} {:<12} {}:{} {}:{} ...".format("CPU", "TOTAL", "FIELD", "VALUE", "FIELD", "VALUE"))
    else:
        print("[{:<16}] {:<12} {}:{} {}:{} ...".format("FIELD", "TOTAL", "CPU", "VALUE", "CPU", "VALUE"))

    stats = {}
    cpu_cnt = 0
    with open(args.infile, "r") as f:
        cpu = 0
        for line in f.readlines():
            line = line.strip()

            z = re.match("[0-9a-f]+.*", line)
            if not z:
                continue

            #matches
            process_line(line, stats, cpu_cnt, args.cpuwise)
            cpu += 1
            cpu_cnt = max(cpu_cnt, cpu)
        #for line
    #with open

    print_stats(stats, cpu_cnt, args.cpuwise)
    print()

    if args.onetime: break
    time.sleep(int(args.time))
#while True
