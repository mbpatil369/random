#!/usr/sbin/dtrace -Cqs

/*
Sample Run:
[root@XXXX ~]# rds-stress -r 192.168.12.3 -s 192.168.12.7 --reset

[root@XXXX mbpatil]# ./mad.d
DTrace 2.0.0 [Pre-Release with limited functionality]
2024 Apr 26 13:45:32 867906486995578 cm_recv_handler: DREQ SUCCESS(0)
2024 Apr 26 13:45:32 867906487809840 cm_send_handler: DREP SUCCESS(0) IDLE
2024 Apr 26 13:45:32 867906491846567 cm_recv_handler: REQ SUCCESS(0)
2024 Apr 26 13:45:32 867906525626057 cm_recv_handler: RTU SUCCESS(0)
2024 Apr 26 13:45:32 867906525643080 cm_send_handler: REP WR_FLUSH_ERR(5) REP_SENT
*/

#define container_of(__ptr, __type, __member) ((__type *)((unsigned long long)__ptr - (unsigned long long)offsetof(__type, __member)))

BEGIN
{
/*
#define CM_REQ_ATTR_ID	  cpu_to_be16(0x0010)
#define CM_MRA_ATTR_ID	  cpu_to_be16(0x0011)
#define CM_REJ_ATTR_ID	  cpu_to_be16(0x0012)
#define CM_REP_ATTR_ID	  cpu_to_be16(0x0013)
#define CM_RTU_ATTR_ID	  cpu_to_be16(0x0014)
#define CM_DREQ_ATTR_ID	 cpu_to_be16(0x0015)
#define CM_DREP_ATTR_ID	 cpu_to_be16(0x0016)
#define CM_SIDR_REQ_ATTR_ID     cpu_to_be16(0x0017)
#define CM_SIDR_REP_ATTR_ID     cpu_to_be16(0x0018)
#define CM_LAP_ATTR_ID	  cpu_to_be16(0x0019)
#define CM_APR_ATTR_ID	  cpu_to_be16(0x001A)

enum ib_wc_status {
	IB_WC_SUCCESS,
	IB_WC_LOC_LEN_ERR,
	IB_WC_LOC_QP_OP_ERR,
	IB_WC_LOC_EEC_OP_ERR,
	IB_WC_LOC_PROT_ERR,
	IB_WC_WR_FLUSH_ERR,
	IB_WC_MW_BIND_ERR,
	IB_WC_BAD_RESP_ERR,
	IB_WC_LOC_ACCESS_ERR,
	IB_WC_REM_INV_REQ_ERR,
	IB_WC_REM_ACCESS_ERR,
	IB_WC_REM_OP_ERR,
	IB_WC_RETRY_EXC_ERR,
	IB_WC_RNR_RETRY_EXC_ERR,
	IB_WC_LOC_RDD_VIOL_ERR,
	IB_WC_REM_INV_RD_REQ_ERR,
	IB_WC_REM_ABORT_ERR,
	IB_WC_INV_EECN_ERR,
	IB_WC_INV_EEC_STATE_ERR,
	IB_WC_FATAL_ERR,
	IB_WC_RESP_TIMEOUT_ERR,
	IB_WC_GENERAL_ERR
};

enum ib_cm_state {
	IB_CM_IDLE,
	IB_CM_LISTEN,
	IB_CM_REQ_SENT,
	IB_CM_REQ_RCVD,
	IB_CM_MRA_REQ_SENT,
	IB_CM_MRA_REQ_RCVD,
	IB_CM_REP_SENT,
	IB_CM_REP_RCVD,
	IB_CM_MRA_REP_SENT,
	IB_CM_MRA_REP_RCVD,
	IB_CM_ESTABLISHED,
	IB_CM_DREQ_SENT,
	IB_CM_DREQ_RCVD,
	IB_CM_TIMEWAIT,
	IB_CM_SIDR_REQ_SENT,
	IB_CM_SIDR_REQ_RCVD
};

enum ib_cm_event_type {
	IB_CM_REQ_ERROR,
	IB_CM_REQ_RECEIVED,
	IB_CM_REP_ERROR,
	IB_CM_REP_RECEIVED,
	IB_CM_RTU_RECEIVED,
	IB_CM_USER_ESTABLISHED,
	IB_CM_DREQ_ERROR,
	IB_CM_DREQ_RECEIVED,
	IB_CM_DREP_RECEIVED,
	IB_CM_TIMEWAIT_EXIT,
	IB_CM_MRA_RECEIVED,
	IB_CM_REJ_RECEIVED,
	IB_CM_LAP_ERROR,
	IB_CM_LAP_RECEIVED,
	IB_CM_APR_RECEIVED,
	IB_CM_SIDR_REQ_ERROR,
	IB_CM_SIDR_REQ_RECEIVED,
	IB_CM_SIDR_REP_RECEIVED
};
*/

	ATTR_ID[0x10] = "REQ";
	ATTR_ID[0x11] = "MRA";
	ATTR_ID[0x12] = "REJ";
	ATTR_ID[0x13] = "REP";
	ATTR_ID[0x14] = "RTU";
	ATTR_ID[0x15] = "DREQ";
	ATTR_ID[0x16] = "DREP";
	ATTR_ID[0x17] = "SIDR_REQ";
	ATTR_ID[0x18] = "SIDR_REP";
	ATTR_ID[0x19] = "LAP";
	ATTR_ID[0x1A] = "ARP";

	WC_STATUS[0] = "SUCCESS";
	WC_STATUS[1] = "LOC_LEN_ERR";
	WC_STATUS[2] = "LOC_QP_OP_ERR";
	WC_STATUS[3] = "LOC_EEC_OP_ERR";
	WC_STATUS[4] = "LOC_PROT_ERR";
	WC_STATUS[5] = "WR_FLUSH_ERR";
	WC_STATUS[6] = "MW_BIND_ERR";
	WC_STATUS[7] = "BAD_RESP_ERR";
	WC_STATUS[8] = "LOC_ACCESS_ERR";
	WC_STATUS[9] = "REM_OP_ERR";
	WC_STATUS[10] = "RETRY_EXC_ERR";
	WC_STATUS[11] = "RNR_RETRY_EXC_ERR";
	WC_STATUS[12] = "LOC_RDD_VIOL_ERR";
	WC_STATUS[13] = "REM_INV_RD_REQ_ERR";
	WC_STATUS[14] = "REM_ABORT_ERR";
	WC_STATUS[15] = "INV_EEC_ERR";
	WC_STATUS[16] = "IBV_EEC_STATE_ERR";
	WC_STATUS[17] = "FATAL_ERR";
	WC_STATUS[18] = "RESP_TIMEOUT_ERR";
	WC_STATUS[19] = "GEN_ERR";

	CM_STATE[0] = "IDLE";
	CM_STATE[1] = "LISTEN";
	CM_STATE[2] = "REQ_SENT";
	CM_STATE[3] = "REQ_RECEIVED";
	CM_STATE[4] = "MRA_REQ_SENT";
	CM_STATE[5] = "MRA_REQ_RECEIVED";
	CM_STATE[6] = "REP_SENT";
	CM_STATE[7] = "REP_RECEIVED";
	CM_STATE[8] = "MRA_REP_SENT";
	CM_STATE[9] = "MRA_REP_RECEIVED";
	CM_STATE[10] = "ESTABLISHED";
	CM_STATE[11] = "DREQ_SENT";
	CM_STATE[12] = "DREQ_RECEIVED";
	CM_STATE[13] = "TIMEWAIT";
	CM_STATE[14] = "SIDR_REQ_SENT";
	CM_STATE[15] = "SIDR_REQ_RECEIVED";

	CM_EVENT[0] = "REQ_ERROR";
	CM_EVENT[1] = "REQ_RECEIVED";
	CM_EVENT[2] = "REP_ERROR";
	CM_EVENT[3] = "REP_RECEIVED";
	CM_EVENT[4] = "RTU_RECEIVED";
	CM_EVENT[5] = "USER_ESTABLISHED";
	CM_EVENT[6] = "DREQ_ERROR";
	CM_EVENT[7] = "DREQ_RECEIVED";
	CM_EVENT[8] = "DREP_RECEIVED";
	CM_EVENT[9] = "TIMEWAIT_EXIT";
	CM_EVENT[10] = "MRA_RECEIVED";
	CM_EVENT[11] = "REJ_RECEIVED";
	CM_EVENT[12] = "LAP_ERROR";
	CM_EVENT[13] = "LAP_RECEIVED";
	CM_EVENT[14] = "ARP_RECEIVED";
	CM_EVENT[15] = "SIDR_REQ_ERROR";
	CM_EVENT[16] = "SIDR_REQ_RECEIVED";
	CM_EVENT[17] = "SIDR_REP_RECEIVED";
}

