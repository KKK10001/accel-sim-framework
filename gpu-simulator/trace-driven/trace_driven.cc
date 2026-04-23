// Copyright (c) 2018-2021, Mahmoud Khairy, Vijay Kandiah, Timothy Rogers, Tor
// M. Aamodt, Nikos Hardavellas
// Northwestern University, Purdue University, The University of British
// Columbia
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
// 1. Redistributions of source code must retain the above copyright notice,
// this
//    list of conditions and the following disclaimer;
// 2. Redistributions in binary form must reproduce the above copyright notice,
//    this list of conditions and the following disclaimer in the documentation
//    and/or other materials provided with the distribution;
// 3. Neither the names of Northwestern University, Purdue University,
//    The University of British Columbia nor the names of their contributors
//    may be used to endorse or promote products derived from this software
//    without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.

#include <bits/stdc++.h>
#include <math.h>
#include <stdio.h>
#include <time.h>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "../ISA_Def/accelwattch_component_mapping.h"
#include "../ISA_Def/ampere_opcode.h"
#include "../ISA_Def/kepler_opcode.h"
#include "../ISA_Def/pascal_opcode.h"
#include "../ISA_Def/trace_opcode.h"
#include "../ISA_Def/turing_opcode.h"
#include "../ISA_Def/volta_opcode.h"
#include "abstract_hardware_model.h"
#include "cuda-sim/cuda-sim.h"
#include "cuda-sim/ptx_ir.h"
#include "cuda-sim/ptx_parser.h"
#include "gpgpu-sim/gpu-sim.h"
#include "gpgpu_context.h"
#include "gpgpusim_entrypoint.h"
#include "option_parser.h"
#include "trace_driven.h"

const trace_warp_inst_t *trace_shd_warp_t::get_next_trace_inst() {
  if (trace_pc < warp_traces.size()) {
    trace_warp_inst_t *new_inst = new trace_warp_inst_t(get_shader()->get_config());
    new_inst->set_warp_id(get_warp_id());
    new_inst->set_sid(get_shader()->get_sid());
    new_inst->set_time(get_time());
    // new_inst->set_time(get_shader()->get_time());
    new_inst->parse_from_trace_struct(
        warp_traces[trace_pc], m_kernel_info->OpcodeMap,
        m_kernel_info->m_tconfig, m_kernel_info->m_kernel_trace_info);
    trace_pc++;
    return new_inst;
  } else
    return NULL;
}

void trace_shd_warp_t::clear() {
  trace_pc = 0;
  warp_traces.clear();
  m_trace_active_threads.reset();
}

// functional_done
bool trace_shd_warp_t::trace_done() { return trace_pc == (warp_traces.size()); }

address_type trace_shd_warp_t::get_start_trace_pc() {
  assert(warp_traces.size() > 0);
  return warp_traces[0].m_pc;
}

address_type trace_shd_warp_t::get_pc() {
  assert(warp_traces.size() > 0);
  assert(trace_pc < warp_traces.size());
  return warp_traces[trace_pc].m_pc;
}

void trace_shd_warp_t::init_active_threads(unsigned active_count) {
  m_trace_active_threads.reset();
  unsigned limit = std::min<unsigned>(active_count, MAX_WARP_SIZE);
  for (unsigned lane = 0; lane < limit; ++lane) {
    m_trace_active_threads.set(lane);
  }
}

bool trace_shd_warp_t::is_lane_active(unsigned lane) const {
  if (lane >= MAX_WARP_SIZE) return false;
  return m_trace_active_threads.test(lane);
}

void trace_shd_warp_t::mark_lane_completed(unsigned lane) {
  if (!is_lane_active(lane)) return;
  m_trace_active_threads.reset(lane);
  shd_warp_t::set_completed(lane);
}

trace_kernel_info_t::trace_kernel_info_t(dim3 gridDim, dim3 blockDim,
                                         trace_function_info *m_function_info,
                                         trace_parser *parser,
                                         class trace_config *config,
                                         kernel_trace_t *kernel_trace_info)
    : kernel_info_t(gridDim, blockDim, m_function_info,
                    kernel_trace_info->cuda_stream_id) {
  m_parser = parser;
  m_tconfig = config;
  m_kernel_trace_info = kernel_trace_info;
  m_was_launched = false;

  // resolve the binary version
  if (kernel_trace_info->binary_verion == AMPERE_RTX_BINART_VERSION ||
      kernel_trace_info->binary_verion == AMPERE_A100_BINART_VERSION) {
    OpcodeMap = &Ampere_OpcodeMap;
  }    
  else if (kernel_trace_info->binary_verion == VOLTA_BINART_VERSION) {
    OpcodeMap = &Volta_OpcodeMap;
  }
  else if (kernel_trace_info->binary_verion == PASCAL_TITANX_BINART_VERSION ||
           kernel_trace_info->binary_verion == PASCAL_P100_BINART_VERSION) {
    OpcodeMap = &Pascal_OpcodeMap;
  }    
  else if (kernel_trace_info->binary_verion == KEPLER_BINART_VERSION) {
    OpcodeMap = &Kepler_OpcodeMap;
  }
  else if (kernel_trace_info->binary_verion == TURING_BINART_VERSION) {
    OpcodeMap = &Turing_OpcodeMap;
  }    
  else {
    printf("unsupported binary version: %d\n",
           kernel_trace_info->binary_verion);
    fflush(stdout);
    exit(0);
  }
}

