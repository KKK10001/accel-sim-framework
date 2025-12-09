// -----------------------------------------------------------------------------
// Stride Prefetch Prototype -- Header Side (based on gpu-cache.h)
// -----------------------------------------------------------------------------
// This file contains only the sections of gpu-cache.h that need to be amended
// when wiring a simple stride-based data prefetcher into GPGPU-Sim. Everything
// else in the original header remains unchanged.
// -----------------------------------------------------------------------------

#ifndef GPU_CACHE_PREFETCH_PROTOTYPE_H
#define GPU_CACHE_PREFETCH_PROTOTYPE_H

#include <deque>
#include <string>
#include <unordered_map>
#include <unordered_set>

#include "../../gpu-simulator/gpgpu-sim/src/gpgpu-sim/gpu-cache.h"

// -----------------------------------------------------------------------------
// 1) New helper configuration structure (place near the top-level defines)
// -----------------------------------------------------------------------------
struct stride_prefetch_config {
  stride_prefetch_config()
      : enabled(false),
        degree(1),
        distance(1),
        queue_size(16),
        confidence_threshold(2),
        lifetime(512),
        max_outstanding(16),
        miss_queue_reservation(1) {}

  bool enabled;                    // enable/disable stride prefetch
  unsigned degree;                 // number of forward strides to request
  unsigned distance;               // stride multiplier per degree step
  unsigned queue_size;             // cap for queued speculative addresses
  unsigned confidence_threshold;   // minimum repeat count before issuing
  unsigned lifetime;               // cycles before expiring stale requests
  unsigned max_outstanding;        // limit concurrent prefetches in flight
  unsigned miss_queue_reservation; // keep at least N entries for demand miss
};

// -----------------------------------------------------------------------------
// 2) cache_config additions (merge into the class definition)
// -----------------------------------------------------------------------------
class cache_config {
 public:
  cache_config()
      : m_valid(false),
        m_disabled(false),
        m_config_string(NULL),
        m_config_stringPrefL1(NULL),
        m_config_stringPrefShared(NULL),
        m_data_port_width(0),
        m_set_index_function(LINEAR_SET_FUNCTION),
        m_is_streaming(false),
        m_wr_percent(0),
        m_stride_prefetch_cfg() {}

  void configure_stride_prefetch(const stride_prefetch_config &cfg) {
    m_stride_prefetch_cfg = cfg;
  }

  stride_prefetch_config get_stride_prefetch_config() const {
    return m_stride_prefetch_cfg;
  }

  bool stride_prefetch_enabled() const {
    return m_stride_prefetch_cfg.enabled;
  }

  // ... existing public members stay untouched ...

 protected:
  // ... existing protected fields ...
  stride_prefetch_config m_stride_prefetch_cfg;
};

// -----------------------------------------------------------------------------
// 3) baseline_cache hook (extend class definition)
// -----------------------------------------------------------------------------
class baseline_cache : public cache_t {
 public:
  // ... existing API ...

   virtual void service_prefetch(unsigned long long time);

 protected:
  // ... existing protected members ...
};

// -----------------------------------------------------------------------------
// 4) data_cache augmentations (conf/queues/statistics)
// -----------------------------------------------------------------------------
class data_cache : public baseline_cache {
 public:
  data_cache(const char *name, cache_config &config, int core_id, int type_id,
             mem_fetch_interface *memport, mem_fetch_allocator *mfcreator,
             enum mem_fetch_status status, mem_access_type wr_alloc_type,
             mem_access_type wrbk_type, class gpgpu_sim *gpu,
             enum cache_gpu_level level)
      : baseline_cache(name, config, core_id, type_id, memport, status, level,
                       gpu),
        m_prefetch_cfg(config.get_stride_prefetch_config()) {
    init(mfcreator);
    m_wr_alloc_type = wr_alloc_type;
    m_wrbk_type = wrbk_type;
    m_gpu = gpu;
  }

  virtual enum cache_request_status access(new_addr_type addr, mem_fetch *mf,
                                           unsigned long long time,
                                           std::list<cache_event> &events);

  virtual void service_prefetch(unsigned long long time);

 protected:
  bool prefetch_enabled() const;
  void record_prefetch_feedback(new_addr_type block_addr,
                                enum cache_request_status probe_status,
                                enum cache_request_status access_status,
                                unsigned long long time);
  void handle_prefetch_generation(new_addr_type block_addr, mem_fetch *mf,
                                  enum cache_request_status probe_status,
                                  enum cache_request_status access_status,
                                  unsigned long long time);
  void update_stride_tracker(unsigned wid, new_addr_type block_addr);
  bool enqueue_prefetch_candidate(new_addr_type block_addr, mem_fetch *mf,
                                  unsigned long long time);
  bool issue_prefetch_candidate(const struct prefetch_candidate &candidate,
                                unsigned cache_index,
                                unsigned long long time);
  void prune_prefetch_entries(unsigned long long time);
  unsigned count_outstanding_prefetches() const;

  struct stride_tracker_state {
    stride_tracker_state()
        : valid(false), last_block_addr(0), stride(0), confidence(0) {}
    bool valid;
    new_addr_type last_block_addr;
    long long stride;
    unsigned confidence;
  };

  struct prefetch_candidate {
    new_addr_type block_addr;
    mem_access_type access_type;
    active_mask_t warp_mask;
    mem_access_byte_mask_t byte_mask;
    mem_access_sector_mask_t sector_mask;
    unsigned wid;
    unsigned sid;
    unsigned tpc;
    unsigned long long stream_id;
    unsigned long long enqueue_time;
  };

  struct prefetch_line_state {
    prefetch_line_state()
        : enqueue_cycle(0), issue_cycle(0), issued(false), pending_misses(0) {}
    unsigned long long enqueue_cycle;
    unsigned long long issue_cycle;
    bool issued;
    unsigned pending_misses;
  };

  struct prefetch_stats_t {
    prefetch_stats_t()
        : scheduled(0), issued(0), useful(0), redundant(0), expired(0),
          late(0) {}
    unsigned long long scheduled;
    unsigned long long issued;
    unsigned long long useful;
    unsigned long long redundant;
    unsigned long long expired;
    unsigned long long late;
  };

  stride_prefetch_config m_prefetch_cfg;
  std::unordered_map<unsigned, stride_tracker_state> m_stride_tracker;
  std::deque<prefetch_candidate> m_prefetch_queue;
  std::unordered_map<new_addr_type, prefetch_line_state> m_prefetch_lines;
  prefetch_stats_t m_prefetch_stats;
};

#endif  // GPU_CACHE_PREFETCH_PROTOTYPE_H
