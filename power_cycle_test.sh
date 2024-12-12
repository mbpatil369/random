#!/bin/sh

touch /tmp/$(basename $0).running

STOP_FILE="/tmp/stop"

#wait for 5 mins
sleep 300

power_cycle()
{
        if [[ -f $STOP_FILE ]]
        then
                logger "$0: Found $STOP_FILE. Stopping Power Cycle test"
                return
        fi

        logger "$0: doing Power Cycle"
        sync;sync;sync
        sleep 3

        ipmitool sunoem setval /System/deep_power_cycle true
        ipmitool sunoem setval /SP/policy/HOST_AUTO_POWER_ON enabled
        ipmitool power reset
}

conns=`rds-info -I | grep ffff | wc -l`
stuck_conns=`rds-info -I | grep "::" | grep -v ffff | wc -l`

logger "$0: conns=$conns stuck_conns=$stuck_conns"

#rename
mv /tmp/$(basename $0).running /tmp/$(basename $0).ran.`date +'%Y%m%d_%H%M%S'`

if [[ $conns -ne 0 && $stuck_conns -eq 0 ]]
then
        power_cycle
fi
