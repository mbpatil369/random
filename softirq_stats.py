#!/usr/bin/env python3

'''
[mbpatil@XXXX scripts]$ ./softirq_stats.py -e NET                                                                 
zzz 2023-06-24 10:26:47.817983 file=/proc/softirqs interval=5
[SIRQ_NAME       ] TOTAL        CPU:SIRQs CPU:SIRQs ...
[NET_TX:         ] 360035098    1:1129755 2:73465281 3:1855686 4:4686628 
...
'''
import argparse
from datetime import datetime
import re
import time

parser = argparse.ArgumentParser(description='Show SOFTIRQ related stats')
parser.add_argument('-i', '--infile', help='input filename', default='/proc/softirqs')
parser.add_argument('-t', '--time', help='time between iterations', default='5')
parser.add_argument('-o', '--onetime', help='run for one iteration', action="store_true")
parser.add_argument('-c', '--cpuwise', help='show stats cpuwise', action="store_true")
parser.add_argument('-e', '--expression', help='Regular expression of pattern')
args = parser.parse_args()

prev_stats = {}
def process_line(line):
    fields = line.split()
    sirq_name = fields[0]

    total = 0
    cpu_values = {}
    for cpu in range(len(fields)):
        sirqs = 0
        try: sirqs = int(fields[cpu])
        except ValueError: continue
        if not sirqs: continue

        key =  sirq_name+ str(cpu)
        if key not in prev_stats:
            prev_stats[key] = 0

        value = sirqs - prev_stats[key]
        if not value: continue
        prev_stats[key] = sirqs

        if cpu not in cpu_values:
           cpu_values[cpu] = 0
        cpu_values[cpu] = value
        total += value
    #for cpu

    if total:
        print("[{:<16}] {:<12}".format(sirq_name[:16], total), end=' ')
        for cpu in cpu_values.keys():
            print("{}:{}".format(cpu, cpu_values[cpu]), end=' ')
        print()
#def

def process_line_cpuwise(line, cpustats):
    fields = line.split()
    sirq_name = fields[0]

    for cpu in range(len(fields)):
        sirqs = 0
        try: sirqs = int(fields[cpu])
        except ValueError: continue
        if not sirqs: continue

        if cpu not in cpu_stats:
            cpu_stats[cpu] = {}
            cpu_stats[cpu]["total"] = 0

        cpu_stat = cpu_stats[cpu]
        key = str(cpu) + sirq_name
        if key not in prev_stats:
            prev_stats[key] = 0

        value = sirqs - prev_stats[key]
        if not value: continue
        prev_stats[key] = sirqs

        if sirq_name not in cpu_stat:
           cpu_stat[sirq_name] = 0
        cpu_stat[sirq_name] = value
        cpu_stat["total"] += value
    #for cpu
#def

while True:
    now = datetime.now()
    print("zzz {} file={} interval={}".format(now, args.infile, args.time))

    if args.cpuwise:
        print("{:4} {:<12} {}:{} {}:{} ...".format("CPU", "TOTAL", "SIRQ", "SIRQs", "SIRQN", "SIRQs"))
    else:
        print("[{:<16}] {:<12} {}:{} {}:{} ...".format("SIRQ_NAME", "TOTAL", "CPU", "SIRQs", "CPU", "SIRQs"))

    cpu_stats = {}
    with open(args.infile, "r") as f:
        for line in f.readlines():
            line = line.strip()

            #skip lines not contianing patten/expression
            if args.expression:
                if not re.search(args.expression, line):
                    continue

            z = re.match("\.*\w+:.*", line)
            if not z:
                continue

            #matches
            if args.cpuwise: process_line_cpuwise(line, cpu_stats)
            else: process_line(line)
        #for line
    #with open

    if args.cpuwise:
        for cpu in cpu_stats.keys():
            cpu_stat = cpu_stats[cpu]
            if not cpu_stat["total"]: continue
            print("{:<4} {:<12}".format(cpu, cpu_stat["total"]), end=' ')
            for sirq_name in cpu_stat.keys():
                if not cpu_stat[sirq_name] or sirq_name == "total": continue
                print("{}{}".format(sirq_name, cpu_stat[sirq_name]), end=' ') 
            print() 
        #for cpu
    #if arg.cpuwise
    print()

    if args.onetime: break
    time.sleep(int(args.time))
#while True
