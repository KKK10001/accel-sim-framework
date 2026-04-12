#include "accel-sim.h"
#include "accelsim_version.h"
#include "gpgpu-sim/src/trace.h"

accel_sim_framework::accel_sim_framework(std::string config_file,
                                          std::string trace_file) {
  std::cout << "Accel-Sim [build " << g_accelsim_version << "]";
  m_gpgpu_context = new gpgpu_context();

  // mimic argv
  unsigned argc = 5;
  const char *argv[] = {"accel-sim.out", "-config", config_file.c_str(),
                        "-trace", trace_file.c_str()};

  m_gpgpu_sim = gpgpu_trace_sim_init_perf_model(argc, argv, m_gpgpu_context, &tconfig);
  m_gpgpu_sim->init();

  tracer = trace_parser(tconfig.get_traces_filename());

  tconfig.parse_config();

  init();
}

accel_sim_framework::accel_sim_framework(int argc, const char **argv) {
  std::cout << "Accel-Sim [build " << g_accelsim_version << "]";
  m_gpgpu_context = new gpgpu_context();

  m_gpgpu_sim = gpgpu_trace_sim_init_perf_model(argc, argv, m_gpgpu_context, &tconfig);
  m_gpgpu_sim->init();

  tracer = trace_parser(tconfig.get_traces_filename());

  tconfig.parse_config();

  init();
}

void accel_sim_framework::simulation_loop() {
  // for each kernel
  // load file
  // parse and create kernel info
  // launch
  // while loop till the end of the end kernel execution
  // prints stats

  while (commandlist_index < commandlist.size() || !kernels_info.empty()) {
    u32 prev_cmdlist_idx  = commandlist_index;
    u32 prev_cmdlist_size = commandlist.size();
    bool kernel_was_not_empty = !kernels_info.empty();
    parse_commandlist();

    // Launch all kernels within window that are on a stream that isn't already
    // running
    for (auto k : kernels_info) {
      bool stream_busy = false;
      for (auto s : busy_streams) {
        if (s == k->get_cuda_stream_id()) stream_busy = true;
      }
      if (!stream_busy && m_gpgpu_sim->can_start_kernel() &&
          !k->was_launched()) {
        // In trace-driven mode, prefer the kernel name from the trace header to avoid
        // relying on function_info name plumbing which may be unset in some builds.
        const char *trace_kernel_name = "<unknown>";
        if (k && k->get_trace_info()) {
          trace_kernel_name = k->get_trace_info()->kernel_name.c_str();
        }
        std::cout << "launching kernel name: " << trace_kernel_name
                  << " uid: " << k->get_uid()
                  << " cuda_stream_id: " << k->get_cuda_stream_id()
                  << std::endl;
        m_gpgpu_sim->launch(k);
        k->set_launched();
        busy_streams.push_back(k->get_cuda_stream_id());
      }
    }

    unsigned finished_kernel_uid = simulate();
    u64 finished_kernel_cuda_stream_id = (u64) - 1;
    // if (DTRACE(SIM_LOOP)) {
    //   fprintf(Trace::out, "commandlist_index:%u < commandlist.size:%lu "
    //     "!kernels_info.empty:%u. finished_kernel_uid:%u = simulate()\n",
    //     commandlist_index, commandlist.size(), !kernels_info.empty(),
    //     finished_kernel_uid);
    // }
    fprintf(Trace::out, "(prev_cmdlist_idx:%u < prev_cmdlist_size:%u) "
      "|| kernel_was_not_empty:%u -> finished_kernel_uid:%u = simulate()\n",
      prev_cmdlist_idx, prev_cmdlist_size, kernel_was_not_empty,
      finished_kernel_uid);

    // cleanup finished kernel
    std::string active_type = "";
    if (finished_kernel_uid || m_gpgpu_sim->cycle_insn_cta_max_hit() ||
        !m_gpgpu_sim->active(active_type)) {
      if (DTRACE(KERNEL_STATS)) { // 12-22
        fprintf(Trace::out, "%llu cleanup(finished_kernel_uid:%u)\n", 
          m_gpgpu_sim->gpu_tot_sim_cycle + m_gpgpu_sim->gpu_sim_cycle,
          finished_kernel_uid);
      }      
      cleanup(finished_kernel_uid, finished_kernel_cuda_stream_id);
    }

    if (sim_cycles) {
      m_gpgpu_sim->update_stats(finished_kernel_uid, finished_kernel_cuda_stream_id);
      m_gpgpu_context->print_simulation_time();
    }

    if (m_gpgpu_sim->cycle_insn_cta_max_hit()) {
      printf(
          "GPGPU-Sim: ** break due to reaching the maximum cycles (or "
          "instructions) **\n");
      fflush(stdout);
      break;
    }
  } // while (commandlist_index < commandlist.size() || !kernels_info.empty()) {
}

