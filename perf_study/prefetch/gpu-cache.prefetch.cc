// -----------------------------------------------------------------------------
// Stride Prefetch Prototype -- Source Side (based on gpu-cache.cc)
// -----------------------------------------------------------------------------
// The snippets below mirror the changes that would be required in the real
// gpu-cache.cc implementation. They assume the declarations from
// gpu-cache.prefetch.h have been merged into the live headers.
// -----------------------------------------------------------------------------

#include "gpu-cache.prefetch.h"

#include <algorithm>
#include <limits>
#include <list>

#include "../../gpu-simulator/gpgpu-sim/src/gpgpu-sim/gpu-sim.h"
#include "../../gpu-simulator/gpgpu-sim/src/gpgpu-sim/mem_fetch.h"

// -----------------------------------------------------------------------------
// 1) baseline_cache hook implementation
// -----------------------------------------------------------------------------
void baseline_cache::service_prefetch(unsigned long long) {
  // Default behaviour: no-op. Data/texture caches can override as needed.
}

// -----------------------------------------------------------------------------
// 2) data_cache helpers
// -----------------------------------------------------------------------------
bool data_cache::prefetch_enabled() const {
  return m_prefetch_cfg.enabled;
}

void data_cache::record_prefetch_feedback(new_addr_type block_addr,
                                          enum cache_request_status probe_status,
                                          enum cache_request_status access_status,
                                          unsigned long long /*time*/) {
  auto it = m_prefetch_lines.find(block_addr);
  if (it == m_prefetch_lines.end()) return;

  if (probe_status == HIT || probe_status == HIT_RESERVED ||
      access_status == HIT) {
    if (it->second.issued)
      m_prefetch_stats.useful++;
    else
      m_prefetch_stats.redundant++;
    m_prefetch_lines.erase(it);
    return;
  }

  if ((access_status == MISS || access_status == SECTOR_MISS) &&
      !it->second.issued) {
    // Demand miss re-observed before the speculative request ever launched;
    // count it as "late" and let the demand access proceed normally.
    m_prefetch_stats.late++;
    m_prefetch_lines.erase(it);
  }
}

void data_cache::handle_prefetch_generation(new_addr_type block_addr,
                                            mem_fetch *mf,
                                            enum cache_request_status /*probe_status*/,
                                            enum cache_request_status access_status,
                                            unsigned long long time) {
  if (!prefetch_enabled()) return;
  if (mf->get_is_write()) return;
  if (!(access_status == MISS || access_status == SECTOR_MISS)) return;

  update_stride_tracker(mf->get_wid(), block_addr);
  const stride_tracker_state &entry = m_stride_tracker[mf->get_wid()];

  if (!entry.valid) return;
  if (entry.stride == 0) return;
  if (entry.confidence < m_prefetch_cfg.confidence_threshold) return;

  for (unsigned i = 1; i <= m_prefetch_cfg.degree; ++i) {
    long long offset = static_cast<long long>(entry.stride) *
                       static_cast<long long>(i * m_prefetch_cfg.distance);
    long long candidate_block = static_cast<long long>(block_addr) + offset;
    if (candidate_block < 0) continue;
    enqueue_prefetch_candidate(static_cast<new_addr_type>(candidate_block), mf,
                               time);
  }
}

void data_cache::update_stride_tracker(unsigned wid, new_addr_type block_addr) {
  stride_tracker_state &entry = m_stride_tracker[wid];
  if (!entry.valid) {
    entry.valid = true;
    entry.last_block_addr = block_addr;
    entry.stride = 0;
    entry.confidence = 0;
    return;
  }

  long long delta = static_cast<long long>(block_addr) -
                    static_cast<long long>(entry.last_block_addr);
  if (delta == 0) {
    entry.last_block_addr = block_addr;
    return;
  }

  if (delta == entry.stride) {
    if (entry.confidence < std::numeric_limits<unsigned>::max())
      entry.confidence++;
  } else {
    entry.stride = delta;
    entry.confidence = 1;
  }
  entry.last_block_addr = block_addr;
}

bool data_cache::enqueue_prefetch_candidate(new_addr_type block_addr,
                                            mem_fetch *mf,
                                            unsigned long long time) {
  if (m_prefetch_lines.count(block_addr)) return false;
  if (m_prefetch_queue.size() >= m_prefetch_cfg.queue_size) {
    m_prefetch_stats.expired++;  // treat overflow as an expired opportunity
    return false;
  }

  prefetch_candidate cand;
  cand.block_addr = block_addr;
  cand.access_type = mf->get_access_type();
  cand.warp_mask = mf->get_access_warp_mask();
  cand.byte_mask = mf->get_access_byte_mask();
  cand.sector_mask = mf->get_access_sector_mask();
  cand.wid = mf->get_wid();
  cand.sid = mf->get_sid();
  cand.tpc = mf->get_tpc();
  cand.stream_id = mf->get_streamID();
  cand.enqueue_time = time;

  if (!cand.byte_mask.any()) cand.byte_mask.set();
  if (!cand.sector_mask.any()) cand.sector_mask.set();

  m_prefetch_queue.push_back(cand);

  prefetch_line_state state;
  state.enqueue_cycle = time;
  m_prefetch_lines.emplace(block_addr, state);
  m_prefetch_stats.scheduled++;
  return true;
}

