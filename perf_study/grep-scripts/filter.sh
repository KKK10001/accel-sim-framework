grep "wr L1D" trace.out > wr_l1d
grep "rd L1D" trace.out > rd_l1d
grep "global monitor" trace.out > total_access_l1d
grep "l1_lat PC=" trace.out > all_decode_inst
grep "decoded inst" trace.out > decoded_inst
grep "fetched inst" trace.out > fetched_inst
grep "ptx_inst" trace.out > ptx_inst
grep "Scheduled insn" trace.out > issued_inst
grep "squeezing bubbles" trace.out > 1_latency_queue
grep "l1_latency_queue\[bank:0" trace.out > l1_latency_queue_bank_0
grep "WR_MISS on pc" trace.out > wr_miss
grep "l1_lat_q\|WR_MISS on pc\|wr L1D\|rd L1D" trace.out > arise_l1d_miss
# follow one single pc
grep "pc=0x2580" trace.out > pc_0x2580

####################### Miss Section #######################
grep '::rd_miss_base L1D READ_REQUEST' trace.out | grep -E 'SECTOR_MISS|MISS' > l1d_rd_miss
awk '{print $7}' l1d_rd_miss > l1d_rd_miss_addr
awk '{print $1}' l1d_rd_miss > l1d_rd_miss_timestamp
grep '::rd_miss_base L2C READ_REQUEST' trace.out | grep -E 'SECTOR_MISS|MISS' > l2c_rd_miss
awk '{print $7}' l2c_rd_miss > l2c_rd_miss_addr
awk '{print $1}' l2c_rd_miss > l2c_rd_miss_timestamp
paste l2c_rd_miss_timestamp l1d_rd_miss_timestamp | awk '{print $1-$2}' > latency_l1d_rd_miss_to_l2c_rd_miss
sort latency_l1d_rd_miss_to_l2c_rd_miss | uniq -c | awk '{print $2, $1}' > latency_l1d_rd_miss_to_l2c_rd_miss_dist

####################### Tag Probe Section #######################
grep '::access L1D READ_REQUEST' trace.out | grep -E 'SECTOR_MISS|MISS' > l1d_tag_probe_rd_miss
awk '{print $7}' l1d_tag_probe_rd_miss > l1d_tag_probe_rd_miss_addr
grep '::access L2C READ_REQUEST' trace.out | grep -E 'SECTOR_MISS|MISS' > l2c_tag_probe_rd_miss
awk '{print $7}' l2c_tag_probe_rd_miss > l2c_tag_probe_rd_miss_addr

####################### Refill Section #######################
grep '::fill' trace.out > fill_cache
grep '::fill L1D' trace.out > fill_l1d
grep '::fill L2C' trace.out > fill_l2c

####################### filter *.o #######################
grep "Total_core_cache_stats_breakdown\[GLOBAL_ACC_R\]\[TOTAL_ACCESS\]" *.o
grep "Total_core_cache_stats_breakdown\[GLOBAL_ACC_R\]\[MISS\]\|Total_core_cache_stats_breakdown\[GLOBAL_ACC_R\]\[SECTOR_MISS\]" *.o 

grep "Total_core_cache_stats_breakdown\[GLOBAL_ACC_W\]\[TOTAL_ACCESS\]" *.o