void trace_kernel_info_t::get_next_threadblock_traces(
    std::vector<std::vector<inst_trace_t> *> threadblock_traces) {
  m_parser->get_next_threadblock_traces(
      threadblock_traces, m_kernel_trace_info->trace_verion,
      m_kernel_trace_info->enable_lineinfo, m_kernel_trace_info->pipeReader);
}

types_of_operands get_oprnd_type(op_type op, special_ops sp_op) {
  switch (op) {
    case SP_OP:
    case SFU_OP:
    case SPECIALIZED_UNIT_2_OP:
    case SPECIALIZED_UNIT_3_OP:
    case DP_OP:
    case LOAD_OP:
    case STORE_OP:
      return FP_OP;
    case INTP_OP:
    case SPECIALIZED_UNIT_4_OP:
      return INT_OP;
    case ALU_OP:
      if ((sp_op == FP__OP) || (sp_op == TEX__OP) || (sp_op == OTHER_OP))
        return FP_OP;
      else if (sp_op == INT__OP)
        return INT_OP;
    default:
      return UN_OP;
  }
}

void trace_warp_inst_t::dump_load_detail(
  u32 core,
  u32 warp,
  u64 pc,
  std::string opcode, /* inst name */
  _memory_op_t memory_op,
  memory_space_t space,
  cache_operator_type cache_op,
  u32 latency, u32 issue_gap
) {

  fprintf(Trace::out, 
  "%llu "
  "core:%u " /* core */
  "warp:%u " /* warp */
  "inst "
  "pc:%#llx " /* pc */  
  "%s " /* opcode */
  "%s " /* memory_op */
  "%s " /* m_type */
  "%s " /* cache_op */
  "lat:%u " /* latency */
  "issue_gap:%u\n", /* issue_gap */
  get_time(), core, warp, pc, 
  opcode.c_str(),
  memory_op_str(memory_op),
  memory_space_str(space.get_type()),
  cache_op_str(cache_op),
  latency, issue_gap);
}