void accel_sim_framework::dump_commandlist() {
  for (unsigned i = 0; i < commandlist.size(); i++) {
    std::cout << "commandlist[" << i << "] = {cmd: " << 
    commandlist[i].command_string << ", type: " << 
    command_type_str(commandlist[i].m_type) << "}" << std::endl;
  }
}

void accel_sim_framework::parse_commandlist() {
  // gulp up as many commands as possible - either cpu_gpu_mem_copy
  // or kernel_launch - until the vector "kernels_info" has reached
  // the window_size or we have read every command from commandlist
  while (kernels_info.size() < window_size && commandlist_index < commandlist.size()) {
    trace_kernel_info_t *kernel_info = NULL;
    if (commandlist[commandlist_index].m_type == command_type::cpu_gpu_mem_copy) {
      size_t addre, Bcount;
      tracer.parse_memcpy_info(commandlist[commandlist_index].command_string, addre, Bcount);
      std::cout << "launching memcpy command : "
                << commandlist[commandlist_index].command_string << std::endl;
      m_gpgpu_sim->perf_memcpy_to_gpu(addre, Bcount);
      commandlist_index++;
    } else if (commandlist[commandlist_index].m_type == command_type::kernel_launch) {
      // Read trace header info for window_size number of kernels
      kernel_trace_t *kernel_trace_info =
          tracer.parse_kernel_info(commandlist[commandlist_index].command_string);
      kernel_info = create_kernel_info(kernel_trace_info, m_gpgpu_context,
                                       &tconfig, &tracer);
      kernels_info.push_back(kernel_info);
      std::cout << "Header info loaded for kernel command : "
                << commandlist[commandlist_index].command_string << std::endl;
      commandlist_index++;
    } else {
      // unsupported commands will fail the simulation
      assert(0 && "Undefined Command");
    }
  }
}

void accel_sim_framework::cleanup(u32 finished_kernel, u64& finished_kernel_cuda_stream_id) {
  trace_kernel_info_t *k = NULL;
  for (unsigned j = 0; j < kernels_info.size(); j++) {
    std::string active_type = "";
    k = kernels_info.at(j);
    if (k->get_uid() == finished_kernel ||
        m_gpgpu_sim->cycle_insn_cta_max_hit() || !m_gpgpu_sim->active(active_type)) {
      for (unsigned int l = 0; l < busy_streams.size(); l++) {
        if (busy_streams.at(l) == k->get_cuda_stream_id()) {
          finished_kernel_cuda_stream_id = k->get_cuda_stream_id();
          busy_streams.erase(busy_streams.begin() + l);
          break;
        }
      }
      tracer.kernel_finalizer(k->get_trace_info());
      delete k->entry();
      delete k;
      kernels_info.erase(kernels_info.begin() + j);
      if (!m_gpgpu_sim->cycle_insn_cta_max_hit() && m_gpgpu_sim->active(active_type)) {
        break;
      }        
    }
  }
  assert(k);  
}