fbt:ib_cm:*cm_send_handler*:entry
{
	this->mad_agent = (struct ib_mad_agent *)arg0;
	this->cm_port = (struct cm_port *)this->mad_agent->context;
	this->cm_dev = (struct cm_device *)this->cm_port->cm_dev;
	this->ib_device = (struct ib_device *)this->cm_dev->ib_device;
	this->port_num = this->cm_port->port_num;

	this->mad_send_wc = (struct ib_mad_send_wc *)arg1;
	this->msg = (struct ib_mad_send_buf *)this->mad_send_wc->send_buf;
	this->msg_hdr = (struct ib_mad_hdr *)this->msg->mad;
	this->attr_id = ntohs(this->msg_hdr->attr_id);
	this->>cm_state = (unsigned long)this->msg->context[1];

	printf("%Y %lu %s:%s:%d %s %s(%d) %s\n",
		walltimestamp, timestamp, probefunc,
		this->ib_device->name, this->port_num,
		ATTR_ID[this->attr_id],
		WC_STATUS[this->mad_send_wc->status], this->mad_send_wc->status,
		CM_STATE[this->cm_state]);
}

fbt:ib_cm:*cm_recv_handler*:entry
{
	this->mad_agent = (struct ib_mad_agent *)arg0;
	this->cm_port = (struct cm_port *)this->mad_agent->context;
	this->cm_dev = (struct cm_device *)this->cm_port->cm_dev;
	this->ib_device = (struct ib_device *)this->cm_dev->ib_device;
	this->port_num = this->cm_port->port_num;

	this->mad_recv_wc = (struct ib_mad_recv_wc *)arg2;
	this->recv_msg = (struct ib_mad_recv_buf *) &this->mad_recv_wc->recv_buf;
	/* recv_mad = (struct ib_mad *)this->recv_msg->mad;*/
	this->grh = (struct ib_grh *)this->recv_msg->grh;
	this->recv_mad = (struct ib_mad *)(this->grh + 1);
	this->msg_hdr = (struct ib_mad_hdr *)&this->recv_mad->mad_hdr;
	this->attr_id = ntohs(this->msg_hdr->attr_id);

	this->wc = (struct ib_wc *)this->mad_recv_wc->wc;

	printf("%Y %lu %s:%s:%d %s %s(%d)\n",
		walltimestamp, timestamp, probefunc,
		this->ib_device->name, this->port_num,
		ATTR_ID[this->attr_id],
		WC_STATUS[this->wc->status], this->wc->status);
}

fbt:ib_cm:*cm_work_handler*:entry
{
	this->_work = (struct work_struct *)arg0;
	this->work = container_of(this->_work, struct cm_work, work);
	this->cm_port = (struct cm_port *)this->work->port;
	this->cm_dev = (struct cm_device *)this->cm_port->cm_dev;
	this->ib_device = (struct ib_device *)this->cm_dev->ib_device;
	this->port_num = this->cm_port->port_num;

	this->cm_event = (struct ib_cm_event *)&this->work->cm_event;

	printf("%Y %lu %s:%s:%d %s\n",
		walltimestamp, timestamp, probefunc,
		this->ib_device->name, this->port_num,
		CM_EVENT[this->cm_event->event]);
}