bool trace_warp_inst_t::parse_from_trace_struct(
    const inst_trace_t &trace,
    const std::unordered_map<std::string, OpcodeChar> *OpcodeMap,
    const class trace_config *tconfig,
    const class kernel_trace_t *kernel_trace_info) {
  // fill the inst_t and warp_inst_t params
  
  // fill active mask
  active_mask_t active_mask = trace.mask;
  set_active(active_mask);

  // fill and initialize common params
  m_decoded = true;
  pc = (address_type)trace.m_pc;
  trace_opcode = trace.opcode;  
  std::string inst_name = trace.opcode.c_str();
  const u32 issue_gap   = initiation_interval;

  // starting from MAXWELL isize = 16 bytes (including the control bytes)
  isize = 16;
  for (unsigned i = 0; i < MAX_OUTPUT_VALUES; i++) {
    out[i] = 0;
  }
  for (unsigned i = 0; i < MAX_INPUT_VALUES; i++) {
    in[i] = 0;
  }

  is_vectorin = 0;
  is_vectorout = 0;
  pred = 0;
  ar1 = 0;
  ar2 = 0;
  memory_op = no_memory_op;
  data_size = 0;
  op = ALU_OP;
  sp_op = OTHER_OP;
  mem_op = NOT_TEX;
  const_cache_operand = 0;
  oprnd_type = UN_OP;

  // get the opcode
  std::vector<std::string> opcode_tokens = trace.get_opcode_tokens();
  std::string opcode1 = opcode_tokens[0];

  std::unordered_map<std::string, OpcodeChar>::const_iterator it = OpcodeMap->find(opcode1);
  if (it != OpcodeMap->end()) {
    m_opcode = it->second.opcode;
    op = (op_type)(it->second.opcode_category);

    // for debug OpcodeMap
    if (DTRACE(UOP_DETAIL)) {
      fprintf(Trace::out, "OpcodeMap[opcode1:%s] = <opcode:%s, op_type:%s>\n",
        opcode1.c_str(), trace.opcode.c_str(), uarch_op_str(op));
    }

    const std::unordered_map<unsigned, unsigned> *OpcPowerMap = &OpcodePowerMap;
    std::unordered_map<unsigned, unsigned>::const_iterator it2 = 
      OpcPowerMap->find(m_opcode);
    if (it2 != OpcPowerMap->end()) {
      sp_op = (special_ops)(it2->second);
    }

    oprnd_type = get_oprnd_type(op, sp_op);
  } else {
    std::cout << "ERROR:  undefined instruction : " << trace.opcode
              << " Opcode: " << opcode1 << std::endl;
    assert(0 && "undefined instruction");
  }
  std::string opcode = trace.opcode;

  if (opcode1 == "MUFU") {  // Differentiate between different MUFU operations
                            // for power model
    if ((opcode == "MUFU.SIN") || (opcode == "MUFU.COS")) sp_op = FP_SIN_OP;
    if ((opcode == "MUFU.EX2") || (opcode == "MUFU.RCP")) sp_op = FP_EXP_OP;
    if (opcode == "MUFU.RSQ") sp_op = FP_SQRT_OP;
    if (opcode == "MUFU.LG2") sp_op = FP_LG_OP;
  }

  if (opcode1 == "IMAD") {  // Differentiate between different IMAD operations
                            // for power model
    if ((opcode == "IMAD.MOV") || (opcode == "IMAD.IADD")) sp_op = INT__OP;
  }

  // fill regs information
  num_regs = trace.reg_srcs_num + trace.reg_dsts_num;
  num_operands = num_regs;
  outcount = trace.reg_dsts_num;
  for (unsigned m = 0; m < trace.reg_dsts_num; ++m) {
    // Increment by one because GPGPU-sim starts
    // from R1, while SASS starts from R0
    out[m] = trace.reg_dest[m] + 1;                                
    arch_reg.dst[m] = trace.reg_dest[m] + 1;
  }

  incount = trace.reg_srcs_num;
  for (unsigned m = 0; m < trace.reg_srcs_num; ++m) {
    // Increment by one because GPGPU-sim starts
    // from R1, while SASS starts from R0    
    in[m] = trace.reg_src[m] + 1;                                   
    arch_reg.src[m] = trace.reg_src[m] + 1;
  }

  // fill latency and initl
  tconfig->set_latency(op, latency, initiation_interval);

  // if (opcode1 == "FCHK") {
  //   fprintf(Trace::out, "Hit target inst FCHK\n");
  // }
  // UARCH_TUP(NO_OP)
  // UARCH_TUP(ALU_OP) // 
  // UARCH_TUP(SFU_OP) // 
  // UARCH_TUP(DP_OP) // 
  // UARCH_TUP(SP_OP) //
  // UARCH_TUP(INTP_OP) // 
  // UARCH_TUP(LOAD_OP) //
  // UARCH_TUP(STORE_OP) //
  // UARCH_TUP(BARRIER_OP) // 
  // UARCH_TUP(MEMORY_BARRIER_OP) // 
  // UARCH_TUP(EXIT_OPS) // 
  // UARCH_TUP(SPECIALIZED_UNIT_1_OP)
  // UARCH_TUP(SPECIALIZED_UNIT_2_OP)  
  if (!strcmp(uarch_op_str(op), "ALU_OP"))
  {
    // Hit ALU_OP F2F.F64.F32 lat:2 issue_gap:2
    if (DTRACE(UOP_DETAIL)) {
      fprintf(Trace::out, "Hit ALU_OP (m_opcode:%u) %s lat:%u issue_gap:%u\n", 
        m_opcode, trace.opcode.c_str(), latency, initiation_interval);
    }
  }   
  else if (!strcmp(uarch_op_str(op), "SFU_OP"))
  {
    // Hit SFU_OP MUFU.RCP lat:20 issue_gap:8 (dst = 1.0f / src)
    if (DTRACE(UOP_DETAIL)) {
      fprintf(Trace::out, "Hit SFU_OP (m_opcode:%u) %s lat:%u issue_gap:%u\n", 
        m_opcode, trace.opcode.c_str(), latency, initiation_interval);
    }
  }  
  else if (!strcmp(uarch_op_str(op), "DP_OP"))
  {
    // Hit DP_OP DFMA lat:8 issue_gap:4
    if (DTRACE(UOP_DETAIL)) {
      fprintf(Trace::out, "Hit DP_OP (m_opcode:%u) %s lat:%u issue_gap:%u\n", 
        m_opcode, trace.opcode.c_str(), latency, initiation_interval);
    }
  }    
  else if (!strcmp(uarch_op_str(op), "SP_OP"))
  {
    // Hit SP_OP FMUL lat:2 issue_gap:2
    if (DTRACE(UOP_DETAIL)) {
      fprintf(Trace::out, "Hit SP_OP (m_opcode:%u) %s lat:%u issue_gap:%u\n", 
        m_opcode, trace.opcode.c_str(), latency, initiation_interval);
    }
  }   
  else if (!strcmp(uarch_op_str(op), "INTP_OP"))
  {
    // Hit INTP_OP IMAD.MOV.U32 lat:2 issue_gap:2
    if (DTRACE(UOP_DETAIL)) {
      fprintf(Trace::out, "Hit INTP_OP (m_opcode:%u) %s lat:%u issue_gap:%u\n", 
        m_opcode, trace.opcode.c_str(), latency, initiation_interval);      
    }
  }    
  else if (!strcmp(uarch_op_str(op), "LOAD_OP"))
  {
    // Hit LOAD_OP (m_opcode:71) LDG.E.SYS lat:1 issue_gap:1    
    if (DTRACE(UOP_DETAIL)) {
      fprintf(Trace::out, "Hit pc:%#llx warp:%u LOAD_OP (m_opcode:%u) %s lat:%u issue_gap:%u\n", 
        pc, get_warp_id(), m_opcode, trace.opcode.c_str(), latency, initiation_interval);      
    }
  } 
  else if (!strcmp(uarch_op_str(op), "STORE_OP"))
  {
    // Hit STORE_OP STS lat:1 issue_gap:1
    if (DTRACE(UOP_DETAIL)) {
      fprintf(Trace::out, "Hit STORE_OP (m_opcode:%u) %s lat:%u issue_gap:%u\n", 
        m_opcode, trace.opcode.c_str(), latency, initiation_interval);
    }
  }
  else if (!strcmp(uarch_op_str(op), "BARRIER_OP"))
  {
    // Hit BARRIER_OP BAR.SYNC lat:1 issue_gap:1
    if (DTRACE(UOP_DETAIL)) {
      fprintf(Trace::out, "Hit BARRIER_OP (m_opcode:%u) %s lat:%u issue_gap:%u\n", 
        m_opcode, trace.opcode.c_str(), latency, initiation_interval);
    }
  }  
  else if (!strcmp(uarch_op_str(op), "MEMORY_BARRIER_OP"))
  {
    if (DTRACE(UOP_DETAIL)) {
      fprintf(Trace::out, "Hit MEMORY_BARRIER_OP (m_opcode:%u) %s lat:%u issue_gap:%u\n", 
        m_opcode, trace.opcode.c_str(), latency, initiation_interval);
    }
  }
  else if (!strcmp(uarch_op_str(op), "EXIT_OP"))
  { 
    if (DTRACE(UOP_DETAIL)) {
      fprintf(Trace::out, "Hit EXIT_OP (m_opcode:%u) %s lat:%u issue_gap:%u\n", 
        m_opcode, trace.opcode.c_str(), latency, initiation_interval);
    }
  }
  else if (!strcmp(uarch_op_str(op), "SPECIALIZED_UNIT_1_OP"))
  {
    // Hit SPECIALIZED_UNIT_1_OP BRA lat:4 issue_gap:4
    if (DTRACE(UOP_DETAIL)) {
      fprintf(Trace::out, "Hit SPECIALIZED_UNIT_1_OP (m_opcode:%u) %s lat:%u issue_gap:%u\n", 
        m_opcode, trace.opcode.c_str(), latency, initiation_interval);
    }
  }
  else if (!strcmp(uarch_op_str(op), "SPECIALIZED_UNIT_2_OP"))
  {
    if (DTRACE(UOP_DETAIL)) {
      fprintf(Trace::out, "Hit SPECIALIZED_UNIT_2_OP (m_opcode:%u) %s lat:%u issue_gap:%u\n", 
        m_opcode, trace.opcode.c_str(), latency, initiation_interval);      
    }
  }  

  // fill addresses
  if (trace.memadd_info != NULL) {
    data_size = trace.memadd_info->width;
    for (unsigned i = 0; i < warp_size(); ++i)
      set_addr(i, trace.memadd_info->addrs[i]);
  }

  // handle special cases and fill memory space
  switch (m_opcode) {
    case OP_LDC:  // handle Load from Constant
      data_size = 4;
      memory_op = memory_load;
      const_cache_operand = 1;
      space.set_type(const_space);
      cache_op = CACHE_ALL;
      break;
    case OP_LDG:
    // LDGSTS is loading the values needed directly from the global memory to
    // shared memory. Before this feature, the values need to be loaded to
    // registers first, then store to the shared memory.
    case OP_LDGSTS:  // Add for memcpy_async
    case OP_LDL:
      assert(data_size > 0);
      memory_op = memory_load;
      cache_op = CACHE_ALL;
      if (m_opcode == OP_LDL) {
        space.set_type(local_space);
      } else {
        space.set_type(global_space);
      }
      // Add for LDGSTS instruction
      if (m_opcode == OP_LDGSTS) { // AMPERE specific instruction
        m_is_ldgsts = true;
      }
      // check the cache scope, if its strong GPU, then bypass L1
      if ((trace.check_opcode_contain(opcode_tokens, "STRONG") &&
           trace.check_opcode_contain(opcode_tokens, "GPU")) ||
          trace.check_opcode_contain(opcode_tokens, "BYPASS")) {
        cache_op = CACHE_GLOBAL;
      }
      if (DTRACE(LOAD_DETAIL)) {
        dump_load_detail(get_sid(), get_warp_id(), pc, inst_name, memory_op, space, cache_op, latency, issue_gap);
      }
      break;
    case OP_STG:
    case OP_STL:
      assert(data_size > 0);
      memory_op = memory_store;
      cache_op = CACHE_ALL;
      if (m_opcode == OP_STL) {
        space.set_type(local_space);
      } else {
        space.set_type(global_space);
      }
      break;
    case OP_ATOMG:
    case OP_RED:
    case OP_ATOM:
      assert(data_size > 0);
      memory_op = memory_load;
      op = LOAD_OP;
      space.set_type(global_space);
      m_isatomic = true;
      cache_op = CACHE_GLOBAL;  // all the atomics should be done at L2
      break;
    case OP_LDS:
      assert(data_size > 0);
      memory_op = memory_load;
      space.set_type(shared_space);
      if (DTRACE(LOAD_DETAIL)) {
        dump_load_detail(get_sid(), get_warp_id(), pc, inst_name, memory_op, space, cache_op, latency, issue_gap);
      }
      break;
    case OP_STS:
      assert(data_size > 0);
      memory_op = memory_store;
      space.set_type(shared_space);
      break;
    case OP_ATOMS:
      assert(data_size > 0);
      m_isatomic = true;
      memory_op = memory_load;
      space.set_type(shared_space);
      break;
    case OP_LDSM: // Load Matrix from Shared Memory
      assert(data_size > 0);
      space.set_type(shared_space);
      if (DTRACE(LOAD_DETAIL)) {
        dump_load_detail(get_sid(), get_warp_id(), pc, inst_name, memory_op, space, cache_op, latency, issue_gap);
      }      
      break;
    case OP_ST:
    case OP_LD:
      assert(data_size > 0);
      if (m_opcode == OP_LD) {
        memory_op = memory_load;
      } else {
        memory_op = memory_store;
      }
      // resolve generic loads
      if (kernel_trace_info->shmem_base_addr == 0 ||
          kernel_trace_info->local_base_addr == 0) {
        // shmem and local addresses are not set
        // assume all the mem reqs are shared by default
        space.set_type(shared_space);
        if (DTRACE(LOAD_DETAIL)) {
          dump_load_detail(get_sid(), get_warp_id(), pc, inst_name, memory_op, space, cache_op, latency, issue_gap);
        }
      } else {
        // check the first active address
        for (unsigned i = 0; i < warp_size(); ++i) {
          if (active_mask.test(i)) {
            if (trace.memadd_info->addrs[i] >= kernel_trace_info->shmem_base_addr &&
                trace.memadd_info->addrs[i] < kernel_trace_info->local_base_addr) {
              space.set_type(shared_space);
            } else if (trace.memadd_info->addrs[i] >= kernel_trace_info->local_base_addr &&
              trace.memadd_info->addrs[i] < kernel_trace_info->local_base_addr + LOCAL_MEM_SIZE_MAX) {
              space.set_type(local_space);
              cache_op = CACHE_ALL;
            } else {
              space.set_type(global_space);
              cache_op = CACHE_ALL;
            }
            if (m_opcode == OP_LD) {
              if (DTRACE(LOAD_DETAIL)) {
                dump_load_detail(get_sid(), get_warp_id(), pc, inst_name, memory_op, space, cache_op, latency, issue_gap);
              }
            }
            break;
          }
        }
      }
      break;
    case OP_BAR:
      // TO DO: fill this correctly
      bar_id = 0;
      bar_count = (u32) - 1;      
      bar_type = SYNC;
      // TO DO
      // if bar_type = RED;
      // set bar_type
      // barrier_type bar_type;
      // reduction_type red_type;
      break;
    // LDGDEPBAR is to form a group containing the previous LDGSTS instructions
    // that have not been grouped yet. In the implementation, a group number
    // will be assigned once the instruction is met.
    case OP_LDGDEPBAR:
      m_is_ldgdepbar = true;
      break;
    // DEPBAR is served as a warp-wise barrier that is only effective for LDGSTS
    // instructions. It is associated with a immediate value. The immediate
    // value indicates the last N LDGDEPBAR groups to not wait once the
    // instruction is met. For example, if the immediate value is 1, then the
    // last group is able to proceed even with DEPBAR present; if the immediate
    // value is 0, then all of the groups need to finish before proceed.
    case OP_DEPBAR:
      m_is_depbar = true;
      m_depbar_group_no = trace.imm;
      break;
    case OP_HADD2:
    case OP_HADD2_32I:
    case OP_HFMA2:
    case OP_HFMA2_32I:
    case OP_HMUL2_32I:
    case OP_HSET2:
    case OP_HSETP2:
      // FP16 has 2X throughput than FP32
      initiation_interval = initiation_interval / 2;
      // Make sure initiaion interval never goes below 1
      if (initiation_interval < 1) {
        initiation_interval = 1;
      }        
      break;
    default:
      break;
  }

  return true;
}

