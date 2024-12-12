#!/usr/sbin/dtrace -Cqs

/* Sample run:
[root@XXXX mbpatil]# rds-stress -r 192.168.12.3 -s 192.168.12.7 --reset
root@XXXX mbpatil]# ./rds_cm_events.d
DTrace 2.0.0 [Pre-Release with limited functionality]
2024 Apr 26 15:50:37 875411897285974 rds_rdma_cm_event_handler_cmn: [<192.168.12.7,192.168.12.3,0>] DISCONNECTED
2024 Apr 26 15:50:37 875411901904142 rds_conn_create: [<192.168.12.7,192.168.12.3,0>] CONNECT_REQUEST
2024 Apr 26 15:50:37 875411936549996 rds_rdma_cm_event_handler_cmn: [<192.168.12.7,192.168.12.3,0>] ESTABLISHED

[root@XXXX mbpatil]# ./rds_cm_events.d
2024 Apr 26 15:46:08 4311747729846110 rds_rdma_cm_event_handler_cmn: [<192.168.12.3,192.168.12.7,0>] DISCONNECTED
2024 Apr 26 15:46:08 4311747733032294 rds_rdma_cm_event_handler_cmn: [<192.168.12.3,192.168.12.7,0>] ADDR_RESOLVED
2024 Apr 26 15:46:08 4311747733585636 rds_rdma_cm_event_handler_cmn: [<192.168.12.3,192.168.12.7,0>] ROUTE_RESOLVED
2024 Apr 26 15:46:09 4311747768914290 rds_rdma_cm_event_handler_cmn: [<192.168.12.3,192.168.12.7,0>] ESTABLISHED
*/

::BEGIN
{
/*
enum rdma_cm_event_type {
	RDMA_CM_EVENT_ADDR_RESOLVED,
	RDMA_CM_EVENT_ADDR_ERROR,
	RDMA_CM_EVENT_ROUTE_RESOLVED,
	RDMA_CM_EVENT_ROUTE_ERROR,
	RDMA_CM_EVENT_CONNECT_REQUEST,
	RDMA_CM_EVENT_CONNECT_RESPONSE,
	RDMA_CM_EVENT_CONNECT_ERROR,
	RDMA_CM_EVENT_UNREACHABLE,
	RDMA_CM_EVENT_REJECTED,
	RDMA_CM_EVENT_ESTABLISHED,
	RDMA_CM_EVENT_DISCONNECTED,
	RDMA_CM_EVENT_DEVICE_REMOVAL,
	RDMA_CM_EVENT_MULTICAST_JOIN,
	RDMA_CM_EVENT_MULTICAST_ERROR,
	RDMA_CM_EVENT_ADDR_CHANGE,
*/

	CM_EVENT[0] = "ADDR_RESOLVED";
	CM_EVENT[1] = "ADDR_ERROR";
	CM_EVENT[2] = "ROUTE_RESOLVED";
	CM_EVENT[3] = "ROUTE_ERROR";
	CM_EVENT[4] = "CONNECT_REQUEST";
	CM_EVENT[5] = "CONNECT_RESPONSE";
	CM_EVENT[6] = "CONNECT_ERROR";
	CM_EVENT[7] = "UNREACHABLE";
	CM_EVENT[8] = "REJEACTED";
	CM_EVENT[9] = "ESTABLISHED";
	CM_EVENT[10] = "DISCONNECTED";
	CM_EVENT[11] = "DEVICE_REMOVAL";
	CM_EVENT[12] = "MULTICAST_JOIN";
	CM_EVENT[13] = "MULITCAST_ERROR";
	CM_EVENT[14] = "ADDR_CHANGE";
}

::rds_rdma_cm_event_handler_cmn:entry
/ arg2 /
{
	this->event = (struct rdma_cm_event *)arg1;
	this->conn = (struct rds_connection *)arg2;
	this->ic = (struct rds_ib_connection *)this->conn->c_path[0].cp_transport_data;
	this->sip = &this->conn->c_laddr.in6_u.u6_addr32[3];
	this->dip = &this->conn->c_faddr.in6_u.u6_addr32[3];
	this->tos = this->conn->c_tos;

	printf("%Y %lu %s: [<%s,%s,%d>] %s\n",
		walltimestamp, timestamp, probefunc,
		inet_ntoa(this->sip), inet_ntoa(this->dip), this->tos,
		CM_EVENT[this->event->event]);
}

::rds_rdma_cm_event_handler_cmn:entry
/ !arg2 /
{
	self->track_rds_conn_create = 1;
	self->event = (struct rdma_cm_event *)arg1;
}

::rds_conn_create:return
/ self->track_rds_conn_create /
{
	this->conn = (struct rds_connection *)arg1;
	this->event = self->event;

	this->ic = (struct rds_ib_connection *)this->conn->c_path[0].cp_transport_data;
	this->sip = &this->conn->c_laddr.in6_u.u6_addr32[3];
	this->dip = &this->conn->c_faddr.in6_u.u6_addr32[3];
	this->tos = this->conn->c_tos;

	printf("%Y %lu %s: [<%s,%s,%d>] %s\n",
		walltimestamp, timestamp, probefunc,
		inet_ntoa(this->sip), inet_ntoa(this->dip), this->tos,
		CM_EVENT[this->event->event]);

	self->track_rds_conn_create = 0;
}
