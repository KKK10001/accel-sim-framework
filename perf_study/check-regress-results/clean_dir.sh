sim_root=~/dev/accel-sim/accel-sim-framework/sim_run_12.1
log_files_dir=~/dev/accel-sim/accel-sim-framework/util/job_launching/logfiles
echo "sim_root = "$sim_root
#!/usr/bin/env bash

echo "sim_root = $sim_root"
paths=()
paths+=( "$sim_root/backprop-rodinia-2.0-ft/4096___data_result_4096_txt/QV100-SASS" )
paths+=( "$sim_root/bfs-rodinia-2.0-ft/__data_graph4096_txt___data_graph4096_result_txt/QV100-SASS" )
paths+=( "$sim_root/heartwall-rodinia-2.0-ft/__data_test_avi_1___data_result_1_txt/QV100-SASS" )
paths+=( "$sim_root/hotspot-rodinia-2.0-ft/30_6_40___data_result_30_6_40_txt/QV100-SASS" )
paths+=( "$sim_root/lud-rodinia-2.0-ft/_v__b__i___data_64_dat/QV100-SASS" )
paths+=( "$sim_root/nw-rodinia-2.0-ft/128_10___data_result_128_10_txt/QV100-SASS" )
paths+=( "$sim_root/nn-rodinia-2.0-ft/__data_filelist_4_3_30_90___data_filelist_4_3_30_90_result_txt/QV100-SASS" )
paths+=( "$sim_root/pathfinder-rodinia-2.0-ft/1000_20_5___data_result_1000_20_5_txt/QV100-SASS" )
paths+=( "$sim_root/srad_v2-rodinia-2.0-ft/__data_matrix128x128_txt_0_127_0_127__5_2___data_result_matrix128x128_1_150_1_100__5_2_txt/QV100-SASS" )
paths+=( "$sim_root/streamcluster-rodinia-2.0-ft/3_6_16_1024_1024_100_none_output_txt_1___data_result_3_6_16_1024_1024_100_none_1_txt/QV100-SASS" )

shopt -s nullglob

# regress_tag=regress-default-config-11-25-eve-debug # Congratulations! All Tests Pass!
# regress_tag=regress-miss-q-entries-32-11-25-eve-debug # Congratulations! All Tests Pass!
# regress_tag=regress-mshr-max-merge-32-11-25-eve-specify-relative-cfg-file-path #Passed:0/10, No error:1/10, Failed/Error:9/10, Running:0/10, Waiting:0/10

