#include <iostream>
#include <fstream>
#include "ns3/packet.h"
#include "ns3/simulator.h"
#include "ns3/object-vector.h"
#include "ns3/uinteger.h"
#include "ns3/log.h"
#include "ns3/assert.h"
#include "ns3/global-value.h"
#include "ns3/boolean.h"
#include "ns3/simulator.h"
#include "ns3/broadcom-node.h"
#include "ns3/random-variable.h"
#include "switch-mmu.h"
#include "assert.h"

NS_LOG_COMPONENT_DEFINE("SwitchMmu");
namespace ns3 {
	TypeId SwitchMmu::GetTypeId(void){
		static TypeId tid = TypeId("ns3::SwitchMmu")
			.SetParent<Object>()
			.AddConstructor<SwitchMmu>();
		return tid;
	}

	SwitchMmu::SwitchMmu(void){
		buffer_size = 12 * 1024 * 1024;
		// reserve = 4 * 1024;
		reserve = 0;
		resume_offset = 9 * 1024;

		// headroom
		shared_used_bytes = 0;
		memset(hdrm_bytes, 0, sizeof(hdrm_bytes));
		memset(ingress_bytes, 0, sizeof(ingress_bytes));
		memset(paused, 0, sizeof(paused));
		memset(egress_bytes, 0, sizeof(egress_bytes));
	}
	bool SwitchMmu::CheckIngressAdmission(uint32_t port, uint32_t qIndex, uint32_t psize){
		// printf("PFC threshold: %u\n",GetPfcThreshold(port));
		if (psize + hdrm_bytes[port][qIndex] > headroom[port] && psize + GetSharedUsed(port, qIndex) > GetPfcThreshold(port)){
			printf("%lu %u Drop: queue:%u,%u: Headroom full, hdrm: %u+%u=%u (%u), shared_use: %u+%u=%u (%u) \n", Simulator::Now().GetTimeStep(), node_id, port, qIndex, hdrm_bytes[port][qIndex],psize, hdrm_bytes[port][qIndex]+psize, headroom[port],  GetSharedUsed(port, qIndex), psize, psize+GetSharedUsed(port, qIndex), GetPfcThreshold(port));
			for (uint32_t i = 1; i < 64; i++)
				printf("(%u,%u)", hdrm_bytes[i][3], ingress_bytes[i][3]);
			printf("\n");
			return false;
		}
		return true;
	}
	bool SwitchMmu::CheckEgressAdmission(uint32_t port, uint32_t qIndex, uint32_t psize){
		return true;
	}
	void SwitchMmu::UpdateIngressAdmission(uint32_t port, uint32_t qIndex, uint32_t psize){
		uint32_t prev_ingress = ingress_bytes[port][qIndex];
		uint32_t new_bytes = ingress_bytes[port][qIndex] + psize;
		uint32_t prev_shared_use = GetSharedUsed(port, qIndex);
		uint32_t prev_hdrm = hdrm_bytes[port][qIndex];
		if (new_bytes <= reserve){
			ingress_bytes[port][qIndex] += psize;
		}else {
			uint32_t thresh = GetPfcThreshold(port);
			if (new_bytes - reserve > thresh){
				hdrm_bytes[port][qIndex] += psize;
			}else {
				ingress_bytes[port][qIndex] += psize; 
				shared_used_bytes += std::min(psize, new_bytes - reserve);
			}
		}
		if ((node_id==0))
		{
			std::cout<< "Time: " << Simulator::Now().GetTimeStep() << " [Inque] node: " << node_id << " port: " << port << " psize: " << psize <<  ", ingress: " << prev_ingress << "->" << ingress_bytes[port][qIndex] << ", hdrm: " << prev_hdrm << "->" << hdrm_bytes[port][qIndex] << ", share_used: " << prev_shared_use << "->" << GetSharedUsed(port, qIndex) << ", thres: " << GetPfcThreshold(port) << "\n";
		}
	}
	void SwitchMmu::UpdateEgressAdmission(uint32_t port, uint32_t qIndex, uint32_t psize){
		egress_bytes[port][qIndex] += psize;
	}
	void SwitchMmu::RemoveFromIngressAdmission(uint32_t port, uint32_t qIndex, uint32_t psize){
		uint32_t from_hdrm = std::min(hdrm_bytes[port][qIndex], psize);
		uint32_t from_shared = std::min(psize - from_hdrm, ingress_bytes[port][qIndex] > reserve ? ingress_bytes[port][qIndex] - reserve : 0);
		hdrm_bytes[port][qIndex] -= from_hdrm;
		uint32_t prev_ingress = ingress_bytes[port][qIndex];
		ingress_bytes[port][qIndex] -= psize - from_hdrm;
		shared_used_bytes -= from_shared;

		if ((node_id==0))
		{
			forward_bytes += psize;
			std::cout<< "Time: " << Simulator::Now().GetTimeStep() << " [deque] node: " << node_id << " port: " << port << " psize: " << psize << ", from_hdrm: " << from_hdrm << ", from_shared: " << from_shared << ", ingres: " << prev_ingress << " -> " << ingress_bytes[port][qIndex] << ", forwarded: " << forward_bytes << "\n";
		}

	}
	void SwitchMmu::RemoveFromEgressAdmission(uint32_t port, uint32_t qIndex, uint32_t psize){
		egress_bytes[port][qIndex] -= psize;
	}
	bool SwitchMmu::CheckShouldPause(uint32_t port, uint32_t qIndex){
		// if (node_id == 2 && (port==3))
		// {
		// 	std::cout << "\t[check] " << "port: " << port  \
		// 	          << " paused: " << paused[port][qIndex] << " hdrm: " << hdrm_bytes[port][qIndex] \
		// 			  << " shared use: " << GetSharedUsed(port, qIndex) << " thres: " << GetPfcThreshold(port) \
		// 			  << " should pause: " << (!paused[port][qIndex] && (hdrm_bytes[port][qIndex] > 0 || GetSharedUsed(port, qIndex) >= GetPfcThreshold(port))) << "\n";
		// 	        //   << " shared use: " << GetSharedUsed(port, qIndex) << " thres: " << GetPfcThreshold(port) << " headroom: " << hdrm_bytes[port][qIndex] << "\n";
		// }
		if (!paused[port][qIndex] && (hdrm_bytes[port][qIndex] > 0 || GetSharedUsed(port, qIndex) >= GetPfcThreshold(port)))
		{
			std::cout << "\t!!!!!!! node: " << node_id << " port: " << port << " sends pause hdrm: " << hdrm_bytes[port][qIndex] << " used: " << GetSharedUsed(port, qIndex) << " thres: " << GetPfcThreshold(port) << "\n";
		}
		return !paused[port][qIndex] && (hdrm_bytes[port][qIndex] > 0 || GetSharedUsed(port, qIndex) >= GetPfcThreshold(port));
	}
	bool SwitchMmu::CheckShouldResume(uint32_t port, uint32_t qIndex){ 
		if (!paused[port][qIndex])
			return false;
		uint32_t shared_used = GetSharedUsed(port, qIndex);
	    bool res =  hdrm_bytes[port][qIndex] == 0 && (shared_used == 0 || shared_used + resume_offset <= GetPfcThreshold(port));
		if (res)
		{
			std::cout << "\t!!!!!!! node: " << node_id << " port: " << port << " sends resume\n";
		}
		return res;
	}
	void SwitchMmu::SetPause(uint32_t port, uint32_t qIndex){
		paused[port][qIndex] = true;
	}
	void SwitchMmu::SetResume(uint32_t port, uint32_t qIndex){
		paused[port][qIndex] = false;
	}