trace_config::trace_config() {
  printf("Inside trace_config::trace_config()...\n");
  int_latency    = 0;
  fp_latency     = 0;
  dp_latency     = 0;
  sfu_latency    = 0;
  tensor_latency = 0;
  int_init       = 0;
  fp_init        = 0;
  dp_init        = 0;
  sfu_init       = 0;
  tensor_init    = 0;
  for (size_t i = 0; i < SPECIALIZED_UNIT_NUM; i++)
  {
    specialized_unit_latency[i] = 0;
    specialized_unit_initiation[i] = 0;
  }

  g_traces_filename = nullptr;
  trace_opcode_latency_initiation_int = nullptr;
  trace_opcode_latency_initiation_sp = nullptr;
  trace_opcode_latency_initiation_dp = nullptr;
  trace_opcode_latency_initiation_sfu = nullptr;
  trace_opcode_latency_initiation_tensor = nullptr;
  for (size_t i = 0; i < SPECIALIZED_UNIT_NUM; ++i) {
    trace_opcode_latency_initiation_specialized_op[i] = nullptr;
  }
}

void trace_config::reg_options(option_parser_t opp) {
  option_parser_register(opp, "-trace", OPT_CSTR, &g_traces_filename,
                         "traces kernel file"
                         "traces kernel file directory",
                         "./traces/kernelslist.g");

  option_parser_register(opp, "-trace_opcode_latency_initiation_int", OPT_CSTR,
                         &trace_opcode_latency_initiation_int,
                         "Opcode latencies and initiation for integers in "
                         "trace driven mode <latency,initiation>",
                         "4,1");
  option_parser_register(opp, "-trace_opcode_latency_initiation_sp", OPT_CSTR,
                         &trace_opcode_latency_initiation_sp,
                         "Opcode latencies and initiation for sp in trace "
                         "driven mode <latency,initiation>",
                         "4,1");
  option_parser_register(opp, "-trace_opcode_latency_initiation_dp", OPT_CSTR,
                         &trace_opcode_latency_initiation_dp,
                         "Opcode latencies and initiation for dp in trace "
                         "driven mode <latency,initiation>",
                         "4,1");
  option_parser_register(opp, "-trace_opcode_latency_initiation_sfu", OPT_CSTR,
                         &trace_opcode_latency_initiation_sfu,
                         "Opcode latencies and initiation for sfu in trace "
                         "driven mode <latency,initiation>",
                         "4,1");
  option_parser_register(opp, "-trace_opcode_latency_initiation_tensor",
                         OPT_CSTR, &trace_opcode_latency_initiation_tensor,
                         "Opcode latencies and initiation for tensor in trace "
                         "driven mode <latency,initiation>",
                         "4,1");

  for (unsigned j = 0; j < SPECIALIZED_UNIT_NUM; ++j) {
    std::stringstream ss;
    ss << "-trace_opcode_latency_initiation_spec_op_" << j + 1;
    option_parser_register(opp, ss.str().c_str(), OPT_CSTR,
                           &trace_opcode_latency_initiation_specialized_op[j],
                           "specialized unit config"
                           " <latency,initiation>",
                           "4,4");
  }
}