# regress_tag=perf-study-mshr-max-merge-32 # removed
# regress_tag=reg_scb_crf_baseline
# regress_tag=reg_warp_schedule_base
# regress_tag=reg_num_eu_64__num_sched_per_core_64__opc_64__max_insn_issue_per_warp_1
# regress_tag=reg_num_eu_16__num_sched_per_core_16__opc_16__max_insn_issue_per_warp_1
# regress_tag=reg_num_eu_8__num_sched_per_core_8__max_insn_issue_per_warp_1
# regress_tag=reg_sched_warp_when_interference_below_20
# regress_tag=reg_sched_warp_when_interference_below_5
# regress_tag=reg_sched_warp_when_interference_below_10
# regress_tag=reg_warp_interfere_awared_schedule
# regress_tag=reg_baseline_default_sched
# regress_tag=reg_warp_interfere_and_filltime_awared_schedule
# regress_tag=reg_warp_interfere_awared_cache_replace
# regress_tag=reg_warp_interfere_and_filltime_awared_cache_replace
# regress_tag=reg_warp_corr_set_indexing
# regress_tag=reg_baseline_default_sched_II
# regress_tag=reg_warp_interfere_awared_cache_replace_fixed
# regress_tag=reg_l1d_mshr_awared_repl
# regress_tag=reg_wia_warp_limiting_repl_l1d_mq_32
# regress_tag=reg_wia_two_level_active_repl_l1d_mq_32
# regress_tag=reg_l1d_l2_wia_old_repl_l1d_mq_32
# regress_tag=reg_wia_cache_repl_l1d_mq_16
# regress_tag=reg_wia_cache_repl_l1d_mq_32
# regress_tag=reg_wia_old_repl_l1d_mq_32
# regress_tag=reg_evict_l1d_low_reusage_pending_longop
# regress_tag=reg_l1d_plopa_repl_l1d_mq_32
# regress_tag=reg_chk_l1d_pending_longop_evict
# regress_tag=reg_dis_wia_repl
# regress_tag=reg_dont_cache_low_locality_lines
# regress_tag=reg_no_alloc_low_loc_lines
# regress_tag=reg_chk_assert_no_wr_event_sent_by_l1d
# regress_tag=reg_base_no_mshr
# regress_tag=reg_l1d_byp_check_flow
# regress_tag=reg_l1d_satcnt_only_inc_upb_3_gto_srad_v2
# regress_tag=reg_l1d_sat_cnt_up_bound_3_gto
# regress_tag=reg_l1d_satcnt_only_inc_upb_3_gto_srad_v2_II
# regress_tag=reg_l1d_max_evict_then_satcnt_gto_srad_v2_again
# regress_tag=reg_l1d_l2_max_evict_then_satcnt_gto_srad_v2
# regress_tag=reg_l1d_max_evict_upb_10_then_satcnt_upb_3_gto_srad_v2
# regress_tag=reg_l1d_dyn_byp_evict_bd_10_satcnt_bd_3_gto_srad_v2
# regress_tag=reg_l1d_dyn_byp_total_evict_unaware_lrr_srad_v2
# regress_tag=reg_l1d_dyn_byp_total_evict_unaware_lrr
# regress_tag=reg_l1d_dyn_byp_total_evict_aware_lrr_hotspot
# regress_tag=reg_l1d_dyn_byp_total_evict_aware_upb_5_lrr_hotspot
# regress_tag=reg_l1d_dyn_byp_total_evict_aware_upb_3_lrr_hotspot
# regress_tag=reg_l1d_dyn_byp_total_evict_aware_upb_5_gto_hotspot
regress_tag=reg_l1d_dyn_byp_total_evict_aware_upb_5_lrr_streamcluster
# regress_tag=reg_l1d_also_byp_tag_probe
# regress_tag=reg_base_no_mshr_src_nn
# regress_tag=reg_l1d_byp_fine_tune
# regress_tag=reg_l1d_byp_alway_probe
# regress_tag=reg_base_no_mshr_srad_v2
# regress_tag=reg_l1d_byp_tune_srad_v2_dec_step_1
# regress_tag=reg_l1d_bypkey_srad_v2
# regress_tag=reg_base_rm_set_addr_with_extra_mf_fields_addr
# regress_tag=reg_l1d_also_byp_probe_srad_v2
# regress_tag=reg_l1d_byp_tune_srad_v2_dec_step_2
# regress_tag=reg_l1d_byp_fine_tune_srad_v2
# regress_tag=reg_l1d_byp_detect_f2e_gap_conf_cnt
# regress_tag=reg_l1d_bypass_fixed_thrash_threshold
# regress_tag=reg_l1d_bypass_low_loc_threshold_5_lines
# regress_tag=reg_l1d_bypass_low_loc_threshold_50_lines
# regress_tag=reg_l1d_mpki_aware_bypass
# regress_tag=reg_l1d_byp_adaptive_tune_low_loc_thres
# regress_tag=reg_l1d_bypass_low_loc_lines_II
# regress_tag=reg_l1d_bypass_low_loc_blk_addr
# regress_tag=reg_l1d_smart_byp
# regress_tag=reg_l1d_byp_fuck_check
# regress_tag=reg_byp_trash_over_3_for_l1d
# regress_tag=reg_l1d_bypass_low_loc_lines
# regress_tag=reg_byp_trashed_req_for_l1d
# regress_tag=reg_dont_cache_low_loc_ln_II
# regress_tag=reg_wia_cache_repl_l1d_mq_64
# regress_tag=reg_mshr_disable_all_lru_enhanced_with_timestamp_and_total_hits
# regress_tag=reg_baseline_fixed_mshr_corr_repl
# regress_tag=reg_test_l2_wia_worked
# regress_tag=reg_wia_cache_repl_base
# regress_tag=reg_wia_old_repl_l1d_mq_16
# regress_tag=reg_mshr_en_and_aware_all_lru_enhanced_with_timestamp
# regress_tag=reg_warp_interfere_awared_cache_replace_fixed_mshr_awared_repl
# regress_tag=reg_max_insn_issue_per_warp_2
# regress_tag=reg_num_int_units_8_num_sched_per_core_8
# regress_tag=perf-study-miss-q-entries-32
# regress_tag=reg_warp_interfere_awared_schedule_l1d_l2
# regress_tag=reg_warp_interfere_awared_schedule_050_picker
# regress_tag=reg_warp_interfere_mid_awared_schedule
# regress_tag=reg_re_ref_interval_aware_for_l2_srrip_mshr_aware

rm -f -- $log_files_dir/*$regress_tag*

counter=0
zero_count=0
missing_dirs=0
for path in "${paths[@]}"; do
    counter=$((counter + 1))
    case_dir="$path/$regress_tag"
    echo "Ready to remove directory: $case_dir"
    rm -rf "$case_dir"
    echo "Removed directory: $case_dir"
done
