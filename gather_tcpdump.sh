#! /bin/sh

MSGFILE='/var/log/messages'
SEARCH_FORMAT1='not responding, still trying'
SEARCH_FORMAT2='xs_tcp_setup_socket: connect returned unhandled error -107'
NFSPORT=2049
NLMPORT=50302  #port being used by lockd  <-- change this
DURATION=300   #gather information for 300 seconds

logger "`date` - START of gathering information - before"
#chage the interface eth1 to appropriate value
tcpdump -i eth1 port $NFSPORT or port $NLMPORT -s 512 -C 100 -W 10 -w /dev/shm/before_nfs_lockd_`hostname`.pcap &
tcpdump_before_pid=$!

while [ 1 ]; do
	if grep -qE "$SEARCH_FORMAT1|$SEARCH_FORMAT2" "$MSGFILE"
	then
		break;
	else
#		echo "not found"
		sleep 1
	fi
done
kill -2 $tcpdump_before_pid
logger "`date` - STOP of gathering information - before"

logger "`date` - START of gathering information - after"
#chage the interface eth1 to appropriate value
tcpdump -i eth1 port $NFSPORT or port $NLMPORT -s 512 -C 100 -W 10 -w /dev/shm/after_nfs_lockd_`hostname`.pcap &
tcpdump_after_pid=$!

sleep $DURATION

kill -2 $tcpdump_after_pid
logger "`date` - STOP of gathering information - after"