void trace_config::parse_config() {
  if (trace_opcode_latency_initiation_int)
    sscanf(trace_opcode_latency_initiation_int, "%u,%u", &int_latency, &int_init);
  if (trace_opcode_latency_initiation_sp)
    sscanf(trace_opcode_latency_initiation_sp, "%u,%u", &fp_latency, &fp_init);
  if (trace_opcode_latency_initiation_dp)
    sscanf(trace_opcode_latency_initiation_dp, "%u,%u", &dp_latency, &dp_init);
  if (trace_opcode_latency_initiation_sfu)
    sscanf(trace_opcode_latency_initiation_sfu, "%u,%u", &sfu_latency, &sfu_init);
  if (trace_opcode_latency_initiation_tensor)
    sscanf(trace_opcode_latency_initiation_tensor, "%u,%u", &tensor_latency,
           &tensor_init);

  for (unsigned j = 0; j < SPECIALIZED_UNIT_NUM; ++j) {
    if (trace_opcode_latency_initiation_specialized_op[j]) {
      sscanf(trace_opcode_latency_initiation_specialized_op[j], "%u,%u",
             &specialized_unit_latency[j], &specialized_unit_initiation[j]);
    }
  }
}
void trace_config::set_latency(unsigned category, unsigned &latency,
                               unsigned &initiation_interval) const {
  initiation_interval = latency = 1;

  switch (category) {
    case ALU_OP:
    case INTP_OP:
    case BRANCH_OP:
    case CALL_OPS:
    case RET_OPS:
      latency = int_latency;
      initiation_interval = int_init;
      break;
    case SP_OP:
      latency = fp_latency;
      initiation_interval = fp_init;
      break;
    case DP_OP:
      latency = dp_latency;
      initiation_interval = dp_init;
      break;
    case SFU_OP:
      latency = sfu_latency;
      initiation_interval = sfu_init;
      break;
    case TENSOR_CORE_OP:
      latency = tensor_latency;
      initiation_interval = tensor_init;
      break;
    default:
      break;
  }
  // for specialized units
  if (category >= SPEC_UNIT_START_ID) {
    unsigned spec_id = category - SPEC_UNIT_START_ID;
    assert(spec_id >= 0 && spec_id < SPECIALIZED_UNIT_NUM);
    latency = specialized_unit_latency[spec_id];
    initiation_interval = specialized_unit_initiation[spec_id];
  }
}

