import argparse
import sys
import os

config_template="""ENABLE_QCN 1
USE_DYNAMIC_PFC_THRESHOLD 1

PACKET_PAYLOAD_SIZE 1500

TOPOLOGY_FILE experiments/{topo}.txt
FLOW_FILE experiments/{exp}/flow.txt
TRACE_FILE experiments/trace.txt
TRACE_OUTPUT_FILE experiments/{exp}/{cc}/traceout.txt
FCT_OUTPUT_FILE experiments/{exp}/{cc}/fct.txt
PFC_OUTPUT_FILE experiments/{exp}/{cc}/pfc.txt

SIMULATOR_STOP_TIME 4.00

CC_MODE {mode}
ALPHA_RESUME_INTERVAL {t_alpha}
RATE_DECREASE_INTERVAL {t_dec}
CLAMP_TARGET_RATE 0
RP_TIMER {t_inc}
EWMA_GAIN {g}
FAST_RECOVERY_TIMES 1
RATE_AI {ai}Mb/s
RATE_HAI {hai}Mb/s
MIN_RATE 100Mb/s
DCTCP_RATE_AI {dctcp_ai}Mb/s

ERROR_RATE_PER_LINK 0.0000
L2_CHUNK_SIZE 4000
L2_ACK_INTERVAL 1
L2_BACK_TO_ZERO 0

HAS_WIN {has_win}
GLOBAL_T 1
VAR_WIN {vwin}
FAST_REACT {us}
U_TARGET {u_tgt}
MI_THRESH {mi}
INT_MULTI {int_multi}
MULTI_RATE 0
SAMPLE_FEEDBACK 0

RATE_BOUND 1

ACK_HIGH_PRIO {ack_prio}

LINK_DOWN {link_down}

ENABLE_TRACE 0

KMAX_MAP {kmax_map}
KMIN_MAP {kmin_map}
PMAX_MAP {pmax_map}
BUFFER_SIZE {buffer_size}
QLEN_MON_FILE experiments/{exp}/{cc}/qlen.txt
QLEN_MON_START 1000000000
QLEN_MON_END 1050000000
"""
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='run simulation')
	parser.add_argument('--exp', dest='exp', action='store', default='test', help="experiment name")
	parser.add_argument('--cc', dest='cc', action='store', default='hpcc', help="hpcc/dcqcn/timely/dctcp")
	parser.add_argument('--trace', dest='trace', action='store', default='flow', help="the name of the flow file")
	parser.add_argument('--bw', dest="bw", action='store', default='40', help="the NIC bandwidth")
	parser.add_argument('--down', dest='down', action='store', default='0 0 0', help="link down event")
	parser.add_argument('--topo', dest='topo', action='store', default='topology', help="the name of the topology file")
	parser.add_argument('--utgt', dest='utgt', action='store', type=int, default=95, help="eta of HPCC")
	parser.add_argument('--mi', dest='mi', action='store', type=int, default=0, help="MI_THRESH")
	parser.add_argument('--hpai', dest='hpai', action='store', type=int, default=0, help="AI for HPCC")
	parser.add_argument('--run', dest='run', action='store', type=int, default=0, help="run simulation for the trace")
	args = parser.parse_args()

	exp = args.exp
	topo=args.topo
	bw = int(args.bw)
	trace = args.trace
	#bfsz = 16 if bw==50 else 32
	# bfsz = 16 * bw / 50
	bfsz = 12
	u_tgt=args.utgt/100.
	mi=args.mi

	failure = ''
	if args.down != '0 0 0':
		failure = '_down'

	config_name = "experiments/%s/config.txt"%(args.exp)

	kmax_map = "2 %d %d %d %d"%(bw*1000000000, 400*bw/25, bw*4*1000000000, 400*bw*4/25)
	kmin_map = "2 %d %d %d %d"%(bw*1000000000, 100*bw/25, bw*4*1000000000, 100*bw*4/25)
	pmax_map = "2 %d %.2f %d %.2f"%(bw*1000000000, 0.2, bw*4*1000000000, 0.2)
	if (args.cc.startswith("dcqcn")):
		ai = 5 * bw / 25
		hai = 50 * bw /25

		if args.cc == "dcqcn":
			config = config_template.format(exp = exp, bw=bw, trace=trace, topo=topo, cc=args.cc, mode=1, t_alpha=1, t_dec=4, t_inc=300, g=0.00390625, ai=ai, hai=hai, dctcp_ai=1000, has_win=0, vwin=0, us=0, u_tgt=u_tgt, mi=mi, int_multi=1, ack_prio=1, link_down=args.down, failure=failure, kmax_map=kmax_map, kmin_map=kmin_map, pmax_map=pmax_map, buffer_size=bfsz)
		elif args.cc == "dcqcn_paper":
			config = config_template.format(exp = exp, bw=bw, trace=trace, topo=topo, cc=args.cc, mode=1, t_alpha=50, t_dec=50, t_inc=55, g=0.00390625, ai=ai, hai=hai, dctcp_ai=1000, has_win=0, vwin=0, us=0, u_tgt=u_tgt, mi=mi, int_multi=1, ack_prio=1, link_down=args.down, failure=failure, kmax_map=kmax_map, kmin_map=kmin_map, pmax_map=pmax_map, buffer_size=bfsz)
		elif args.cc == "dcqcn_vwin":
			config = config_template.format(exp = exp, bw=bw, trace=trace, topo=topo, cc=args.cc, mode=1, t_alpha=1, t_dec=4, t_inc=300, g=0.00390625, ai=ai, hai=hai, dctcp_ai=1000, has_win=1, vwin=1, us=0, u_tgt=u_tgt, mi=mi, int_multi=1, ack_prio=0, link_down=args.down, failure=failure, kmax_map=kmax_map, kmin_map=kmin_map, pmax_map=pmax_map, buffer_size=bfsz)
		elif args.cc == "dcqcn_paper_vwin":
			config = config_template.format(exp = exp, bw=bw, trace=trace, topo=topo, cc=args.cc, mode=1, t_alpha=50, t_dec=50, t_inc=55, g=0.00390625, ai=ai, hai=hai, dctcp_ai=1000, has_win=1, vwin=1, us=0, u_tgt=u_tgt, mi=mi, int_multi=1, ack_prio=0, link_down=args.down, failure=failure, kmax_map=kmax_map, kmin_map=kmin_map, pmax_map=pmax_map, buffer_size=bfsz)
	elif args.cc == "hpcc":
		ai = 10 * bw / 25;
		if args.hpai > 0:
			ai = args.hpai
		hai = ai # useless
		int_multi = bw / 25;
		# cc = "%s%d"%(args.cc, args.utgt)
		# if (mi > 0):
		# 	cc += "mi%d"%mi
		# if args.hpai > 0:
		# 	cc += "ai%d"%ai
		# config_name = "mix/config_%s_%s_%s%s.txt"%(topo, trace, cc, failure)
		config = config_template.format(exp = exp, bw=bw, trace=trace, topo=topo, cc=args.cc, mode=3, t_alpha=1, t_dec=4, t_inc=300, g=0.00390625, ai=ai, hai=hai, dctcp_ai=1000, has_win=1, vwin=1, us=1, u_tgt=u_tgt, mi=mi, int_multi=int_multi, ack_prio=0, link_down=args.down, failure=failure, kmax_map=kmax_map, kmin_map=kmin_map, pmax_map=pmax_map, buffer_size=bfsz)
	elif args.cc == "dctcp":
		ai = 10 # ai is useless for dctcp
		hai = ai  # also useless
		dctcp_ai=615 # calculated from RTT=13us and MTU=1KB, because DCTCP add 1 MTU per RTT.
		kmax_map = "2 %d %d %d %d" % (
			bw*1000000000, 30*bw/10, bw*4*1000000000, 30*bw*4/10)
		kmin_map = "2 %d %d %d %d"%(bw*1000000000, 30*bw/10, bw*4*1000000000, 30*bw*4/10)
		pmax_map = "2 %d %.2f %d %.2f"%(bw*1000000000, 1.0, bw*4*1000000000, 1.0)
		config = config_template.format(exp = exp, bw=bw, trace=trace, topo=topo, cc=args.cc, mode=8, t_alpha=1, t_dec=4, t_inc=300, g=0.0625, ai=ai, hai=hai, dctcp_ai=dctcp_ai, has_win=1, vwin=1, us=0, u_tgt=u_tgt, mi=mi, int_multi=1, ack_prio=0, link_down=args.down, failure=failure, kmax_map=kmax_map, kmin_map=kmin_map, pmax_map=pmax_map, buffer_size=bfsz)
	elif args.cc == "timely":
		ai = 10 * bw / 10;
		hai = 50 * bw / 10;
		config = config_template.format(exp = exp, bw=bw, trace=trace, topo=topo, cc=args.cc, mode=7, t_alpha=1, t_dec=4, t_inc=300, g=0.00390625, ai=ai, hai=hai, dctcp_ai=1000, has_win=0, vwin=0, us=0, u_tgt=u_tgt, mi=mi, int_multi=1, ack_prio=1, link_down=args.down, failure=failure, kmax_map=kmax_map, kmin_map=kmin_map, pmax_map=pmax_map, buffer_size=bfsz)
	elif args.cc == "timely_vwin":
		ai = 10 * bw / 10;
		hai = 50 * bw / 10;
		config = config_template.format(exp = exp, bw=bw, trace=trace, topo=topo, cc=args.cc, mode=7, t_alpha=1, t_dec=4, t_inc=300, g=0.00390625, ai=ai, hai=hai, dctcp_ai=1000, has_win=1, vwin=1, us=0, u_tgt=u_tgt, mi=mi, int_multi=1, ack_prio=1, link_down=args.down, failure=failure, kmax_map=kmax_map, kmin_map=kmin_map, pmax_map=pmax_map, buffer_size=bfsz)
	else:
		print "unknown cc:", args.cc
		sys.exit(1)

	if(os.path.isdir("./experiments/" + args.exp) == False):
		os.mkdir("./experiments/" + args.exp)

	with open(config_name, "w") as file:
		file.write(config)
	
	if(os.path.isdir("./experiments/" + args.exp + '/' + args.cc) == False):
		os.mkdir("./experiments/" + args.exp + '/' + args.cc)

	if(args.run == 1):
		os.system("./waf --run 'scratch/third %s'"%(config_name))
