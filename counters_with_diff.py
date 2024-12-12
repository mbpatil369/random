#!/usr/bin/python

USAGE = '''
Usage:
[mbpatil@XXXX RDSinfo.ExaWatcher]$  ~/scripts/counters_with_diff.py "grep ib_rdma_mr_8k_pool_flush *RDSinfo*dat"
        ib_rdma_mr_8k_pool_flush          5103610 [Diff    5103610 ]
        ib_rdma_mr_8k_pool_flush          5104175 [Diff        565 ]
        ib_rdma_mr_8k_pool_flush          5105019 [Diff        844 ]
        ib_rdma_mr_8k_pool_flush          5105792 [Diff        773 ]
        ib_rdma_mr_8k_pool_flush          5106572 [Diff        780 ]
'''
import commands, re, sys

if len(sys.argv) < 2:
	print USAGE
	sys.exit(0)

CMD = sys.argv[1]
prev_stats = {}
for line in commands.getoutput(CMD).split("\n"):
	print line,
	z = re.match("(\w+)\s+(\d+)",line.strip())
	if z:
		typ, cur = z.group(1), int(z.group(2))
		if typ not in prev_stats:
			prev_stats[typ] = 0

		value = cur - prev_stats[typ];
		print ("[Diff %10d %6d]")%(value, value/(1024*1024))
		prev_stats[typ] = cur
	else:
		print
#for