void trace_gpgpu_sim::createSIMTCluster() {
  assert(m_shader_config && "m_shader_config is null in trace_gpgpu_sim::createSIMTCluster");
  assert(m_shader_config->n_simt_clusters > 0 && "n_simt_clusters must be > 0");

  m_cluster = new simt_core_cluster *[m_shader_config->n_simt_clusters];
  for (unsigned i = 0; i < m_shader_config->n_simt_clusters; i++) {
    m_cluster[i] = new trace_simt_core_cluster(
      this, i, m_shader_config, m_memory_config, m_shader_stats, m_memory_stats);
  }
}

void trace_simt_core_cluster::create_shader_core_ctx() {
  m_core = new shader_core_ctx *[m_config->n_simt_cores_per_cluster];
  for (unsigned core = 0; core < m_config->n_simt_cores_per_cluster; core++) {
    unsigned sid = m_config->cid_to_sid(core, m_cluster_id);
    if (m_config->n_simt_clusters == 1) {
      assert(sid == core);
    }
    m_core[core] = new trace_shader_core_ctx(
      m_gpu, this, sid, m_cluster_id, m_config, m_mem_config, m_stats);

    m_core_sim_order.push_back(core);

    if (DTRACE(SIM_TOP)) {
      fprintf(Trace::out, "%llu Added sim round for core[%u]\n", 
        m_gpu->get_cycle(), core);
    };    
  }
}