unsigned accel_sim_framework::simulate() {
  unsigned finished_kernel_uid = 0;
  do {
    std::string active_type = "";
    if (!m_gpgpu_sim->active(active_type)) {
      break;
    }

    // performance simulation
    if (m_gpgpu_sim->active(active_type)) {
      m_gpgpu_sim->cycle();
      sim_cycles = true;
      m_gpgpu_sim->deadlock_check();
    } else {
      if (m_gpgpu_sim->cycle_insn_cta_max_hit()) {
        m_gpgpu_context->the_gpgpusim->g_stream_manager
            ->stop_all_running_kernels();
        break;
      }
    }
    active = m_gpgpu_sim->active(active_type);
    finished_kernel_uid = m_gpgpu_sim->finished_kernel();
  } while (active && !finished_kernel_uid);
  return finished_kernel_uid;
}

trace_kernel_info_t *accel_sim_framework::create_kernel_info(kernel_trace_t *kernel_trace_info,
                                        gpgpu_context *m_gpgpu_context,
                                        trace_config *config,
                                        trace_parser *parser) {
  gpgpu_ptx_sim_info info;
  info.smem = kernel_trace_info->shmem;
  info.regs = kernel_trace_info->nregs;
  dim3 gridDim(kernel_trace_info->grid_dim_x, kernel_trace_info->grid_dim_y,
               kernel_trace_info->grid_dim_z);
  dim3 blockDim(kernel_trace_info->tb_dim_x, kernel_trace_info->tb_dim_y,
                kernel_trace_info->tb_dim_z);
  trace_function_info *function_info =
      new trace_function_info(info, m_gpgpu_context);
  function_info->set_name(kernel_trace_info->kernel_name.c_str());
  trace_kernel_info_t *kernel_info = new trace_kernel_info_t(
      gridDim, blockDim, function_info, parser, config, kernel_trace_info);

  return kernel_info;
}

gpgpu_sim *accel_sim_framework::gpgpu_trace_sim_init_perf_model(
    int argc, const char *argv[], gpgpu_context *m_gpgpu_context,
    trace_config *m_config) {
  srand(1);
  print_splash();

  option_parser_t opp = option_parser_create();
  m_gpgpu_context->ptx_reg_options(opp);
  m_gpgpu_context->func_sim->ptx_opcocde_latency_options(opp);

  icnt_reg_options(opp);

  m_gpgpu_context->the_gpgpusim->g_the_gpu_config = new gpgpu_sim_config(m_gpgpu_context);
  m_gpgpu_context->the_gpgpusim->g_the_gpu_config->reg_options(opp);  // register GPU microrachitecture options
  m_config->reg_options(opp);

  option_parser_cmdline(opp, argc, argv);  // parse configuration options
  fprintf(stdout, "GPGPU-Sim: Configuration options:\n\n");
  option_parser_print(opp, stdout);
  // ROLLBACK_MARKER(leak-fix-2026-02-21): destroy parser after options are
  // parsed/printed to avoid leaking OptionParser and registered option objects.
  // Remove this call to restore previous lifetime behavior.
  option_parser_destroy(opp);
  // Initialize Trace streams and optional output redirection after parsing
  // configuration. Without this, -trace_enabled/-trace_components won't emit.
  if (Trace::enabled) {
    Trace::init();
  }  
  // Set the Numeric locale to a standard locale where a decimal point is a
  // "dot" not a "comma" so it does the parsing correctly independent of the
  // system environment variables
  assert(setlocale(LC_NUMERIC, "C"));
  m_gpgpu_context->the_gpgpusim->g_the_gpu_config->init();

  m_gpgpu_context->the_gpgpusim->g_the_gpu = new trace_gpgpu_sim
      (*(m_gpgpu_context->the_gpgpusim->g_the_gpu_config), m_gpgpu_context);

  m_gpgpu_context->the_gpgpusim->g_stream_manager =
      new stream_manager((m_gpgpu_context->the_gpgpusim->g_the_gpu),
                         m_gpgpu_context->func_sim->g_cuda_launch_blocking);

  m_gpgpu_context->the_gpgpusim->g_simulation_starttime = time((time_t *)NULL);

  return m_gpgpu_context->the_gpgpusim->g_the_gpu;
}