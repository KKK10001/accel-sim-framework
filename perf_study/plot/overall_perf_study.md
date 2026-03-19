# Overall Performance Study

|study|IPC|L1D_RD_MISSES|L1D_READS|L1D_RD_MISS_RATE|L1D_N_FILL_TO_EVICT_LINES|l1d_avg_rd_byp_act|l1d_avg_rd_byp_deact|avg_l1d_rd_miss_served_cycles|intra_warp_interferences|inter_warp_interferences|inter_wi_percent|non_valid_percent|dep_chk_fail_percent|pipe_stalled_percent|total_issue_ratio|total_issue_fails|g_acc_r_mq_full|issue_bw_utilization|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|base-config|120.463|23036.890|30491.162|0.756|3219.070|NA|NA|795.507|595.246|13493.343|0.958|0.006|0.198|0.381|6.875|2066452.837|35877.747|0.430|
|reg_base_no_mshr_srad_v2|120.463 (+0.000%)|23036.890 (+0.000%)|30491.162 (+0.000%)|0.756 (+0.000%)|3219.070 (+0.000%)|NA|NA|795.507 (+0.000%)|595.246 (+0.000%)|13493.343 (+0.000%)|0.958 (+0.000%)|0.006 (+0.000%)|0.198 (+0.000%)|0.381 (+0.000%)|6.875 (+0.000%)|2066452.837 (+0.000%)|35877.747 (+0.000%)|0.430 (+0.000%)|