void trace_shader_core_ctx::create_shd_warp() {
  m_warp.resize(m_config->max_warps_per_shader);
  for (unsigned k = 0; k < m_config->max_warps_per_shader; ++k) {
    m_warp[k] = new trace_shd_warp_t(this, m_config->warp_size);
  }
}

void trace_shader_core_ctx::get_pdom_stack_top_info(unsigned warp_id,
                                                    const warp_inst_t *pI,
                                                    unsigned *pc,
                                                    unsigned *rpc) {
  // In trace-driven mode, we assume no control hazard
  assert(pI != NULL && "Unexpexted behaviour , inst should not be null");
  *pc = pI->pc;
  *rpc = pI->pc;
}

const active_mask_t &trace_shader_core_ctx::get_active_mask(
    unsigned warp_id, const warp_inst_t *pI) {
  // For Trace-driven, the active mask already set in traces, so
  // just read it from the inst
  return pI->get_active_mask();
}

unsigned trace_shader_core_ctx::sim_init_thread(
    kernel_info_t &kernel, ptx_thread_info **thread_info, int sid, unsigned tid,
    unsigned threads_left, unsigned num_threads, core_t *core,
    unsigned hw_cta_id, unsigned hw_warp_id, gpgpu_t *gpu) {
  if (kernel.no_more_ctas_to_run()) {
    return 0;  // finished!
  }

  if (kernel.more_threads_in_cta()) {
    kernel.increment_thread_id();
  }

  if (!kernel.more_threads_in_cta()) kernel.increment_cta_id();

  return 1;
}

void trace_shader_core_ctx::init_warps(unsigned cta_id, unsigned start_thread,
                                       unsigned end_thread, unsigned ctaid,
                                       int cta_size, kernel_info_t &kernel) {
  // call base class
  shader_core_ctx::init_warps(cta_id, start_thread, end_thread, ctaid, cta_size, kernel);

  // then init traces
  unsigned start_warp = start_thread / m_config->warp_size;
  unsigned end_warp = end_thread / m_config->warp_size +
                      ((end_thread % m_config->warp_size) ? 1 : 0);

  init_traces(start_warp, end_warp, kernel);
}

