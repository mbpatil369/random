#!/usr/bin/env python3

'''
[mbpatil@XXXX scripts]$ ./irq_stats.py
zzz 2023-06-22 20:03:42.796901 file=/proc/interrupts interval=5
IRQN [IRQ_NAME        ] TOTAL        CPU:IRQs CPU:IRQs ...
0:   [timer           ] 28           0:28
1:   [i8042           ] 9            4:9
4:   [ttyS0           ] 693          6:693
...
'''
import argparse
from datetime import datetime
import re
import time

parser = argparse.ArgumentParser(description='Show IRQ related stats')
parser.add_argument('-i', '--infile', help='input filename', default='/proc/interrupts')
parser.add_argument('-t', '--time', help='time between iterations', default='5')
parser.add_argument('-I', '--irq', help='space separated irq numbers to filter the output', nargs='+')
parser.add_argument('-C', '--cpu', help='space separated cpu numbers to filter the output', nargs='+')
parser.add_argument('-o', '--onetime', help='run for one iteration', action="store_true")
parser.add_argument('-c', '--cpuwise', help='show stats cpuwise', action="store_true")
parser.add_argument('-e', '--expression', help='Regular expression of pattern')
args = parser.parse_args()

prev_stats = {}
def process_line(line):
    fields = line.split()
    irqn = fields[0]
    irq_name = fields[-1]

    if args.irq and irqn.split(":")[0] not in args.irq:
        return

    fields = fields[1:-3] # get rid first and last two fields
    total = 0
    cpu_values = {}
    for cpu in range(len(fields)):
        if args.cpu and str(cpu) not in args.cpu:
            continue

        irqs = 0
        try: irqs = int(fields[cpu])
        except ValueError: continue
        if not irqs: continue

        key = irqn + str(cpu)
        if key not in prev_stats:
            prev_stats[key] = 0

        value = irqs - prev_stats[key]
        if not value: continue
        prev_stats[key] = irqs

        if cpu not in cpu_values:
           cpu_values[cpu] = 0
        cpu_values[cpu] = value
        total += value
    #for cpu

    if total:
        print("{:4} [{:<16}] {:<12}".format(irqn, irq_name[:16], total), end=' ')
        for cpu in cpu_values.keys():
            print("{}:{}".format(cpu, cpu_values[cpu]), end=' ')
        print()
#def

def process_line_cpuwise(line, cpustats):
    fields = line.split()
    irqn = fields[0]
    irq_name = fields[-1]

    if args.irq and args.irq != irqn.split(":")[0]:
        return

    fields = fields[1:-3] # get rid first and last two fields
    for cpu in range(len(fields)):
        if args.cpu and int(args.cpu) != cpu:
            continue

        irqs = 0
        try: irqs = int(fields[cpu])
        except ValueError: continue
        if not irqs: continue

        if cpu not in cpu_stats:
            cpu_stats[cpu] = {}
            cpu_stats[cpu]["total"] = 0

        cpu_stat = cpu_stats[cpu]
        key = str(cpu) + irqn
        if key not in prev_stats:
            prev_stats[key] = 0

        value = irqs - prev_stats[key]
        if not value: continue
        prev_stats[key] = irqs

        if irqn not in cpu_stat:
           cpu_stat[irqn] = 0
        cpu_stat[irqn] = value
        cpu_stat["total"] += value
    #for cpu

#def

while True:
    now = datetime.now()
    print("zzz {} file={} interval={}".format(now, args.infile, args.time))
    if args.cpuwise:
        print("{:4} {:<12} {}:{} {}:{} ...".format("CPU", "TOTAL", "IRQN", "IRQs", "IRQN", "IRQs"))
    else:
        print("{:4} [{:<16}] {:<12} {}:{} {}:{} ...".format("IRQN", "IRQ_NAME", "TOTAL", "CPU", "IRQs", "CPU", "IRQs"))
    cpu_stats = {}
    with open(args.infile, "r") as f:
        for line in f.readlines():
            line = line.strip()

            #skip lines not contianing patten/expression
            if args.expression:
                if not re.search(args.expression, line):
                    continue

            z = re.match("(\d+):.*", line)
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
            for irqn in cpu_stat.keys():
                if not cpu_stat[irqn] or irqn == "total": continue
                print("{}{}".format(irqn, cpu_stat[irqn]), end=' ') 
            print() 
        #for cpu
    #if arg.cpuwise
    print()

    if args.onetime: break
    time.sleep(int(args.time))
#while True