	uint32_t SwitchMmu::GetPfcThreshold(uint32_t port){
		// printf("%u, %u, %u, %u, %u\n",buffer_size,total_hdrm,total_rsrv,shared_used_bytes,pfc_a_shift[port]);
		// return 4*1024;
		// if (node_id == 2 && port == 2)
		// {
		// 	std::cout << "\t[PFC] buffer size: " << buffer_size << " total hdrm: " << total_hdrm << " total rsrv: " << total_rsrv << " shared used: " << shared_used_bytes << " pfc: " << ((buffer_size - total_hdrm - total_rsrv - shared_used_bytes) >> pfc_a_shift[port]) << "\n";

		// }

		// return 9*1048;

		// return (buffer_size - total_hdrm - total_rsrv - shared_used_bytes) >> 2;
		
		// // return 1048 + 1;
		bool small_buffer_size = true;
		if (small_buffer_size)
		{
			// return 1048 * 54 * 3 + 1;
			return 1048 * 5 + 1;

		}
		assert(uint64_t(buffer_size) >= uint64_t(total_hdrm + total_rsrv + shared_used_bytes));
		return (buffer_size - total_hdrm - total_rsrv - shared_used_bytes) >> pfc_a_shift[port];
	}
	uint32_t SwitchMmu::GetSharedUsed(uint32_t port, uint32_t qIndex){
		uint32_t used = ingress_bytes[port][qIndex];
		return used > reserve ? used - reserve : 0;
	}
	bool SwitchMmu::ShouldSendCN(uint32_t ifindex, uint32_t qIndex){
		if (qIndex == 0)
			return false;
		if (egress_bytes[ifindex][qIndex] > kmax[ifindex])
			return true;
		if (egress_bytes[ifindex][qIndex] > kmin[ifindex]){
			double p = pmax[ifindex] * double(egress_bytes[ifindex][qIndex] - kmin[ifindex]) / (kmax[ifindex] - kmin[ifindex]);
			if (UniformVariable(0, 1).GetValue() < p)
				return true;
		}
		return false;
	}
	void SwitchMmu::ConfigEcn(uint32_t port, uint32_t _kmin, uint32_t _kmax, double _pmax){
		kmin[port] = _kmin * 1000;
		kmax[port] = _kmax * 1000;
		pmax[port] = _pmax;
	}
	void SwitchMmu::ConfigHdrm(uint32_t port, uint32_t size){
		headroom[port] = size;
	}
	void SwitchMmu::ConfigNPort(uint32_t n_port){
		total_hdrm = 0;
		total_rsrv = 0;
		for (uint32_t i = 1; i <= n_port; i++){
			total_hdrm += headroom[i];
			total_rsrv += reserve;
		}
		std::cout << "switch " << node_id << " total hdrm: " << total_hdrm << " total rsrv: " << total_rsrv << "\n";
		// if (node_id == 2)
		// {
			
		// }
		
	}
	void SwitchMmu::ConfigBufferSize(uint32_t size){
		buffer_size = size;
	}
}