const warp_inst_t *trace_shader_core_ctx::get_next_inst(
  unsigned warp_id, address_type pc, bool is_pI2) {
  // read the inst from the traces
  trace_shd_warp_t *m_trace_warp = static_cast<trace_shd_warp_t *>(m_warp[warp_id]);
  m_trace_warp->set_time(m_gpu->get_cycle());
  const trace_warp_inst_t *ret = m_trace_warp->get_next_trace_inst();

  if (DTRACE(INST_TRACE)) {    
    fprintf(Trace::out, "%llu fetch_slot:%u get_next_inst for %s "
      "warp_id:%u, pc:%#llx, ret_pc:%#llx, active_mask:%s\n",
      m_gpu->get_cycle(), m_fetch_slot, 
      is_pI2 ? "pI2" : "pI1", 
      warp_id, pc, ret ? ret->pc : 0,
      ret ? ret->get_active_mask().to_string().c_str() : "N/A");
  }

  if (m_trace_warp->trace_done()) {
    if (!m_warp[warp_id]->inst_in_pipeline() &&
        m_warp[warp_id]->stores_done() &&
        !m_scoreboard->pendingWrites(warp_id)) {
      for (u32 t = 0; t < m_warp_size; t++) {
        if (m_trace_warp->is_lane_active(t)) {
          m_trace_warp->mark_lane_completed(t);
        }
      }
      m_barriers.warp_exit(warp_id);
    }
  }
  return ret;
}

void trace_shader_core_ctx::updateSIMTStack(unsigned warpId,
                                            warp_inst_t *inst) {
  // No SIMT-stack in trace-driven  mode
}

void trace_shader_core_ctx::init_traces(unsigned start_warp, unsigned end_warp,
                                        kernel_info_t &kernel) {
  std::vector<std::vector<inst_trace_t> *> threadblock_traces;
  for (unsigned i = start_warp; i < end_warp; ++i) {
    trace_shd_warp_t *m_trace_warp = static_cast<trace_shd_warp_t *>(m_warp[i]);
    m_trace_warp->clear();
    threadblock_traces.push_back(&(m_trace_warp->warp_traces));
  }
  trace_kernel_info_t &trace_kernel =
      static_cast<trace_kernel_info_t &>(kernel);
  trace_kernel.get_next_threadblock_traces(threadblock_traces);

  // set the pc from the traces and ignore the functional model
  for (unsigned i = start_warp; i < end_warp; ++i) {
    trace_shd_warp_t *m_trace_warp = static_cast<trace_shd_warp_t *>(m_warp[i]);
    m_trace_warp->set_next_pc(m_trace_warp->get_start_trace_pc());
    m_trace_warp->set_kernel(&trace_kernel);
    unsigned warp_local_idx = i - start_warp;
    int cta_threads = kernel.threads_per_cta();
    int threads_remaining =
        cta_threads - static_cast<int>(warp_local_idx * m_config->warp_size);
  unsigned active_count =
    threads_remaining > 0
      ? std::min<unsigned>(static_cast<unsigned>(threads_remaining),
                 m_config->warp_size)
      : 0;
    m_trace_warp->init_active_threads(active_count);
  }
}

void trace_shader_core_ctx::checkExecutionStatusAndUpdate(warp_inst_t &inst,
                                                          unsigned t,
                                                          unsigned tid) {
  if (inst.isatomic()) {
    m_warp[inst.get_warp_id()]->inc_n_atomic();
  }

  if (inst.space.is_local() && (inst.is_load() || inst.is_store())) {
    new_addr_type localaddrs[max_accesses_per_insn_per_tid];
    unsigned num_addrs;
    num_addrs = translate_local_memaddr(
        inst.get_addr(t), tid,
        m_config->n_simt_clusters * m_config->n_simt_cores_per_cluster,
        inst.data_size, (new_addr_type *)localaddrs);
    inst.set_addr(t, (new_addr_type *)localaddrs, num_addrs);
  }
}

void trace_shader_core_ctx::func_exec_inst(warp_inst_t &inst) {
  for (u32 t = 0; t < m_warp_size; t++) {
    if (inst.active(t)) {
      u32 tid = m_warp_size * inst.get_warp_id() + t;
      // virtual function
      checkExecutionStatusAndUpdate(inst, t, tid);
    }
  }
  // here, we generate memory acessess and set the status if thread (done?)
  if (inst.is_load() || inst.is_store()) {    
    inst.generate_mem_accesses(m_gpu->get_cycle());
  }
}

void trace_shader_core_ctx::issue_warp(register_set &warp,
                                       const warp_inst_t *pI,
                                       const active_mask_t &active_mask,
                                       unsigned warp_id, unsigned sch_id) {
  shader_core_ctx::issue_warp(warp, pI, active_mask, warp_id, sch_id);

  // delete warp_inst_t class here, it is not required anymore by gpgpu-sim
  // after issue
  delete pI;
}