bool data_cache::issue_prefetch_candidate(const prefetch_candidate &candidate,
                                          unsigned cache_index,
                                          unsigned long long time) {
  if (count_outstanding_prefetches() >= m_prefetch_cfg.max_outstanding)
    return false;

  mem_access_byte_mask_t byte_mask = candidate.byte_mask;
  mem_access_sector_mask_t sector_mask = candidate.sector_mask;
  if (!byte_mask.any()) byte_mask.set();
  if (!sector_mask.any()) sector_mask.set();

  mem_fetch *pref_mf = m_memfetch_creator->alloc(
      candidate.block_addr, candidate.access_type, candidate.warp_mask,
      byte_mask, sector_mask, m_config.get_atom_sz(), false,
      m_gpu->gpu_tot_sim_cycle + m_gpu->gpu_sim_cycle, candidate.wid,
      candidate.sid, candidate.tpc, NULL, candidate.stream_id);

  bool do_miss = false;
  bool wb = false;
  evicted_block_info evicted;
  std::list<cache_event> dummy_events;

  send_read_request(candidate.block_addr, candidate.block_addr, cache_index,
                    pref_mf, time, do_miss, wb, evicted, dummy_events, false,
                    false);

  if (!do_miss) {
    delete pref_mf;
    return false;
  }

  prefetch_line_state &line = m_prefetch_lines[candidate.block_addr];
  line.issue_cycle = time;
  line.issued = true;
  if (line.pending_misses < std::numeric_limits<unsigned>::max())
    line.pending_misses++;

  m_prefetch_stats.issued++;
  return true;
}

void data_cache::prune_prefetch_entries(unsigned long long time) {
  if (!m_prefetch_cfg.lifetime) return;
  for (auto it = m_prefetch_lines.begin(); it != m_prefetch_lines.end();) {
    const prefetch_line_state &state = it->second;
    unsigned long long base = state.issued ? state.issue_cycle
                                           : state.enqueue_cycle;
    if (base && time - base > m_prefetch_cfg.lifetime) {
      m_prefetch_stats.expired++;
      it = m_prefetch_lines.erase(it);
    } else {
      ++it;
    }
  }
}

unsigned data_cache::count_outstanding_prefetches() const {
  unsigned total = 0;
  for (const auto &kv : m_prefetch_lines) {
    if (kv.second.issued) total += kv.second.pending_misses;
  }
  return total;
}

void data_cache::service_prefetch(unsigned long long time) {
  if (!prefetch_enabled()) return;

  prune_prefetch_entries(time);
  if (m_prefetch_queue.empty()) return;

  unsigned attempts = 0;
  while (!m_prefetch_queue.empty()) {
    const prefetch_candidate &cand = m_prefetch_queue.front();

    auto line_it = m_prefetch_lines.find(cand.block_addr);
    if (line_it == m_prefetch_lines.end()) {
      m_prefetch_queue.pop_front();
      continue;
    }

    unsigned cache_index = (unsigned)-1;
    mem_access_sector_mask_t sector_mask = cand.sector_mask;
    if (!sector_mask.any()) sector_mask.set();
    enum cache_request_status status =
        m_tag_array->probe(cand.block_addr, cache_index, sector_mask, false,
                           time, false, NULL);

    if (status == HIT || status == HIT_RESERVED) {
      m_prefetch_stats.redundant++;
      m_prefetch_lines.erase(line_it);
      m_prefetch_queue.pop_front();
      continue;
    }

    if (miss_queue_full(m_prefetch_cfg.miss_queue_reservation)) break;

    if (issue_prefetch_candidate(cand, cache_index, time)) {
      attempts++;
      m_prefetch_queue.pop_front();
    } else {
      break;
    }

    if (attempts >= m_prefetch_cfg.degree) break;
  }
}

// -----------------------------------------------------------------------------
// 3) Modified access() front-end (call the helper hooks)
// -----------------------------------------------------------------------------
enum cache_request_status data_cache::access(new_addr_type addr, mem_fetch *mf,
                                             unsigned long long time,
                                             std::list<cache_event> &events) {
  assert(mf->get_data_size() <= m_config.get_atom_sz());
  bool wr = mf->get_is_write();
  new_addr_type block_addr = m_config.block_addr(addr);
  unsigned cache_index = (unsigned)-1;
  enum cache_request_status probe_status =
      m_tag_array->probe(block_addr, cache_index, mf,
                         mf->is_write(), time, true);
  enum cache_request_status access_status =
      process_tag_probe(wr, probe_status, addr, cache_index, mf, time, events);

  if (prefetch_enabled()) {
    record_prefetch_feedback(block_addr, probe_status, access_status, time);
    handle_prefetch_generation(block_addr, mf, probe_status, access_status,
                               time);
  }

  m_stats.inc_stats(mf->get_access_type(),
                    m_stats.select_stats_status(probe_status, access_status),
                    mf->get_streamID());
  m_stats.inc_stats_pw(mf->get_access_type(),
                       m_stats.select_stats_status(probe_status, access_status),
                       mf->get_streamID());

  return access_status;
}
