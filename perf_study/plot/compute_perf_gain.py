#!/usr/bin/env python3
"""
compute_perf_gain.py

Generates performance gain outputs comparing base vs tuned variant:
    - Text (legacy): perf_gain.txt
    - CSV: perf_gain.csv
    - Markdown: perf_gain.md (tables per benchmark + summary)
    - Fail cause breakdown (sorted): fail_cause_breakdown.xlsx

Metrics:
    IPC, GLOBAL_ACC_R fail count, GLOBAL_ACC_W fail count.
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants regress-default-cfg-11-25-eve fuck-perf-study-mshr-max-merge-32 \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx  

python3 compute_perf_gain.py \
  --variants \
    regress-default-cfg-11-25-eve \
    perf-study-miss-q-ent-32-and-mshr-max-merge-32 \
    perf-study-miss-q-ent-64-and-mshr-max-merge-32 \
    perf-study-miss-q-ent-128-and-mshr-max-merge-32 \
    perf-study-miss-q-ent-256-and-mshr-max-merge-32 \
    perf-study-miss-q-ent-288-and-mshr-max-merge-32 \
    perf-study-miss-q-ent-320-and-mshr-max-merge-32 \
    perf-study-miss-q-ent-352-and-mshr-max-merge-32 \
    perf-study-miss-q-ent-384-and-mshr-max-merge-32 \
    perf-study-miss-q-ent-512-and-mshr-max-merge-32 \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants \
    regress-default-cfg-11-25-eve \
    perf-study-miss-q-ent-32-and-mshr-max-merge-32 \
    perf-study-miss-q-ent-64-and-mshr-max-merge-32 \
    perf-study-miss-q-ent-128-and-mshr-max-merge-32 \
    perf-study-miss-q-ent-256-and-mshr-max-merge-32 \
    perf-study-miss-q-ent-288-and-mshr-max-merge-32 \
    perf-study-miss-q-ent-320-and-mshr-max-merge-32 \
    perf-study-miss-q-ent-352-and-mshr-max-merge-32 \
    perf-study-miss-q-ent-384-and-mshr-max-merge-32 \
    perf-study-miss-q-ent-512-and-mshr-max-merge-32 \
    perf-study-gpgpusim-iter-II-mshr-entries-1024 \
    perf-study-dse-iter-II-mshr-ent-1024-mq-ent-wp-wb \
    perf-study-dse-iter-II-mshr-ent-1024-miss-q-ent-512-mq-ent-wp-wb \
    perf-study-dse-iter-II-mshr-ent-1024-miss-q-ent-1024-mq-ent-wp-wb \
    perf-study-dse-iter-II-mshr-ent-1024-miss-q-ent-768-mq-ent-wp-wb \
    perf-study-dse-iter-II-mshr-ent-1024-miss-q-ent-640-mq-ent-wp-wb \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants \
    regress-default-cfg-11-25-eve \
    l2_max_merge_zero \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

########################################### Begin of L2 Perf. Study ###########################################
python3 compute_perf_gain.py \
  --variants \
    reg_check_2026_1_1_again \
    regress_no_conservative_reply_l1 \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants \
    regress_no_mshr_l2_dram_q_size_8 \
    regress_no_mshr_l2_dram_q_size_64 \
    regress_l2_dram_q_size_8 \
    regress_l2_dram_q_size_64 \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

  python3 compute_perf_gain.py \
  --variants \
    regress_disable_mshr \
    regress_enable_mshr \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

  python3 compute_perf_gain.py \
  --variants \
    regress_disable_mshr_l2_correlation \
    regress_disable_mshr_l1p5_correlation \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx  

  python3 compute_perf_gain.py \
  --variants \
    regress_disable_mshr_l2_correlation \
    regress_enable_mshr_l2_correlation \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx    

  python3 compute_perf_gain.py \
  --variants \
    regress_disable_mshr \
    regress_enable_mshr \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx  

# +14% IPC 
python3 compute_perf_gain.py \
  --variants \
    regress_disable_mshr_use_macro_again \
    regress_enable_mshr_use_macro_again \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx  

# Just to check if diff existed even if MSHR be enabled (no diff)
python3 compute_perf_gain.py \
  --variants \
    regress_enable_mshr \
    regress_enable_mshr_use_macro_again \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

# Check if diff existed in between {config, macro} when MSHR being disabled
python3 compute_perf_gain.py \
  --variants \
    regress_disable_mshr \
    regress_disable_mshr_use_macro_again \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx  

  regress_disable_all_mshr

# Use config.
# 2026-1-15
python3 compute_perf_gain.py \
  --variants \
    regress_mshr_disable \
    regress_mshr_disable_all_cache_lru.o \
    regress_mshr_disable_l1d_l2_srrip_other_lru \
    regress_mshr_disable_l2_srrip_lru_switch_other_lru \
    regress_mshr_disable_l2_srrip_fp_other_lru \
    regress_mshr_disable_l2_srrip_hp_other_lru \
    regress_mshr_disable_l1d_l2_srrip_fp_lru_switch_other_lru \
    regress_mshr_disable_l2_set_max_rrpv_for_lru_picked_index \
    regress_mshr_disable_l2_srrip_hp_set_max_rrpv_for_lru_picked_index \
    regress_mshr_disable_modify_lru_picked_index_with_srrip_update_logic \
    regress_mshr_disable_l2_srrip_hp_lru_switch_other_lru \
    reg_l1d_l2_srrip_hp_lru_switch_rrpv_half_max_when_allocate \
    reg_l2_srrip_hp_lru_switch_rrpv_half_max_when_allocate \
    reg_l2_srrip_hp_rrpv_half_max_when_allocate_again \
    reg_l2_srrip_hp_rrpv_half_max_plus_1_when_allocate \
    reg_l2_srrip_hp_lru_switch_rrpv_half_max_plus_1_when_allocate \
    reg_l2_srrip_hp_lru_switch_rrpv_0_when_allocate \
    reg_en_l2_mshr_l2_srrip_hp_lru_switch_half_max_plus_1_when_allocate \
    reg_en_all_mshr_all_cache_lru \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx  
      
python3 compute_perf_gain.py \
  --variants \
    regress_mshr_disable \
    reg_en_all_mshr_all_cache_lru \
    reg_en_all_mshr_all_cache_mshr_corr_rep \
    reg_en_all_mshr_pick_min_records_in_mshr \
    reg_en_all_mshr_all_cache_mshr_corr_rep_l2_assoc_32 \
    reg_mshr_aware_mixed_rep_l1d_l2_prime_srrip \
    reg_mshr_aware_mixed_rep_l2_prime_lru \
    reg_mshr_aware_mixed_rep_l2_prime_srrip \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx  

python3 compute_perf_gain.py \
  --variants \
    reg_mshr_disable_all_cache_rep_lru \
    reg_mshr_disable_all_hybrid_rep_lru_smaller_hits \
    reg_mshr_independent_hybrid_rep \
    reg_mshr_en_hybrid_rep_and_mshr_aware_II \
    reg_mshr_aware_all_lru_enhanced_with_timestamp_hits \
    reg_mshr_aware_all_lru_enhanced_with_timestamp_hits_icnt_l2_128 \
    reg_mshr_aware_all_lru_enhanced_with_timestamp \
    reg_mshr_aware_all_lru \
    reg_en_all_mshr_all_cache_lru \
    reg_en_all_mshr_l2_srrip \
    reg_en_all_mshr_l2_srrip_l2_assoc_32 \
    reg_mshr_aware_mixed_rep_l1d_l2_prime_srrip_l1d_assoc_64_l2_assoc_16 \
    reg_mshr_aware_mixed_rep_l2_prime_lru \
    reg_mshr_aware_mixed_rep_l2_prime_srrip \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants \
    reg_mshr_disable_all_lru \
    reg_mshr_disable_all_lru_enhanced_with_total_hits \
    reg_mshr_disable_all_lru_l1d_enhanced_with_total_hits \
    reg_mshr_en_but_no_aware_all_lru \
    reg_mshr_en_and_aware_all_lru \
    reg_mshr_en_and_aware_all_lru_enhanced_with_total_hits \
    reg_mshr_en_and_aware_all_lru_icnt_l2_128 \
    reg_mshr_en_and_aware_l2_srrip \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx    

python3 compute_perf_gain.py \
  --variants \
    reg_mshr_disable_l2_srrip \
    reg_mshr_en_l2_srrip \
    reg_mshr_en__all_aware_mshr_l2_aware_filltime__l2_srrip \
    reg_mshr_en__aware_mshr__l2_srrip \
    reg_mshr_en__l1d_aware_filltime__l2_srrip \
    reg_mshr_en__all_aware_mshr_l1d_aware_filltime__l2_srrip \
    reg_mshr_en__aware_mshr_filltime__l2_srrip \
    reg_mshr_en__l2_aware_filltime__l2_srrip \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx 
########################################### End of L2 Perf. Study ###########################################

########################################### SCB/CRF Regression Study ###################################
# "--clean-old-o" option is used to clear old .o files before picking latest .o file
# You can also use $ACCELSIM_ROOT/../perf_study/check-regress-results/clean_dir.sh by specifying $tag_name to clear old *.o
# python3 compute_perf_gain.py \
#   --variants \
#     reg_baseline_default_sched \
#     reg_warp_interfere_awared_schedule \
#     reg_num_eu_8__num_sched_per_core_8__max_insn_issue_per_warp_1 \
#     reg_num_eu_64__num_sched_per_core_64__opc_64__max_insn_issue_per_warp_1 \
#   --clean-old-o \
#   --fail-total-metrics NONE \
#   --txt-file perf_gain.txt \
#   --csv-file perf_gain.csv \
#   --md-file perf_gain.md \
#   --html-file perf_gain.html \
#   --xlsx-file perf_gain.xlsx \
#   --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants \
    reg_dis_wia_repl \
    reg_wia_cache_repl_base \
    reg_chk_l1d_pending_longop_evict \
    reg_chk_issue_to_l1d_access_path \
    reg_l1d_mshr_awared_repl \
    reg_l1d_l2_mshr_awared_repl \
    reg_wia_cache_repl_l1d_mq_16 \
    reg_wia_cache_repl_l1d_mq_64 \
    reg_wia_cache_repl_l1d_mq_32 \
    reg_l1d_plopa_repl_l1d_mq_32 \
    reg_wia_mshr_aware_replace_l1d_mq_32 \
    reg_wia_gto_repl_l1d_mq_32 \
    reg_wia_rrr_repl_l1d_mq_32 \
    reg_wia_old_repl_l1d_mq_32 \
    reg_wia_old_repl_l1d_mq_16 \
    reg_old_repl_l1d_mq_32 \
    reg_l1d_l2_wia_old_repl_l1d_mq_32 \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants \
    reg_base_no_mshr \
    reg_l1d_byp_detect_f2e_gap_tuned_conf_cnt \
    reg_l1d_bypass_fixed_thrash_threshold \
    reg_l1d_smart_byp \
    reg_l1d_smart_byp_no_reset \
    reg_l1d_deferred_bypass \
    reg_l1d_mpki_aware_bypass \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

# now
python3 compute_perf_gain.py \
  --variants \
    reg_base_rm_set_addr_with_extra_mf_fields_addr \
    reg_base_no_mshr \
    reg_l1d_byp_fine_tune \
    reg_l1d_byp_rm_f2e_q_when_deact \
    reg_l1d_byp_dec_step_2 \
    reg_l1d_max_byp_n_10_inc_bound_5 \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

# Compare single cases
python3 compute_perf_gain.py \
  --variants \
    reg_base_no_mshr_srad_v2 \
    reg_l1d_byp_tune_srad_v2_dec_step_1 \
    reg_l1d_bypkey_srad_v2 \
    reg_l1d_set_max_byp_num_5_srad_v2 \
    reg_l1d_set_max_byp_num_15_srad_v2 \
    reg_l1d_max_byp_n_10_no_dec_srad_v2 \
    reg_l1d_max_byp_n_10_inc_bound_7_srad_v2 \
    reg_l1d_max_byp_n_10_inc_bound_5_srad_v2 \
    reg_l1d_max_byp_n_10_inc_bound_3_srad_v2 \
    reg_l1d_max_byp_n_8_inc_bound_5_srad_v2 \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx
  
# 164.599 (+0.000%) vs 164.599 (+0.000%) - no diff in IPC
python3 compute_perf_gain.py \
  --variants \
    reg_base_no_mshr_src_backprop \
    reg_l1d_byp_detect_f2e_gap_tuned_conf_cnt_backprop \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants \
    reg_base_no_mshr_streamcluster \
    reg_l1d_byp_detect_f2e_gap_tuned_conf_cnt_streamcluster \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants \
    reg_base_no_mshr_nw \
    reg_l1d_byp_detect_f2e_gap_tuned_conf_cnt_nw \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants \
    reg_base_no_mshr_nn \
    reg_l1d_byp_detect_f2e_gap_tuned_conf_cnt_nn \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants \
    reg_base_no_mshr_hotspot \
    reg_l1d_byp_detect_f2e_gap_tuned_conf_cnt_hotspot \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants \
    reg_base_no_mshr_streamcluster \
    reg_l1d_dynamic_byp_streamcluster_dec_step_2 \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants \
    reg_base_no_mshr_srad_v2 \
    reg_l1d_byp_tune_srad_v2_dec_step_1 \
    reg_l1d_byp_tune_srad_v2_dec_step_2 \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants \
    reg_base_no_mshr_streamcluster \
    reg_l1d_byp_fine_tuned_streamcluster \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx
  
python3 compute_perf_gain.py \
  --variants \
    reg_base_no_mshr_gto_srad_v2 \
    reg_l1d_max_evict_bound_20_gto_srad_v2 \
    reg_l1d_max_evict_bound_10_gto_srad_v2 \
    reg_l1d_max_evict_bound_5_gto_srad_v2 \
    reg_l1d_max_evict_bound_7_gto_srad_v2 \
    reg_l1d_sat_cnt_based_gto_srad_v2 \
    reg_l1d_sat_cnt_up_bound_2_gto_srad_v2 \
    reg_l1d_satcnt_both_inc_dec_upb_3_gto_srad_v2 \
    reg_l1d_satcnt_only_inc_upb_3_gto_srad_v2_II \
    reg_l1d_max_evict_then_satcnt_gto_srad_v2 \
    reg_l1d_max_evict_then_satcnt_gto_srad_v2_again \
    reg_l1d_enough_history_or_smaller_gap_gto_srad_v2 \
    reg_l1d_satcnt_only_inc_upb_3_old_srad_v2 \
    reg_l1d_l2_max_evict_then_satcnt_gto_srad_v2 \
    reg_l1d_l2_max_evict_then_satcnt_l2_qsize_30_gto_srad_v2 \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants \
    l1d_no_byp \
    l1d_byp_T_F_T_20_5_3_incoming_000_lrr \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

# single case
python3 compute_perf_gain.py \
  --variants \
    reg_l1d_base_lrr_backprop \
    l1d_byp_T_F_T_20_5_3_incoming_000_lrr_backprop \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants \
    l1d_base_lrr_srad_v2 \
    l1d_byp_T_F_T_20_5_3_lrr_srad_v2 \
    l1d_byp_T_F_T_20_5_3_addr_only_for_match_lrr_srad_v2 \
    l1d_byp_T_F_T_20_5_3_kernel_and_addr_for_match_lrr_srad_v2 \
    l1d_byp_T_F_T_20_5_3_bypass_key_for_match_lrr_srad_v2 \
    l1d_byp_T_F_T_20_5_3_lrr_victim_cache_srad_v2 \
    l1d_byp_T_F_T_20_5_3_lrr_victim_cache_ent_256_swap_srad_v2 \
    l1d_byp_T_F_T_20_5_3_lrr_victim_cache_ent_128_swap_srad_v2 \
    l1d_byp_T_F_T_20_5_3_lrr_victim_cache_ent_64_swap_srad_v2 \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants \
    reg_l1d_base_lrr_streamcluster \
    l1d_byp_T_F_T_20_5_3_incoming_000_lrr_streamcluster \
    l1d_byp_T_F_T_20_5_3_incoming_050_lrr_streamcluster \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants \
    reg_l1d_base_gto_streamcluster \
    reg_l1d_dyn_byp_total_evict_aware_gto_streamcluster \
    reg_l1d_dyn_byp_total_evict_unaware_gto_streamcluster \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants \
    reg_l1d_base_lrr_hotspot \
    reg_l1d_dyn_byp_total_evict_aware_lrr_hotspot \
    reg_l1d_dyn_byp_total_evict_aware_upb_5_lrr_hotspot \
    reg_l1d_dyn_byp_total_evict_aware_upb_3_lrr_hotspot \
    reg_l1d_dyn_byp_total_evict_aware_upb_3_bypset_100_lrr_hotspot \
    reg_l1d_dyn_byp_total_evict_aware_upb_3_bypset_50_lrr_hotspot \
    reg_l1d_dyn_byp_total_evict_aware_upb_3_bypset_40_lrr_hotspot \
    reg_l1d_dyn_byp_total_evict_aware_upb_3_bypset_35_lrr_hotspot \
    reg_l1d_dyn_byp_total_evict_aware_upb_3_bypset_30_lrr_hotspot \
    reg_l1d_dyn_byp_total_evict_aware_upb_3_bypset_20_lrr_hotspot \
    reg_l1d_dyn_byp_total_evict_aware_upb_3_bypset_10_lrr_hotspot \
    reg_l1d_dyn_byp_total_evict_aware_upb_2_lrr_hotspot \
    reg_l1d_dyn_byp_total_evict_unaware_lrr_hotspot \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants \
    reg_l1d_base_lrr_hotspot \
    both_vic_byp_key_use_blkaddr_T_F_T_80_3_3_lrr_hotspot \
    both_vic_byp_key_use_blkaddr_T_F_T_40_3_3_lrr_hotspot \
    both_vic_byp_key_use_blkaddr_T_F_T_20_3_3_lrr_hotspot \
    both_vic_byp_key_use_blkaddr_T_F_T_20_2_2_lrr_hotspot \
    both_vic_byp_key_use_blkaddr_T_F_T_20_1_1_lrr_hotspot \
    both_vic_byp_key_use_blkaddr_T_T_F_20_1_1_lrr_hotspot \
    l1d_byp_T_F_T_40_3_3_incoming_070_lrr_hotspot \
    l1d_byp_T_F_T_40_3_3_incoming_100_lrr_hotspot \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

# Eval max_bypasses
python3 compute_perf_gain.py \
  --variants \
    reg_l1d_base_lrr_hotspot \
    reg_l1d_dyn_byp_infinite_bypasses_hotspot \
    reg_l1d_dyn_byp_max_bypasses_45_hotspot \
    reg_l1d_dyn_byp_max_bypasses_40_hotspot \
    reg_l1d_dyn_byp_max_bypasses_35_hotspot \
    reg_l1d_dyn_byp_max_bypasses_30_hotspot \
    reg_l1d_dyn_byp_max_bypasses_25_hotspot \
    reg_l1d_dyn_byp_max_bypasses_20_hotspot \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants \
    reg_l1d_base_gto_hotspot \
    reg_l1d_dyn_byp_total_evict_aware_gto_hotspot \
    reg_l1d_dyn_byp_total_evict_aware_upb_5_gto_hotspot \
    reg_l1d_dyn_byp_total_evict_aware_upb_3_gto_hotspot \
    reg_l1d_dyn_byp_total_evict_unaware_gto_hotspot \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx


python3 compute_perf_gain.py \
  --variants \
    reg_l1d_base_lrr \
    reg_l1d_dyn_byp_total_evict_aware_lrr \
    reg_l1d_dyn_byp_total_evict_unaware_lrr \
    reg_l1d_base_gto \
    reg_l1d_dyn_byp_total_evict_aware_gto \
    reg_l1d_dyn_byp_total_evict_unaware_gto \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants \
    reg_l1d_base_lrr \
    reg_l1d_dyn_byp_total_evict_aware_lrr \
    reg_l1d_dyn_byp_total_evict_unaware_lrr \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx

python3 compute_perf_gain.py \
  --variants \
    reg_l1d_base_gto \
    reg_l1d_dyn_byp_total_evict_aware_gto \
    reg_l1d_dyn_byp_total_evict_unaware_gto \
  --clean-old-o \
  --fail-total-metrics NONE \
  --txt-file perf_gain.txt \
  --csv-file perf_gain.csv \
  --md-file perf_gain.md \
  --html-file perf_gain.html \
  --xlsx-file perf_gain.xlsx \
  --fail-cause-xlsx fail_cause_breakdown.xlsx
"""
import argparse, os, re, sys, math
from typing import List
from collections import defaultdict
from copy import copy

GPU_IPC_RE = re.compile(r"gpu_tot_ipc\s*=\s*([0-9]+\.?[0-9]*)")
TOTAL_R_RE = re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_R\]\s*=\s*([0-9]+)")
TOTAL_W_RE = re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_W\]\s*=\s*([0-9]+)")
CAUSE_R_RE = re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_R\]\[([^\]]+)\]\s*=\s*([0-9]+)")
CAUSE_W_RE = re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_W\]\[([^\]]+)\]\s*=\s*([0-9]+)")
CAUSE_DRIVER_R_RE = re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_R\]\[([^\]]+)\]\[([^\]]+)\]\s*=\s*([0-9]+)")
CAUSE_DRIVER_W_RE = re.compile(r"Total_core_cache_fail_stats_breakdown\[GLOBAL_ACC_W\]\[([^\]]+)\]\[([^\]]+)\]\s*=\s*([0-9]+)")
KERNEL_NAME_RE = re.compile(r"(?:-kernel name|kernel_name)\s*=\s*(.+)")
KERNEL_UID_RE = re.compile(r"kernel_launch_uid\s*=\s*([0-9]+)")

FLOAT_CAPTURE = r"([+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)"
# L2_BW_RE = re.compile(rf"L2_BW\s*=\s*{FLOAT_CAPTURE}")
# L2_ACCESSES_RE = re.compile(rf"L2_(?:total_cache_)?accesses\s*=\s*{FLOAT_CAPTURE}")
# L2_MISSES_RE = re.compile(rf"L2_misses\s*=\s*{FLOAT_CAPTURE}")
# L2_GLOB_ACC_W_TOTAL_ACCESS_RE = re.compile(rf"L2_stats_breakdown\[GLOBAL_ACC_W\]\[TOTAL_ACCESS\]\s*=\s*{FLOAT_CAPTURE}")
# L2_MISS_RATE_RE = re.compile(rf"L2_(?:total_cache_|total_)?miss_rate\s*=\s*{FLOAT_CAPTURE}")
# L2_AVG_MISS_SERVED_TIME_RE = re.compile(rf"avg_l2_miss_served_cycles\s*=\s*{FLOAT_CAPTURE}")
L1D_ACCESSES_RE = re.compile(rf"L1D_accesses\s*=\s*{FLOAT_CAPTURE}")
L1D_RD_MISSES_RE    = re.compile(rf"L1D_RD_MISSES\s*=\s*{FLOAT_CAPTURE}")
L1D_READS_RE        = re.compile(rf"L1D_READS\s*=\s*{FLOAT_CAPTURE}")
L1D_RD_MISS_RATE_RE = re.compile(rf"L1D_RD_MISS_RATE\s*=\s*{FLOAT_CAPTURE}")
L1D_N_FILL_TO_EVICT_LINES_RE = re.compile(rf"L1D_N_FILL_TO_EVICT_LINES\s*=\s*{FLOAT_CAPTURE}")
L1D_AVG_RD_BYP_ACT_RE      = re.compile(rf"l1d_avg_rd_byp_act\s*=\s*{FLOAT_CAPTURE}")
L1D_AVG_RD_BYP_DEACT_RE    = re.compile(rf"l1d_avg_rd_byp_deact\s*=\s*{FLOAT_CAPTURE}")
L1D_AVG_RD_BYP_ACT_RATE_RE = re.compile(rf"l1d_avg_rd_byp_act_rate\s*=\s*{FLOAT_CAPTURE}")
L1D_AVG_RD_MISS_SERVED_TIME_RE = re.compile(rf"avg_l1d_rd_miss_served_cycles\s*=\s*{FLOAT_CAPTURE}")

L1D_MPKI = re.compile(rf"L1D_MPKI\s*=\s*{FLOAT_CAPTURE}")
NON_VALID_PERCENT = re.compile(rf"non_valid_percent\s*=\s*{FLOAT_CAPTURE}")
DEP_CHK_FAIL_PERCENT = re.compile(rf"dep_chk_fail_percent\s*=\s*{FLOAT_CAPTURE}")
PIPE_STALLED_PERCENT = re.compile(rf"pipe_stalled_percent\s*=\s*{FLOAT_CAPTURE}")

INTRA_WARP_INTERFERENCES = re.compile(rf"total_intra_warp_interferences\s*=\s*{FLOAT_CAPTURE}")
INTER_WARP_INTERFERENCES = re.compile(rf"total_inter_warp_interferences\s*=\s*{FLOAT_CAPTURE}")
IWI_PERCENT = re.compile(rf"inter_warp_interfere_percent\s*=\s*{FLOAT_CAPTURE}")
RAW_CONFLICTS_RATE_RE = re.compile(rf"raw_conflicts_rate\[bank:(\d+)\]\s*=\s*{FLOAT_CAPTURE}")
WR_REG_BANK_CONFLICTS_RATE_RE = re.compile(rf"wr_reg_bank_conflicts_rate\[bank:(\d+)\]\s*=\s*{FLOAT_CAPTURE}")
TOTAL_ISSUE_RATIO = re.compile(rf"total_issue_ratio\s*=\s*{FLOAT_CAPTURE}")
ISSUE_BW_UTILIZATION = re.compile(rf"issue_bw_utilization\s*=\s*{FLOAT_CAPTURE}")
TOTAL_ISSUE_FAILS = re.compile(rf"total_issue_fails\s*=\s*{FLOAT_CAPTURE}")
G_ACC_R_MQ_FULL = re.compile(rf"breakdown\[GLOBAL_ACC_R\]\[MISS_QUEUE_FULL\]\s*=\s*{FLOAT_CAPTURE}")

def _sanitize_csv_name(name: str) -> str:
    s = str(name).strip()
    if not s:
        s = "unknown_benchmark"
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s)

def split_overall_csv_by_benchmark(overall_csv: str, out_dir: str) -> None:
    if not overall_csv or not os.path.isfile(overall_csv):
        print(f"[INFO] skip split: csv not found: {overall_csv}")
        return

    with open(overall_csv, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = list(reader)

    if not headers:
        print(f"[INFO] skip split: empty header in {overall_csv}")
        return

    # 自动识别 benchmark 列
    candidates = ["benchmark", "bench", "app", "application", "workload", "kernel", "trace"]
    lower_map = {h.lower(): h for h in headers}
    bench_col = None

    for c in candidates:
        if c in lower_map:
            bench_col = lower_map[c]
            break
    if bench_col is None:
        for h in headers:
            lh = h.lower()
            if any(c in lh for c in candidates):
                bench_col = h
                break

    if bench_col is None:
        print(f"[INFO] skip split: benchmark column not found in {overall_csv}")
        return

    os.makedirs(out_dir, exist_ok=True)

    grouped = OrderedDict()
    for r in rows:
        key = (r.get(bench_col, "") or "").strip()
        if not key:
            key = "unknown_benchmark"
        grouped.setdefault(key, []).append(r)

    for bench, bench_rows in grouped.items():
        out_csv = os.path.join(out_dir, f"{_sanitize_csv_name(bench)}.csv")
        with open(out_csv, "w", newline="", encoding="utf-8") as wf:
            writer = csv.DictWriter(wf, fieldnames=headers, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(bench_rows)
        print(f"[INFO] wrote per-benchmark csv: {out_csv}")

def pick_latest_o_file(variant_dir: str) -> str:
    pat = re.compile(r".*\.o(\d+)?$")
    if not os.path.isdir(variant_dir): return ''
    files = [f for f in os.listdir(variant_dir) if pat.match(f)]
    if not files: return ''
    paths=[os.path.join(variant_dir,f) for f in files]
    paths.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return paths[0]

# also a must, otherwise fields would not appear in .csv
def parse_o_file(path: str):
    try:
        lines=open(path).read().splitlines()
    except Exception:
        return []
    kernels=[]
    current=None
    r_total=0
    w_total=0
    r_reasons={}
    w_reasons={}
    r_driver_reasons={}
    w_driver_reasons={}
    pending_kernel_name=None
    pending_kernel_uid=None
    l2_bw=None
    l2_accesses=None
    l2_misses=None
    l2_global_acc_w_total_access=None
    l2_miss_rate=None
    l1d_misses=None
    l1d_rd_misses=None
    l1d_reads=None    
    l1d_rd_miss_rate=None
    l1d_n_fill_to_evict_lines=None
    l1d_avg_rd_byp_rate=None
    l1d_avg_rd_byp_act=None
    l1d_avg_rd_byp_deact=None
    l1d_mpki=None
    non_valid_percent=None
    dep_chk_fail_percent=None
    pipe_stalled_percent=None
    intra_warp_interferences=None
    inter_warp_interferences=None
    inter_warp_interfere_percent=None
    partition_level_parallelism=None
    avg_l2_miss_served_cycles=None
    avg_l1d_rd_miss_served_cycles=None
    total_issue_ratio=None
    issue_bw_utilization=None
    total_issue_fails=None
    g_acc_r_mq_full=None
    raw_conflicts_rate_by_bank={}
    wr_reg_bank_conflicts_rate_by_bank={}

    def reset_state():
        nonlocal r_total, w_total, r_reasons, w_reasons, r_driver_reasons, w_driver_reasons
        nonlocal l2_bw, l2_global_acc_w_total_access
        nonlocal l2_misses, l2_accesses, l2_miss_rate
        nonlocal l1d_reads,l1d_rd_misses,l1d_rd_miss_rate
        nonlocal l1d_n_fill_to_evict_lines,l1d_avg_rd_byp_act,l1d_avg_rd_byp_deact,l1d_avg_rd_byp_act_rate
        nonlocal l1d_mpki
        nonlocal non_valid_percent, dep_chk_fail_percent, pipe_stalled_percent
        nonlocal intra_warp_interferences, inter_warp_interferences, inter_warp_interfere_percent
        nonlocal partition_level_parallelism
        nonlocal avg_l2_miss_served_cycles, avg_l1d_rd_miss_served_cycles
        nonlocal total_issue_ratio, issue_bw_utilization, total_issue_fails
        nonlocal g_acc_r_mq_full
        nonlocal raw_conflicts_rate_by_bank, wr_reg_bank_conflicts_rate_by_bank
        r_total=0
        w_total=0
        r_reasons={}
        w_reasons={}
        r_driver_reasons={}
        w_driver_reasons={}
        l2_bw=None
        l2_accesses=None
        l2_misses=None
        l2_global_acc_w_total_access=None
        l2_miss_rate=None
        l1d_misses=None
        l1d_rd_misses=None
        l1d_reads=None        
        l1d_rd_miss_rate=None
        l1d_n_fill_to_evict_lines=None     
        l1d_avg_rd_byp_act=None
        l1d_avg_rd_byp_deact=None        
        l1d_avg_rd_byp_act_rate=None
        l1d_mpki=None
        non_valid_percent=None
        dep_chk_fail_percent=None
        pipe_stalled_percent=None
        intra_warp_interferences=None
        inter_warp_interferences=None
        inter_warp_interfere_percent=None
        partition_level_parallelism=None
        avg_l2_miss_served_cycles=None
        avg_l1d_rd_miss_served_cycles=None
        total_issue_ratio=None
        issue_bw_utilization=None
        total_issue_fails=None
        g_acc_r_mq_full=None
        raw_conflicts_rate_by_bank={}
        wr_reg_bank_conflicts_rate_by_bank={}

    def commit_current():
        nonlocal current
        if current is None:
            return
        current['r_total']=r_total
        current['w_total']=w_total
        current['r_reasons']=dict(r_reasons)
        current['w_reasons']=dict(w_reasons)
        current['r_drivers']={cause: dict(drivers) for cause, drivers in r_driver_reasons.items()}
        current['w_drivers']={cause: dict(drivers) for cause, drivers in w_driver_reasons.items()}
        current['l2_bw']=l2_bw
        current['l2_accesses']=l2_accesses
        current['l2_misses']=l2_misses
        current['l2_global_acc_w_total_access']=l2_global_acc_w_total_access
        current['l2_miss_rate']=l2_miss_rate
        current['l1d_rd_misses']=l1d_rd_misses
        current['l1d_reads']=l1d_reads        
        current['l1d_rd_miss_rate']=l1d_rd_miss_rate
        current['l1d_n_fill_to_evict_lines']=l1d_n_fill_to_evict_lines
        current['l1d_avg_rd_byp_act']=l1d_avg_rd_byp_act
        current['l1d_avg_rd_byp_deact']=l1d_avg_rd_byp_deact
        current['l1d_avg_rd_byp_act_rate']=l1d_avg_rd_byp_act_rate
        current['l1d_mpki']=l1d_mpki
        current['non_valid_percent']=non_valid_percent
        current['dep_chk_fail_percent']=dep_chk_fail_percent
        current['pipe_stalled_percent']=pipe_stalled_percent
        current['intra_warp_interferences']=intra_warp_interferences
        current['inter_warp_interferences']=inter_warp_interferences
        current['inter_warp_interfere_percent']=inter_warp_interfere_percent        
        current['partition_level_parallelism']=partition_level_parallelism
        current['avg_l2_miss_served_cycles']=avg_l2_miss_served_cycles
        current['avg_l1d_rd_miss_served_cycles']=avg_l1d_rd_miss_served_cycles
        current['total_issue_ratio']=total_issue_ratio
        current['issue_bw_utilization']=issue_bw_utilization
        current['total_issue_fails']=total_issue_fails
        current['g_acc_r_mq_full']=g_acc_r_mq_full
        current['raw_conflicts_rate_by_bank']=dict(raw_conflicts_rate_by_bank)
        current['wr_reg_bank_conflicts_rate_by_bank']=dict(wr_reg_bank_conflicts_rate_by_bank)
        current['raw_conflicts_rate_avg']=average_bank_rate(raw_conflicts_rate_by_bank)
        current['wr_reg_bank_conflicts_rate_avg']=average_bank_rate(wr_reg_bank_conflicts_rate_by_bank)
        current['total_fail']=(r_total or 0)+(w_total or 0)
        kernels.append(current)
        current=None
        reset_state()

    for line in lines:
        kernel_name_match=KERNEL_NAME_RE.search(line)
        if kernel_name_match:
            name=kernel_name_match.group(1).strip()
            if current is not None:
                current['kernel']=name
            else:
                pending_kernel_name=name
            continue

        kernel_uid_match=KERNEL_UID_RE.search(line)
        if kernel_uid_match:
            uid=int(kernel_uid_match.group(1))
            if current is not None:
                current['kernel_uid']=uid
            else:
                pending_kernel_uid=uid
            continue

        ipc_match=GPU_IPC_RE.search(line)
        if ipc_match:
            if current is not None or r_total or w_total or r_reasons or w_reasons or r_driver_reasons or w_driver_reasons:
                commit_current()
            current={'ipc':float(ipc_match.group(1))}
            if pending_kernel_name is not None:
                current['kernel']=pending_kernel_name
                pending_kernel_name=None
            if pending_kernel_uid is not None:
                current['kernel_uid']=pending_kernel_uid
                pending_kernel_uid=None
            reset_state()
            continue

        l1d_rd_miss_rate_match=L1D_RD_MISS_RATE_RE.search(line)
        if l1d_rd_miss_rate_match:
            try:
                l1d_rd_miss_rate=parse_float_value(l1d_rd_miss_rate_match.group(1))
            except (TypeError, ValueError):
                pass
            continue

        l1d_n_fill_to_evict_lines_match=L1D_N_FILL_TO_EVICT_LINES_RE.search(line)
        if l1d_n_fill_to_evict_lines_match:
            try:
                l1d_n_fill_to_evict_lines=parse_float_value(l1d_n_fill_to_evict_lines_match.group(1))
            except (TypeError, ValueError):
                pass
            continue

        l1d_avg_rd_byp_act_rate_match=L1D_AVG_RD_BYP_ACT_RATE_RE.search(line)
        if l1d_avg_rd_byp_act_rate_match:
            try:
                l1d_avg_rd_byp_act_rate=parse_float_value(l1d_avg_rd_byp_act_rate_match.group(1))
            except (TypeError, ValueError):
                pass
            continue     

        total_r_match=TOTAL_R_RE.search(line)
        if total_r_match:
            r_total=int(total_r_match.group(1))
            continue

        total_w_match=TOTAL_W_RE.search(line)
        if total_w_match:
            w_total=int(total_w_match.group(1))
            continue

        cause_r_match=CAUSE_R_RE.search(line)
        if cause_r_match:
            try:
                r_reasons[cause_r_match.group(1)]=int(cause_r_match.group(2))
            except ValueError:
                pass
            continue

        cause_driver_r_match=CAUSE_DRIVER_R_RE.search(line)
        if cause_driver_r_match:
            cause=cause_driver_r_match.group(1)
            driver=cause_driver_r_match.group(2)
            try:
                amt=int(cause_driver_r_match.group(3))
            except ValueError:
                pass
            else:
                r_driver_reasons.setdefault(cause, {})[driver]=amt
            continue

        cause_w_match=CAUSE_W_RE.search(line)
        if cause_w_match:
            try:
                w_reasons[cause_w_match.group(1)]=int(cause_w_match.group(2))
            except ValueError:
                pass
            continue

        cause_driver_w_match=CAUSE_DRIVER_W_RE.search(line)
        if cause_driver_w_match:
            cause=cause_driver_w_match.group(1)
            driver=cause_driver_w_match.group(2)
            try:
                amt=int(cause_driver_w_match.group(3))
            except ValueError:
                pass
            else:
                w_driver_reasons.setdefault(cause, {})[driver]=amt
            continue

        # l2_bw_match=L2_BW_RE.search(line)
        # if l2_bw_match:
        #     try:
        #         l2_bw=parse_float_value(l2_bw_match.group(1))
        #     except (TypeError, ValueError):
        #         pass
        #     continue
        # l2_accesses_match=L2_ACCESSES_RE.search(line)
        # if l2_accesses_match:
        #     try:
        #         l2_accesses=int(float(l2_accesses_match.group(1)))
        #     except (TypeError, ValueError):
        #         pass
        #     continue
        # l2_misses_match=L2_MISSES_RE.search(line)
        # if l2_misses_match:
        #     try:
        #         l2_misses=int(float(l2_misses_match.group(1)))
        #     except (TypeError, ValueError):
        #         pass
        #     continue
        # l2_miss_rate_match=L2_MISS_RATE_RE.search(line)
        # if l2_miss_rate_match:
        #     try:
        #         l2_miss_rate=parse_float_value(l2_miss_rate_match.group(1))
        #     except (TypeError, ValueError):
        #         pass
        #     continue
        # l2_global_acc_w_total_access_match=L2_GLOB_ACC_W_TOTAL_ACCESS_RE.search(line)
        # if l2_global_acc_w_total_access_match:
        #     try:
        #         l2_global_acc_w_total_access=int(float(l2_global_acc_w_total_access_match.group(1)))
        #     except (TypeError, ValueError):
        #         pass
        #     continue
        # l2_partition_level_parallelism_match=PARTITION_LEVEL_PARALLELISM.search(line)
        # if l2_partition_level_parallelism_match:
        #     try:
        #         partition_level_parallelism=parse_float_value(l2_partition_level_parallelism_match.group(1))
        #     except (TypeError, ValueError):
        #         pass
        #     continue
        # avg_l2_miss_served_cycles_match=L2_AVG_MISS_SERVED_TIME_RE.search(line)
        # if avg_l2_miss_served_cycles_match:
        #     try:
        #         avg_l2_miss_served_cycles=parse_float_value(avg_l2_miss_served_cycles_match.group(1))
        #     except (TypeError, ValueError):
        #         pass
        #     continue

        avg_l1d_rd_miss_served_cycles_match=L1D_AVG_RD_MISS_SERVED_TIME_RE.search(line)
        if avg_l1d_rd_miss_served_cycles_match:
            try:
                avg_l1d_rd_miss_served_cycles=parse_float_value(avg_l1d_rd_miss_served_cycles_match.group(1))
            except (TypeError, ValueError):
                pass
            continue

        intra_warp_interferences_match=INTRA_WARP_INTERFERENCES.search(line)
        if intra_warp_interferences_match:
            try:
                intra_warp_interferences=parse_float_value(intra_warp_interferences_match.group(1))
            except (TypeError, ValueError):
                pass
            continue

        inter_warp_interferences_match=INTER_WARP_INTERFERENCES.search(line)
        if inter_warp_interferences_match:
            try:
                inter_warp_interferences=parse_float_value(inter_warp_interferences_match.group(1))
            except (TypeError, ValueError):
                pass
            continue

        iwi_percent_match=IWI_PERCENT.search(line)
        if iwi_percent_match:
            try:
                inter_warp_interfere_percent=parse_float_value(iwi_percent_match.group(1))
            except (TypeError, ValueError):
                pass
            continue

        total_issue_ratio_match=TOTAL_ISSUE_RATIO.search(line)
        if total_issue_ratio_match:
            try:
                total_issue_ratio=parse_float_value(total_issue_ratio_match.group(1))
            except (TypeError, ValueError):
                pass
            continue
        issue_bw_utilization_match=ISSUE_BW_UTILIZATION.search(line)
        if issue_bw_utilization_match:
            try:
                issue_bw_utilization=parse_float_value(issue_bw_utilization_match.group(1))
            except (TypeError, ValueError):
                pass
            continue
        total_issue_fails_match=TOTAL_ISSUE_FAILS.search(line)
        if total_issue_fails_match:
            try:
                total_issue_fails=parse_float_value(total_issue_fails_match.group(1))
            except (TypeError, ValueError):
                pass
            continue
        g_acc_r_mq_full_match=G_ACC_R_MQ_FULL.search(line)
        if g_acc_r_mq_full_match:
            try:
                g_acc_r_mq_full=parse_float_value(g_acc_r_mq_full_match.group(1))
            except (TypeError, ValueError):
                pass
            continue        

        raw_conflicts_rate_match=RAW_CONFLICTS_RATE_RE.search(line)
        if raw_conflicts_rate_match:
            try:
                bank=int(raw_conflicts_rate_match.group(1))
                rate=parse_float_value(raw_conflicts_rate_match.group(2))
            except (TypeError, ValueError):
                pass
            else:
                raw_conflicts_rate_by_bank[bank]=rate
            continue

        wr_reg_bank_conflicts_rate_match=WR_REG_BANK_CONFLICTS_RATE_RE.search(line)
        if wr_reg_bank_conflicts_rate_match:
            try:
                bank=int(wr_reg_bank_conflicts_rate_match.group(1))
                rate=parse_float_value(wr_reg_bank_conflicts_rate_match.group(2))
            except (TypeError, ValueError):
                pass
            else:
                wr_reg_bank_conflicts_rate_by_bank[bank]=rate
            continue
         
        l1d_rd_misses_match=L1D_RD_MISSES_RE.search(line)
        if l1d_rd_misses_match:
            try:
                l1d_rd_misses=parse_float_value(l1d_rd_misses_match.group(1))
            except (TypeError, ValueError):
                pass
            continue          
        l1d_avg_rd_byp_act_match=L1D_AVG_RD_BYP_ACT_RE.search(line)
        if l1d_avg_rd_byp_act_match:
            try:
                l1d_avg_rd_byp_act=parse_float_value(l1d_avg_rd_byp_act_match.group(1))
            except (TypeError, ValueError):
                pass
            continue
        l1d_avg_rd_byp_deact_match=L1D_AVG_RD_BYP_DEACT_RE.search(line)
        if l1d_avg_rd_byp_deact_match:
            try:
                l1d_avg_rd_byp_deact=parse_float_value(l1d_avg_rd_byp_deact_match.group(1))
            except (TypeError, ValueError):
                pass
            continue        
        l1d_reads_match=L1D_READS_RE.search(line)
        if l1d_reads_match:
            try:
                l1d_reads=parse_float_value(l1d_reads_match.group(1))
            except (TypeError, ValueError):
                pass
            continue
        l1d_mpki_match=L1D_MPKI.search(line)
        if l1d_mpki_match:
            try:
                l1d_mpki=parse_float_value(l1d_mpki_match.group(1))
            except (TypeError, ValueError):
                pass
            continue
        non_valid_percent_match=NON_VALID_PERCENT.search(line)
        if non_valid_percent_match:
            try:
                non_valid_percent=parse_float_value(non_valid_percent_match.group(1))
            except (TypeError, ValueError):
                pass
            continue        
        dep_chk_fail_percent_match=DEP_CHK_FAIL_PERCENT.search(line)
        if dep_chk_fail_percent_match:
            try:
                dep_chk_fail_percent=parse_float_value(dep_chk_fail_percent_match.group(1))
            except (TypeError, ValueError):
                pass
            continue
        pipe_stalled_percent_match=PIPE_STALLED_PERCENT.search(line)
        if pipe_stalled_percent_match:
            try:
                pipe_stalled_percent=parse_float_value(pipe_stalled_percent_match.group(1))
            except (TypeError, ValueError):
                pass
            continue

    if current is not None:
        commit_current()
    elif r_total or w_total or r_reasons or w_reasons or r_driver_reasons or w_driver_reasons:
        # kerenel determines if item would appear in .xlsx
        kernels=[{
            'ipc': None,
            'kernel': pending_kernel_name,
            'kernel_uid': pending_kernel_uid,
            'r_total': r_total,
            'w_total': w_total,
            'r_reasons': dict(r_reasons),
            'w_reasons': dict(w_reasons),
            'r_drivers': {cause: dict(drivers) for cause, drivers in r_driver_reasons.items()},
            'w_drivers': {cause: dict(drivers) for cause, drivers in w_driver_reasons.items()},
            'l2_global_acc_w_total_access': l2_global_acc_w_total_access,
            # 'l2_bw': l2_bw,
            # 'l2_accesses': l2_accesses,
            # 'l2_misses': l2_misses,            
            # 'l2_miss_rate': l2_miss_rate,
            # 'avg_l2_miss_served_cycles': avg_l2_miss_served_cycles,
            # 'partition_level_parallelism': partition_level_parallelism,
            'l1d_rd_misses': l1d_rd_misses,
            'l1d_reads': l1d_reads,            
            'l1d_rd_miss_rate': l1d_rd_miss_rate,
            'l1d_n_fill_to_evict_lines': l1d_n_fill_to_evict_lines,      
            'l1d_avg_rd_byp_act': l1d_avg_rd_byp_act,
            'l1d_avg_rd_byp_deact': l1d_avg_rd_byp_deact,
            'l1d_avg_rd_byp_rate': l1d_avg_rd_byp_rate,
            'l1d_mpki': l1d_mpki,
            'non_valid_percent': non_valid_percent,
            'dep_chk_fail_percent': dep_chk_fail_percent,
            'pipe_stalled_percent': pipe_stalled_percent,
            'avg_l1d_rd_miss_served_cycles': avg_l1d_rd_miss_served_cycles,
            'intra_warp_interferences': intra_warp_interferences,
            'inter_warp_interferences': inter_warp_interferences,
            'inter_warp_interfere_percent': inter_warp_interfere_percent,            
            'total_issue_ratio': total_issue_ratio,
            'issue_bw_utilization': issue_bw_utilization,
            'total_issue_fails': total_issue_fails,
            'g_acc_r_mq_full': g_acc_r_mq_full,
            'raw_conflicts_rate_by_bank': dict(raw_conflicts_rate_by_bank),
            'wr_reg_bank_conflicts_rate_by_bank': dict(wr_reg_bank_conflicts_rate_by_bank),
            'raw_conflicts_rate_avg': average_bank_rate(raw_conflicts_rate_by_bank),
            'wr_reg_bank_conflicts_rate_avg': average_bank_rate(wr_reg_bank_conflicts_rate_by_bank),
            'total_fail': (r_total or 0)+(w_total or 0),
        }]
    return kernels

def discover(root:str):
    return sorted([d for d in os.listdir(root) if 'rodinia-2.0-ft' in d and os.path.isdir(os.path.join(root,d))])

def default_sim_root()->str:
    env=os.getenv('ACCELSIM_ROOT')
    if not env: return ''
    cand=os.path.abspath(os.path.join(env,'..','sim_run_12.1'))
    return cand if os.path.isdir(cand) else ''

# LAST_VALUE_METRICS={'ipc', 'xxx', 'yyy'}
LAST_VALUE_METRICS={'ipc'}

def find_base_and_tuned(variants):
    base=None; tuned=None
    for v in variants:
        nv=v
        if nv.startswith('regress-'): nv=nv[len('regress-'):]
        if nv.endswith('-again'): nv=nv[:-len('-again')]
        if nv=='default-config': nv='base-config'
        if nv=='base-config' and base is None:
            base=v
        if 'mshr-entries-32' in v or 'mshr-entries-32' in nv:
            tuned=v
    return base, tuned

def normalize_variant_name(v: str) -> str:
    nv=v
    if nv.startswith('regress-'):
        nv=nv[len('regress-'):]
    if nv.startswith('perf-study-'):
        nv=nv[len('perf-study-'):]
    if nv.endswith('-again'):
        nv=nv[:-len('-again')]
    if nv=='default-config':
        nv='base-config'
    return nv

def collect_variant(root, bench, variant):
    bdir=os.path.join(root, bench)
    if not os.path.isdir(bdir): return []
    # choose first args_sub that yields data
    for args_sub in os.listdir(bdir):
        ap=os.path.join(bdir,args_sub,'QV100-SASS',variant)
        of=pick_latest_o_file(ap)
        if of:
            return parse_o_file(of)
    return []

def pct_change(tuned, base):
    if base is None or base==0:
        if tuned is None or tuned==0: return 0.0
        return float('inf')
    return (tuned-base)/base*100.0


def geometric_mean_from_records(records, value_key):
    if not records:
        return None
    values=[]
    for rec in records:
        val=rec.get(value_key)
        if val is None:
            continue
        try:
            fval=float(val)
        except (TypeError, ValueError):
            continue
        if math.isnan(fval):
            continue
        values.append(max(fval, 0.0))
    if not values:
        return None
    positive_values=[v for v in values if v>0.0]
    if len(positive_values)==len(values):
        log_sum=sum(math.log(v) for v in positive_values)
        return math.exp(log_sum/len(positive_values))
    if not positive_values:
        return 0.0
    log_sum=sum(math.log(v+1.0) for v in values)
    return math.exp(log_sum/len(values))-1.0


def ratio_from_geomeans(base_val, tuned_val):
    if base_val is None or tuned_val is None:
        return None
    if base_val == 0.0:
        if tuned_val == 0.0:
            return 1.0
        return float('inf')
    return tuned_val / base_val


def ratio_to_pct(ratio):
    if ratio is None:
        return None
    if ratio==float('inf'):
        return float('inf')
    return (ratio-1.0)*100.0


def geometric_mean(values):
    cleaned=[]
    for val in values:
        if val is None:
            continue
        try:
            fval=float(val)
        except (TypeError, ValueError):
            continue
        if math.isnan(fval):
            continue
        cleaned.append(max(fval, 0.0))
    if not cleaned:
        return None
    positive=[v for v in cleaned if v>0.0]
    if len(positive)==len(cleaned):
        log_sum=sum(math.log(v) for v in positive)
        return math.exp(log_sum/len(positive))
    if not positive:
        return 0.0
    log_sum=sum(math.log(v+1.0) for v in cleaned)
    return math.exp(log_sum/len(cleaned))-1.0

# 1. 'label': name showed in .xlsx. You can use an alias name
# 1. enum name should match 'value_key'
METRIC_DEFINITIONS={
    'ipc': {
        'label': 'IPC',
        'value_key': 'ipc',
        'higher_is_better': True,
    },
    'global_acc_r': {
        'label': 'GLOBAL_ACC_R fails',
        'value_key': 'r_total',
        'higher_is_better': False,
    },
    'global_acc_w': {
        'label': 'GLOBAL_ACC_W fails',
        'value_key': 'w_total',
        'higher_is_better': False,
    },
    # 'l2_bw': {
    #     'label': 'L2_BW',
    #     'value_key': 'l2_bw',
    #     'higher_is_better': False,
    # },
    # 'l2_accesses': {
    #     'label': 'L2_accesses',
    #     'value_key': 'l2_accesses',
    #     'higher_is_better': False,
    # },
    # 'l2_misses': {
    #     'label': 'L2_misses',
    #     'value_key': 'l2_misses',
    #     'higher_is_better': False,
    # },    
    # 'l2_miss_rate': {
    #     'label': 'L2_miss_rate',
    #     'value_key': 'l2_miss_rate',
    #     'higher_is_better': False,
    # },
    # 'avg_l2_miss_served_cycles': {
    #     'label': 'avg_l2_miss_served_cycles',
    #     'value_key': 'avg_l2_miss_served_cycles',
    #     'higher_is_better': False,
    # },  
    # 'partition_level_parallelism': {
    #     'label': 'partition_level_parallelism',
    #     'value_key': 'partition_level_parallelism',
    #     'higher_is_better': True,
    # },
    'l1d_rd_misses': {
        'label': 'L1D_RD_MISSES',
        'value_key': 'l1d_rd_misses',
        'higher_is_better': False,
    },   
    'l1d_reads': {
        'label': 'L1D_READS',
        'value_key': 'l1d_reads',
        'higher_is_better': False,
    },    
    'l1d_rd_miss_rate': {
        'label': 'L1D_RD_MISS_RATE',
        'value_key': 'l1d_rd_miss_rate',
        'higher_is_better': False,
    },
    'l1d_n_fill_to_evict_lines': {
        # 'label': 'L1D_RD_N_F2E_LN',
        'label': 'L1D_N_FILL_TO_EVICT_LINES',
        'value_key': 'l1d_n_fill_to_evict_lines',
        'higher_is_better': False,
    },    
    'l1d_avg_rd_byp_rate': {
        'label': 'l1d_avg_rd_byp_rate',
        'value_key': 'l1d_avg_rd_byp_rate',
        'higher_is_better': False,
    },    
    'l1d_avg_rd_byp_act': {
        'label': 'l1d_avg_rd_byp_act', # alias name
        'value_key': 'l1d_avg_rd_byp_act',
        'higher_is_better': False,
    },     
    'l1d_avg_rd_byp_deact': {
        'label': 'l1d_avg_rd_byp_deact', # alias name
        'value_key': 'l1d_avg_rd_byp_deact',
        'higher_is_better': False,
    },     
    # 'l1d_mpki': { # This name should match 'value_key'
    #     'label': 'L1D_MPKI', # alias name
    #     'value_key': 'l1d_mpki',
    #     'higher_is_better': False,
    # },
    'non_valid_percent': { # This name should match 'value_key'
        'label': 'non_valid_percent', # alias name
        'value_key': 'non_valid_percent',
        'higher_is_better': False,
    },
    'dep_chk_fail_percent': { # This name should match 'value_key'
        'label': 'dep_chk_fail_percent', # alias name
        'value_key': 'dep_chk_fail_percent',
        'higher_is_better': False,
    },     
    'pipe_stalled_percent': { # This name should match 'value_key'
        'label': 'pipe_stalled_percent', # alias name
        'value_key': 'pipe_stalled_percent',
        'higher_is_better': False,
    },      
    'avg_l1d_rd_miss_served_cycles': {
        'label': 'avg_l1d_rd_miss_served_cycles',
        'value_key': 'avg_l1d_rd_miss_served_cycles',
        'higher_is_better': False,
    },
    'intra_warp_interferences': {
        'label': 'intra_warp_interferences',
        'value_key': 'intra_warp_interferences',
        'higher_is_better': False,
    },
    'inter_warp_interferences': {
        'label': 'inter_warp_interferences',
        'value_key': 'inter_warp_interferences',
        'higher_is_better': False,
    },
    'inter_warp_interfere_percent': {
        'label': 'inter_wi_percent', # alias name
        'value_key': 'inter_warp_interfere_percent',
        'higher_is_better': False,
    },
    'raw_conflicts_rate_avg': {
        'label': 'raw_conflicts_rate_avg',
        'value_key': 'raw_conflicts_rate_avg',
        'higher_is_better': False,
    },
    'wr_reg_bank_conflicts_rate_avg': {
        'label': 'wr_reg_bank_conflicts_rate_avg',
        'value_key': 'wr_reg_bank_conflicts_rate_avg',
        'higher_is_better': False,
    },
    'total_issue_ratio': {
        'label': 'total_issue_ratio',
        'value_key': 'total_issue_ratio',
        'higher_is_better': True,
    },
    'issue_bw_utilization': {
        'label': 'issue_bw_utilization',
        'value_key': 'issue_bw_utilization',
        'higher_is_better': True,
    },    
    'total_issue_fails': {
        'label': 'total_issue_fails',
        'value_key': 'total_issue_fails',
        'higher_is_better': True,
    },
    'g_acc_r_mq_full': {
        'label': 'g_acc_r_mq_full',
        'value_key': 'g_acc_r_mq_full',
        'higher_is_better': False,
    },    
}

DEFAULT_METRIC_ORDER=['ipc','global_acc_r','global_acc_w']
METRIC_ORDER=list(DEFAULT_METRIC_ORDER)
METRIC_VALUE_KEYS={name: props['value_key'] for name, props in METRIC_DEFINITIONS.items()}
METRIC_LABELS={name: props['label'] for name, props in METRIC_DEFINITIONS.items()}
METRIC_ORIENTATION={name: props['higher_is_better'] for name, props in METRIC_DEFINITIONS.items()}
DEFAULT_FAIL_CAUSE_TYPES=('MSHR_MERGE_ENTRY_FAIL','MISS_QUEUE_FULL')

def _canonicalize_metric_cli_name(name: str) -> str:
    return re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_') if name else ''

# 1. Once defined, item must appear in METRIC_NAME_ALIASES[]. Otherwise, error would arise
# 2. 'A': 'A' is ok.    'A': 'alias_A' wrong
METRIC_NAME_ALIASES={
    'global_acc_r': 'global_acc_r',
    'globalacc_r': 'global_acc_r',
    'global_acc_w': 'global_acc_w',
    'globalacc_w': 'global_acc_w',
    'l2_bw': 'l2_bw',
    'l2_accesses': 'l2_accesses',
    'l2_misses': 'l2_misses',
    'l2totalcacheaccesses': 'l2_accesses',
    'l2_total_cache_accesses': 'l2_accesses',
    'l2_miss_rate': 'l2_miss_rate',
    'l2_total_cache_miss_rate': 'l2_miss_rate',
    'l2_total_miss_rate': 'l2_miss_rate',
    'l1d_rd_misses': 'l1d_rd_misses',
    'l1d_reads': 'l1d_reads',    
    'l1d_rd_miss_rate': 'l1d_rd_miss_rate',
    'l1d_n_fill_to_evict_lines': 'l1d_n_fill_to_evict_lines',
    'l1d_avg_rd_byp_act': 'l1d_avg_rd_byp_act',
    'l1d_avg_rd_byp_deact': 'l1d_avg_rd_byp_deact',
    'l1d_avg_rd_byp_act_rate': 'l1d_avg_rd_byp_act_rate',
    'l1d_mpki': 'l1d_mpki',
    'non_valid_percent': 'non_valid_percent',
    'dep_chk_fail_percent': 'dep_chk_fail_percent',
    'pipe_stalled_percent': 'pipe_stalled_percent',
    'intra_warp_interferences': 'intra_warp_interferences',
    'inter_warp_interferences': 'inter_warp_interferences',
    'inter_warp_interfere_percent': 'inter_warp_interfere_percent',
    'partition_level_parallelism': 'partition_level_parallelism',
    'avg_l2_miss_served_cycles': 'avg_l2_miss_served_cycles',
    'avg_l1d_rd_miss_served_cycles': 'avg_l1d_rd_miss_served_cycles',
    'raw_conflicts_rate': 'raw_conflicts_rate_avg',
    'raw_conflicts_rate_avg': 'raw_conflicts_rate_avg',
    'wr_reg_bank_conflicts_rate': 'wr_reg_bank_conflicts_rate_avg',
    'wr_reg_bank_conflicts_rate_avg': 'wr_reg_bank_conflicts_rate_avg',
    'total_issue_ratio': 'total_issue_ratio',
    'issue_bw_utilization': 'issue_bw_utilization',
    'total_issue_fails': 'total_issue_fails',
    'g_acc_r_mq_full': 'g_acc_r_mq_full'
}

def resolve_metric_key(name: str) -> str:
    return METRIC_NAME_ALIASES.get(_canonicalize_metric_cli_name(name or ''))


def format_value(value):
    if value is None:
        return 'NA'
    if value==float('inf'):
        return 'inf'
    if value==float('-inf'):
        return '-inf'
    return f"{value:.3f}"


def format_pct(value):
    if value is None:
        return 'NA'
    if value==float('inf'):
        return 'inf'
    return f"{value:.3f}"


def format_pct_signed(value):
    if value is None:
        return None
    if value==float('inf'):
        return '+inf'
    if value==float('-inf'):
        return '-inf'
    return f"{value:+.3f}"


def format_actual_with_pct(actual, pct, include_pct=True):
    actual_str=format_value(actual)
    if actual is None:
        return actual_str
    if not include_pct or pct is None:
        return actual_str
    pct_str=format_pct_signed(pct)
    if pct_str is None:
        return actual_str
    return f"{actual_str} ({pct_str}%)"


def pct_to_float(value):
    if value is None:
        return 0.0
    if value==float('inf'):
        return float('inf')
    return float(value)


def parse_float_value(text):
    if text is None:
        return None
    s=text.strip()
    if not s:
        return None
    lower=s.lower()
    if lower in ('na','nan'):
        return None
    if lower in ('inf','+inf'):
        return float('inf')
    if lower=='-inf':
        return float('-inf')
    try:
        return float(s)
    except ValueError:
        return None


def average_bank_rate(rate_map, bank_count=16):
    if not rate_map:
        return None
    values=[]
    for bank in range(bank_count):
        val=rate_map.get(bank)
        if val is None:
            continue
        try:
            fval=float(val)
        except (TypeError, ValueError):
            continue
        values.append(fval)
    if not values:
        return None
    return sum(values)/len(values)


def parse_overall_cell(cell):
    if cell is None:
        return {'actual': None, 'pct': None}
    s=cell.strip()
    if not s:
        return {'actual': None, 'pct': None}
    if '(' in s and s.endswith(')'):
        actual_part, pct_part = s.split('(', 1)
        actual_val=parse_float_value(actual_part.strip().rstrip('%'))
        pct_text=pct_part[:-1].strip()
        if pct_text.endswith('%'):
            pct_text=pct_text[:-1]
        pct_val=parse_float_value(pct_text)
        return {'actual': actual_val, 'pct': pct_val}
    if s.endswith('%'):
        actual_val=parse_float_value(s[:-1])
        return {'actual': actual_val, 'pct': None}
    actual_val=parse_float_value(s)
    return {'actual': actual_val, 'pct': None}


def value_for_excel(value):
    if value is None:
        return 0.0
    if value==float('inf'):
        return None
    return round(float(value), 3)


def coalesce_metric_actual(metric_key: str, actual):
    if metric_key=='l2_global_acc_w_total_access' and actual is None:
        return 0.0
    return actual

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    ap=argparse.ArgumentParser(description='Compute performance gain percentages between base and tuned variant.')
    ap.add_argument(
        "--per-benchmark-csv-dir",
        default="",
        help="Output directory for one CSV per benchmark (split from --csv-file).",
    )        
    ap.add_argument('--sim-root',help='Path to sim_run dir (default $ACCELSIM_ROOT/../sim_run_12.1)')
    ap.add_argument('--benchmarks',nargs='*',help='Benchmarks to include (auto-discover if omitted).')
    ap.add_argument('--variants',nargs='+',required=True,help='Variants list containing base and tuned.')
    ap.add_argument('--clean-old-o', action='store_true', help='Before processing, delete old *.o* files for each variant under QV100-SASS, keeping only the newest per directory.')
    ap.add_argument('--txt-file',default='perf_gain.txt',help='Legacy TXT output file.')
    ap.add_argument('--csv-file',default='perf_gain.csv',help='CSV output file.')
    ap.add_argument('--md-file',default='perf_gain.md',help='Markdown output file.')
    ap.add_argument('--html-file',default='perf_gain.html',help='Colored HTML table output file.')
    ap.add_argument('--xlsx-file',help='Optional XLSX output file (requires openpyxl).')
    ap.add_argument('--fail-cause-xlsx', default='fail_cause_breakdown.xlsx', help='Fail cause breakdown XLSX output (requires openpyxl). Provide empty string to skip.')
    ap.add_argument('--epsilon',type=float,default=0.2,help='Percent threshold to treat as neutral (+/-). Default 0.2%%.')
    ap.add_argument('--debug-geomean',action='store_true',help='Print detailed geometric mean inputs and alternate calculations.')
    ap.add_argument('--overall-csv', default=os.path.join(SCRIPT_DIR, 'overall_perf_study.csv'), help='Aggregate CSV across studies with per-study geomean results.')
    ap.add_argument('--overall-md', default=os.path.join(SCRIPT_DIR, 'overall_perf_study.md'), help='Aggregate Markdown across studies with per-study geomean results.')
    ap.add_argument('--overall-xlsx', default=os.path.join(SCRIPT_DIR, 'overall_perf_study.xlsx'), help='Aggregate XLSX across studies (requires openpyxl).')
    ap.add_argument('--study-name', help='Override study name for overall tables (default: normalized tuned variant).')
    # Following argument is switches for items (also a must)
    # You can just comment specific item, and keep other logic, and then the item would not show in .xlxs
    ap.add_argument(
        '--overall-extra-metrics',
        nargs='*',
        default=[
            'L1D_RD_MISSES',
            'L1D_READS',
            'L1D_RD_MISS_RATE',
            'L1D_N_FILL_TO_EVICT_LINES',
            'l1d_avg_rd_byp_act',
            'l1d_avg_rd_byp_deact',
            # 'l1d_avg_rd_byp_act_rate',
            'avg_l1d_rd_miss_served_cycles',
            'intra_warp_interferences',
            'inter_warp_interferences',
            'inter_warp_interfere_percent',
            # 'L1D_MPKI',
            'non_valid_percent',
            'dep_chk_fail_percent',
            'pipe_stalled_percent',
            # 'raw_conflicts_rate_avg',
            # 'wr_reg_bank_conflicts_rate_avg',
            'total_issue_ratio',
            'issue_bw_utilization',
            'total_issue_fails',
            'g_acc_r_mq_full',
        ],
        help='Additional metrics to include in overall geomean summary (case-insensitive). '
        'Known values include: '
        'GLOBAL_ACC_R, GLOBAL_ACC_W, '
        'L2_BW, L2_accesses, L2_misses, L2_miss_rate, avg_l2_miss_served_cycles, '
        'L1D_rd_miss_rate, avg_l1d_rd_miss_served_cycles, '
        'partition_level_parallelism',
    )
    ap.add_argument(
        '--fail-total-metrics',
        nargs='*',
        default=[
            'L2_BW',
            'L2_accesses',
            'L2_misses',
            'L2_miss_rate',            
            'L1D_rd_miss_rate',
            'L1D_MPKI',
            'partition_level_parallelism',
            'avg_l2_miss_served_cycles',
            'avg_l1d_rd_miss_served_cycles',
        ],
        help='Metrics to display in Fail-total sheet (case-insensitive). Use NONE to skip defaults.',
    )
    args=ap.parse_args()
    sim_root=os.path.expanduser(os.path.expandvars(args.sim_root)) if args.sim_root else default_sim_root()
    if not sim_root: sys.exit('[ERROR] sim-root unresolved.')
    benches=args.benchmarks if args.benchmarks else discover(sim_root)
    if not benches: sys.exit('[WARN] no benchmarks found.')
    requested_variants=list(args.variants)
    if not requested_variants:
        sys.exit('[ERROR] --variants is required.')

    def _clean_old_o_files(root_dir: str, variants: List[str]) -> None:
        deleted=0
        scanned=0
        for dirpath, _dirnames, filenames in os.walk(root_dir):
            base=os.path.basename(dirpath)
            parent=os.path.basename(os.path.dirname(dirpath))
            if parent != 'QV100-SASS' or base not in variants:
                continue
            o_files=[f for f in filenames if re.match(r".*\.o(\d+)?$", f)]
            if len(o_files) <= 1:
                continue
            scanned+=1
            paths=[os.path.join(dirpath, f) for f in o_files]
            paths.sort(key=lambda p: os.path.getmtime(p), reverse=True)
            keep=paths[0]
            for path in paths[1:]:
                try:
                    os.remove(path)
                    deleted+=1
                except OSError:
                    pass
        if scanned:
            print(f"[INFO] clean-old-o: scanned {scanned} variant dirs, deleted {deleted} old .o files (kept newest per dir).")
        else:
            print("[INFO] clean-old-o: no matching variant dirs found.")

    if args.clean_old_o:
        _clean_old_o_files(sim_root, requested_variants)
    base_variant, _default_tuned = find_base_and_tuned(requested_variants)
    if not base_variant:
        base_variant=requested_variants[0]
    compare_variants=[v for v in requested_variants if v!=base_variant]
    if not compare_variants:
        compare_variants=[base_variant]

    variant_labels={base_variant: normalize_variant_name(base_variant)}
    for variant in compare_variants:
        variant_labels.setdefault(variant, normalize_variant_name(variant))
    if args.study_name and len(compare_variants)==1:
        variant_labels[compare_variants[0]]=args.study_name

    base_label=variant_labels.get(base_variant, normalize_variant_name(base_variant))

    overall_extra_requests=args.overall_extra_metrics or []
    fail_total_requests=args.fail_total_metrics or []

    raw_fail_total_tokens=[]
    for token in args.fail_total_metrics or []:
        if token is None:
            continue
        token_str=str(token).strip()
        raw_fail_total_tokens.append(token_str)
    fail_total_disabled=bool(raw_fail_total_tokens) and all(
        (not token) or token.lower() in ('none','null')
        for token in raw_fail_total_tokens
    )

    def _resolve_metric_tokens(tokens):
        resolved=[]
        unknown=[]
        for token in tokens:
            if token is None:
                continue
            token_str=str(token).strip()
            if not token_str:
                continue
            if token_str.lower() in ('none','null'):
                continue
            metric_key=resolve_metric_key(token_str)
            if not metric_key or metric_key not in METRIC_DEFINITIONS:
                unknown.append(token_str)
                continue
            resolved.append(metric_key)
        return resolved, unknown

    overall_extra_resolved, overall_extra_unknown=_resolve_metric_tokens(overall_extra_requests)
    fail_total_resolved, fail_total_unknown=_resolve_metric_tokens(fail_total_requests)

    unknown_metrics=sorted(set(overall_extra_unknown + fail_total_unknown))
    if unknown_metrics:
        sys.exit(f"[ERROR] Unknown metrics requested via --overall-extra-metrics/--fail-total-metrics: {', '.join(unknown_metrics)}")

    fail_total_metric_keys=[]
    if not fail_total_disabled:
        for metric in fail_total_resolved:
            if metric not in fail_total_metric_keys:
                fail_total_metric_keys.append(metric)

    extra_metric_keys=[]

    def _maybe_add_extra(metric):
        if metric in ('global_acc_r','global_acc_w'):
            return
        if metric not in extra_metric_keys:
            extra_metric_keys.append(metric)

    for metric in overall_extra_resolved:
        _maybe_add_extra(metric)
    if not fail_total_disabled:
        for metric in fail_total_metric_keys:
            _maybe_add_extra(metric)

    extra_metric_keys=[metric for metric in extra_metric_keys if metric not in DEFAULT_METRIC_ORDER]

    optional_summary_metrics=set()
    for metric in overall_extra_resolved:
        if metric in ('global_acc_r','global_acc_w'):
            optional_summary_metrics.add(metric)
    if not fail_total_disabled:
        for metric in fail_total_metric_keys:
            if metric in ('global_acc_r','global_acc_w'):
                optional_summary_metrics.add(metric)

    primary_overall_metrics=['ipc']
    for metric in ('global_acc_r','global_acc_w'):
        if metric in optional_summary_metrics and metric not in primary_overall_metrics:
            primary_overall_metrics.append(metric)

    def summary_metric_label(metric_key: str) -> str:
        if metric_key=='ipc':
            return 'IPC'
        if metric_key=='global_acc_r':
            return 'GLOBAL_ACC_R'
        if metric_key=='global_acc_w':
            return 'GLOBAL_ACC_W'
        return METRIC_LABELS.get(metric_key, metric_key)
    extra_metric_actual_by_label=defaultdict(dict)
    base_extra_metrics_ref=None

    ordered_variant_labels=[]
    _seen_variant_labels=set()

    def _register_variant_label(label: str):
        if not label or label in _seen_variant_labels:
            return
        _seen_variant_labels.add(label)
        ordered_variant_labels.append(label)

    _register_variant_label(base_label)
    for variant in compare_variants:
        _register_variant_label(variant_labels.get(variant, variant))

    header_cols=['variant','benchmark','kernel_index','ipc_base','ipc_tuned','ipc_gain_pct','read_base','read_tuned','read_change_pct','write_base','write_tuned','write_change_pct']
    csv_header_extended=header_cols + ['ipc_gain_class','read_change_class','write_change_class']
    avg_header=['variant','benchmark','ipc_gain_pct','read_change_pct','write_change_pct']

    rows_all=[]
    md_rows_all=[]
    avg_rows_all=[]
    md_avg_rows_all=[]
    bench_pct_records_ordered=[]

    variant_results={
        variant: {
            'rows': [],
            'md_rows': [],
            'avg_rows': [],
            'md_avg_rows': [],
            'bench_pct_records': [],
            'metric_geomean_inputs': {metric: {'base': [], 'tuned': []} for metric in METRIC_ORDER},
            'metric_ratios': {metric: [] for metric in METRIC_ORDER},
            'extra_metric_geo_inputs': {metric: {'base': [], 'tuned': []} for metric in extra_metric_keys},
            'extra_metric_ratios': {metric: [] for metric in extra_metric_keys},
        }
        for variant in compare_variants
    }

    per_kernel_cause_records=defaultdict(list)
    per_kernel_driver_records=defaultdict(list)
    per_kernel_bank_conflict_records=defaultdict(list)

    base_fail_causes={
        'global_acc_r': defaultdict(int),
        'global_acc_w': defaultdict(int),
    }
    variant_fail_causes={
        variant: {
            'global_acc_r': defaultdict(int),
            'global_acc_w': defaultdict(int),
        }
        for variant in compare_variants
    }

    fail_cause_bench_summary={}
    fail_cause_overall_entries={}
    base_fail_cause_overall={}
    tracked_fail_causes=[]
    fail_metric_keys=[]
    fail_metric_labels={}
    fail_cause_bench_order=[]

    def accumulate_fail_causes(target, records):
        for rec in records:
            for cause, count in rec.get('r_reasons', {}).items():
                try:
                    amt=int(count)
                except (TypeError, ValueError):
                    continue
                target['global_acc_r'][cause]+=amt
            for cause, count in rec.get('w_reasons', {}).items():
                try:
                    amt=int(count)
                except (TypeError, ValueError):
                    continue
                target['global_acc_w'][cause]+=amt

    def make_kernel_label(index: int, kernel_name) -> str:
        return f"k{index}"

    def record_per_kernel_details(variant_label: str, bench_name: str, records):
        if not records:
            return
        for idx, rec in enumerate(records, start=1):
            kernel_name=rec.get('kernel')
            kernel_label=make_kernel_label(idx, kernel_name)
            for access_type, total_key, reason_key, driver_key in (
                ('GLOBAL_ACC_R', 'r_total', 'r_reasons', 'r_drivers'),
                ('GLOBAL_ACC_W', 'w_total', 'w_reasons', 'w_drivers'),
            ):
                total=rec.get(total_key) or 0
                try:
                    total_int=int(total)
                except (TypeError, ValueError):
                    total_int=0
                raw_reasons=rec.get(reason_key) or {}
                numeric_reasons={}
                for cause, count in raw_reasons.items():
                    try:
                        val=int(count)
                    except (TypeError, ValueError):
                        continue
                    if val<=0:
                        continue
                    numeric_reasons[cause]=val
                if not numeric_reasons:
                    continue
                effective_total=total_int if total_int>0 else sum(numeric_reasons.values())
                if effective_total<=0:
                    continue
                for cause, fails in numeric_reasons.items():
                    pct=(fails/effective_total*100.0) if effective_total else 0.0
                    per_kernel_cause_records[variant_label].append({
                        'benchmark': bench_name,
                        'kernel': kernel_label,
                        'kernel_index': idx,
                        'access_type': access_type,
                        'cause': cause,
                        'fails': fails,
                        'pct': pct,
                    })
                    driver_map=(rec.get(driver_key) or {}).get(cause, {})
                    if not driver_map:
                        continue
                    cause_total=fails
                    for driver, driver_count in driver_map.items():
                        try:
                            driver_fails=int(driver_count)
                        except (TypeError, ValueError):
                            continue
                        if driver_fails<=0:
                            continue
                        driver_pct=(driver_fails/cause_total*100.0) if cause_total else 0.0
                        per_kernel_driver_records[variant_label].append({
                            'benchmark': bench_name,
                            'kernel': kernel_label,
                            'kernel_index': idx,
                            'access_type': access_type,
                            'cause': cause,
                            'driver': driver,
                            'fails': driver_fails,
                            'pct': driver_pct,
                            'cause_total': cause_total,
                        })
            raw_rates=rec.get('raw_conflicts_rate_by_bank') or {}
            wr_rates=rec.get('wr_reg_bank_conflicts_rate_by_bank') or {}
            if raw_rates or wr_rates:
                all_banks=set(raw_rates.keys()) | set(wr_rates.keys())
                for bank in sorted(all_banks):
                    raw_val=raw_rates.get(bank)
                    wr_val=wr_rates.get(bank)
                    if raw_val is None and wr_val is None:
                        continue
                    per_kernel_bank_conflict_records[variant_label].append({
                        'benchmark': bench_name,
                        'kernel': kernel_label,
                        'kernel_index': idx,
                        'bank': bank,
                        'raw_conflicts_rate': raw_val,
                        'wr_reg_bank_conflicts_rate': wr_val,
                    })

    def sanitize_sheet_name(name: str) -> str:
        invalid=set('[]:*?/\\')
        cleaned=''.join('_' if ch in invalid else ch for ch in name)
        cleaned=cleaned.strip()
        if not cleaned:
            cleaned='Sheet'
        return cleaned[:31]

    def write_fail_table(ws, start_row, metric_key, base_counts, base_total, variant_label, variant_counts, sort_counts):
        metric_title=METRIC_LABELS.get(metric_key, metric_key)
        variant_total=sum(variant_counts.values())
        ws.cell(start_row,1).value=metric_title
        ws.cell(start_row,2).value=f'{variant_label} total: {variant_total}'
        ws.cell(start_row,4).value=f'Base total: {base_total}'
        headers=['Cause','Base Count','Base %',f'{variant_label} Count',f'{variant_label} %','Delta Count','Delta %']
        for col, header in enumerate(headers, start=1):
            ws.cell(start_row+1,col).value=header
        combined=set(base_counts.keys()) | set(variant_counts.keys())
        if not combined:
            ws.cell(start_row+2,1).value='No fail causes'
            return start_row+4
        sorted_causes=sorted(
            combined,
            key=lambda c: (-sort_counts.get(c, 0), c)
        )
        row=start_row+2
        for cause in sorted_causes:
            base_count=base_counts.get(cause,0)
            variant_count=variant_counts.get(cause,0)
            base_pct=(base_count/base_total*100.0) if base_total else 0.0
            variant_pct=(variant_count/variant_total*100.0) if variant_total else 0.0
            delta_count=variant_count-base_count
            delta_pct=variant_pct-base_pct
            values=[cause, base_count, round(base_pct,3), variant_count, round(variant_pct,3), delta_count, round(delta_pct,3)]
            for col, value in enumerate(values, start=1):
                ws.cell(row,col).value=value
            row+=1
        return row+2

    sheet_name_registry=set()

    def unique_sheet_name(label: str) -> str:
        base=sanitize_sheet_name(label)
        candidate=base
        suffix=1
        while candidate in sheet_name_registry:
            suffix_str=f"_{suffix}"
            max_len=max(1, 31-len(suffix_str))
            trimmed=base[:max_len]
            if not trimmed.strip():
                trimmed='Sheet'
            candidate=f"{trimmed}{suffix_str}"
            suffix+=1
        sheet_name_registry.add(candidate)
        return candidate

    def align_variant_records(base_records, tuned_records):
        base_list=list(base_records)
        tuned_list=list(tuned_records)
        target_len=max(len(base_list), len(tuned_list))
        if target_len==0:
            return [], [], 0

        def extend(records):
            if not records:
                return []
            if len(records)>=target_len:
                return list(records[:target_len])
            return list(records) + [records[-1]]*(target_len-len(records))

        return extend(base_list), extend(tuned_list), target_len

    def classify_change(value, metric_type):
        if value is None:
            return 'neutral'
        better_is_greater=METRIC_ORIENTATION.get(metric_type, False)
        if metric_type.startswith('fail::'):
            better_is_greater=False
        if value==float('inf'):
            return 'better' if better_is_greater else 'worse'
        if value==float('-inf'):
            return 'worse' if better_is_greater else 'better'
        if better_is_greater:
            if value>0:
                return 'better'
            if value<0:
                return 'worse'
            return 'neutral'
        if value<0:
            return 'better'
        if value>0:
            return 'worse'
        return 'neutral'

    def format_colored_pct(value, metric_name):
        display=format_pct(value)
        if value is None or display=='NA':
            return display
        metric_class=classify_change(value, metric_name)
        if metric_class=='better':
            return f"<span style='background-color:#d4f5d4'>{display}</span>"
        if metric_class=='worse':
            return f"<span style='background-color:#f8d0d0'>{display}</span>"
        return display
#
    def geometric_mean_from_records(records, value_key):
        if not records:
            return None
        values=[]
        for rec in records:
            val=rec.get(value_key)
            if val is None:
                continue
            try:
                fval=float(val)
            except (TypeError, ValueError):
                continue
            if math.isnan(fval):
                continue
            values.append(max(fval, 0.0))
        if not values:
            return None
        positive_values=[v for v in values if v>0.0]
        if len(positive_values)==len(values):
            log_sum=sum(math.log(v) for v in positive_values)
            return math.exp(log_sum/len(positive_values))
        if not positive_values:
            return 0.0
        log_sum=sum(math.log(v+1.0) for v in values)
        return math.exp(log_sum/len(values))-1.0


    def last_valid_metric_from_records(records, value_key):
        for rec in reversed(records or []):
            val=rec.get(value_key)
            if val is None:
                continue
            try:
                fval=float(val)
            except (TypeError, ValueError):
                continue
            if math.isnan(fval):
                continue
            return fval
        return None
#
    base_cache={}
    for bench in benches:
        base_data=base_cache.get(bench)
        if base_data is None:
            base_data=collect_variant(sim_root, bench, base_variant)
            base_cache[bench]=base_data
        if base_data:
            accumulate_fail_causes(base_fail_causes, base_data)
            record_per_kernel_details(base_label, bench, base_data)
        if not base_data:
            continue

        for variant in compare_variants:
            tuned_data=collect_variant(sim_root, bench, variant)
            if not tuned_data:
                continue
            accumulate_fail_causes(variant_fail_causes[variant], tuned_data)
            variant_label=variant_labels.get(variant, variant)
            if variant != base_variant:
                record_per_kernel_details(variant_label, bench, tuned_data)
            base_aligned, tuned_aligned, kernel_count=align_variant_records(base_data, tuned_data)
            if kernel_count==0:
                continue

            result=variant_results[variant]

            def color_wrap(val, is_good, is_bad):
                if is_good:
                    return f"<span style='background-color:#d4f5d4'>{val}</span>"
                if is_bad:
                    return f"<span style='background-color:#f8d0d0'>{val}</span>"
                return val

            for idx in range(kernel_count):
                b_record=base_aligned[idx]
                t_record=tuned_aligned[idx]
                base_ipc=b_record.get('ipc')
                tuned_ipc=t_record.get('ipc')
                ipc_gain=pct_change(tuned_ipc, base_ipc) if base_ipc is not None and tuned_ipc is not None else 0.0
                read_change=pct_change(t_record.get('r_total'), b_record.get('r_total'))
                write_change=pct_change(t_record.get('w_total'), b_record.get('w_total'))

                ipc_class=classify_change(ipc_gain, 'ipc')
                read_class=classify_change(read_change, 'global_acc_r')
                write_class=classify_change(write_change, 'global_acc_w')

                ipc_gain_str='inf' if ipc_gain==float('inf') else f"{ipc_gain:.3f}"
                read_change_str='inf' if read_change==float('inf') else f"{read_change:.3f}"
                write_change_str='inf' if write_change==float('inf') else f"{write_change:.3f}"

                row=[
                    variant_label,
                    bench,
                    str(idx+1),
                    str(b_record.get('ipc')),
                    str(t_record.get('ipc')),
                    ipc_gain_str,
                    str(b_record.get('r_total')),
                    str(t_record.get('r_total')),
                    read_change_str,
                    str(b_record.get('w_total')),
                    str(t_record.get('w_total')),
                    write_change_str,
                    ipc_class,
                    read_class,
                    write_class,
                ]
                result['rows'].append(row)
                rows_all.append(row)

                md_row=[
                    variant_label,
                    bench,
                    str(idx+1),
                    str(b_record.get('ipc')),
                    str(t_record.get('ipc')),
                    color_wrap(ipc_gain_str, ipc_class=='better', ipc_class=='worse'),
                    str(b_record.get('r_total')),
                    str(t_record.get('r_total')),
                    color_wrap(read_change_str, read_class=='better', read_class=='worse'),
                    str(b_record.get('w_total')),
                    str(t_record.get('w_total')),
                    color_wrap(write_change_str, write_class=='better', write_class=='worse'),
                ]
                result['md_rows'].append(md_row)
                md_rows_all.append(md_row)

            bench_metric_pct={}
            for metric in METRIC_ORDER:
                key=METRIC_VALUE_KEYS[metric]

                if metric in LAST_VALUE_METRICS:
                    # Use the final benchmark value (last valid record), not kernel geomean.
                    base_metric_val=last_valid_metric_from_records(base_aligned, key)
                    tuned_metric_val=last_valid_metric_from_records(tuned_aligned, key)
                    ratio=ratio_from_geomeans(base_metric_val, tuned_metric_val)
                    pct=ratio_to_pct(ratio)
                    bench_metric_pct[metric]=pct
                    if base_metric_val is not None:
                        result['metric_geomean_inputs'][metric]['base'].append(base_metric_val)
                    if tuned_metric_val is not None:
                        result['metric_geomean_inputs'][metric]['tuned'].append(tuned_metric_val)
                    if ratio is not None:
                        result['metric_ratios'][metric].append(ratio)
                    continue
                                    
                base_geo=geometric_mean_from_records(base_aligned, key)
                tuned_geo=geometric_mean_from_records(tuned_aligned, key)
                ratio=ratio_from_geomeans(base_geo, tuned_geo)
                pct=ratio_to_pct(ratio)
                bench_metric_pct[metric]=pct
                if base_geo is not None:
                    result['metric_geomean_inputs'][metric]['base'].append(base_geo)
                if tuned_geo is not None:
                    result['metric_geomean_inputs'][metric]['tuned'].append(tuned_geo)
                if ratio is not None:
                    result['metric_ratios'][metric].append(ratio)

            for metric in extra_metric_keys:
                key=METRIC_VALUE_KEYS[metric]
                if metric in LAST_VALUE_METRICS:
                    base_geo=last_valid_metric_from_records(base_aligned, key)
                    tuned_geo=last_valid_metric_from_records(tuned_aligned, key)
                else:
                    base_geo=geometric_mean_from_records(base_aligned, key)
                    tuned_geo=geometric_mean_from_records(tuned_aligned, key)
                ratio=ratio_from_geomeans(base_geo, tuned_geo)
                if base_geo is not None:
                    result['extra_metric_geo_inputs'][metric]['base'].append(base_geo)
                if tuned_geo is not None:
                    result['extra_metric_geo_inputs'][metric]['tuned'].append(tuned_geo)
                if ratio is not None:
                    result['extra_metric_ratios'][metric].append(ratio)

            avg_row=[
                variant_label,
                bench,
                format_pct(bench_metric_pct.get('ipc')),
                format_pct(bench_metric_pct.get('global_acc_r')),
                format_pct(bench_metric_pct.get('global_acc_w')),
            ]
            result['avg_rows'].append(avg_row)
            avg_rows_all.append(avg_row)

            md_avg_row=[
                variant_label,
                bench,
                format_colored_pct(bench_metric_pct.get('ipc'), 'ipc'),
                format_colored_pct(bench_metric_pct.get('global_acc_r'), 'global_acc_r'),
                format_colored_pct(bench_metric_pct.get('global_acc_w'), 'global_acc_w'),
            ]
            result['md_avg_rows'].append(md_avg_row)
            md_avg_rows_all.append(md_avg_row)

            result['bench_pct_records'].append((bench, bench_metric_pct))
            bench_pct_records_ordered.append((variant, bench, bench_metric_pct))

    overall_entries=[]
    base_metrics_ref=None
    missing_variants=[]
    for variant in compare_variants:
        variant_data=variant_results[variant]
        bench_pct_records=variant_data['bench_pct_records']
        if not bench_pct_records:
            missing_variants.append(variant_labels.get(variant, variant))
            continue

        metric_geo_pct={}
        metric_geo_base={}
        metric_geo_tuned={}
        for metric in METRIC_ORDER:
            inputs=variant_data['metric_geomean_inputs'][metric]
            base_geo=geometric_mean(inputs['base'])
            tuned_geo=geometric_mean(inputs['tuned'])
            ratio=ratio_from_geomeans(base_geo, tuned_geo)
            metric_geo_pct[metric]=ratio_to_pct(ratio)
            metric_geo_base[metric]=base_geo
            metric_geo_tuned[metric]=tuned_geo

        extra_metric_geo_pct={}
        extra_metric_geo_base={}
        extra_metric_geo_tuned={}
        for metric in extra_metric_keys:
            inputs_extra=variant_data['extra_metric_geo_inputs'][metric]
            base_geo=geometric_mean(inputs_extra['base']) if inputs_extra['base'] else None
            tuned_geo=geometric_mean(inputs_extra['tuned']) if inputs_extra['tuned'] else None
            ratio=ratio_from_geomeans(base_geo, tuned_geo)
            extra_metric_geo_pct[metric]=ratio_to_pct(ratio)
            extra_metric_geo_base[metric]=base_geo
            extra_metric_geo_tuned[metric]=tuned_geo

        eps=args.epsilon

        def count_wins(metric):
            better_is_greater=METRIC_ORIENTATION.get(metric, False)
            wins=losses=neutrals=0
            for _, pct_map in bench_pct_records:
                val=pct_map.get(metric)
                if val is None:
                    neutrals+=1
                    continue
                if val==float('inf'):
                    if better_is_greater:
                        wins+=1
                    else:
                        losses+=1
                    continue
                if abs(val)<=eps:
                    neutrals+=1
                elif val>0:
                    if better_is_greater:
                        wins+=1
                    else:
                        losses+=1
                else:
                    if better_is_greater:
                        losses+=1
                    else:
                        wins+=1
            return wins, losses, neutrals

        win_loss_stats={}
        for metric in primary_overall_metrics:
            win_loss_stats[metric]=count_wins(metric)

        variant_label=variant_labels.get(variant, variant)
        lines=[f"GEOMETRIC MEAN SUMMARY ({variant_label})"]
        for metric in primary_overall_metrics:
            label=summary_metric_label(metric)
            lines.append(f"{label} geomean percent change: {format_pct(metric_geo_pct.get(metric))}%")
            if metric in ('global_acc_r','global_acc_w'):
                wins, losses, neutrals=win_loss_stats.get(metric, (0,0,0))
                lines.append(f"{label} win/loss/neutral benchmarks: {wins}/{losses}/{neutrals}")

        added_summary_metrics=set(METRIC_ORDER)
        for metric in extra_metric_keys:
            if metric in added_summary_metrics:
                continue
            lines.append(f"{METRIC_LABELS.get(metric, metric)} geomean percent change: {format_pct(extra_metric_geo_pct.get(metric))}%")
            added_summary_metrics.add(metric)

        if args.debug_geomean:
            print(f"[DEBUG] Bench-level geomean ratios for {variant_label}:")
            for metric, ratios in variant_data['metric_ratios'].items():
                print(f'  {metric}:', ratios)
            print(f"[DEBUG] Bench-level percent changes for {variant_label}:")
            for bench_name, pct_map in bench_pct_records:
                print(f"  {bench_name}: ipc={pct_map.get('ipc')}%, global_acc_r={pct_map.get('global_acc_r')}%, global_acc_w={pct_map.get('global_acc_w')}%")

        variant_data['metric_geo_pct']=metric_geo_pct
        variant_data['metric_geo_base']=metric_geo_base
        variant_data['metric_geo_tuned']=metric_geo_tuned
        variant_data['extra_metric_geo_pct']=extra_metric_geo_pct
        variant_data['extra_metric_geo_base']=extra_metric_geo_base
        variant_data['extra_metric_geo_tuned']=extra_metric_geo_tuned
        variant_data['overall_lines']=lines

        if base_extra_metrics_ref is None:
            base_extra_metrics_ref=extra_metric_geo_base
            extra_metric_actual_by_label[base_label]={metric: coalesce_metric_actual(metric, value) for metric, value in extra_metric_geo_base.items()}
        elif base_label not in extra_metric_actual_by_label:
            extra_metric_actual_by_label[base_label]={metric: coalesce_metric_actual(metric, value) for metric, value in extra_metric_geo_base.items()}

        extra_metric_actual_by_label[variant_label]={metric: coalesce_metric_actual(metric, value) for metric, value in extra_metric_geo_tuned.items()}

        overall_entries.append({
            'variant': variant,
            'label': variant_label,
            'overall_lines': lines,
            'metric_geo_pct': metric_geo_pct,
            'metric_geo_base': metric_geo_base,
            'metric_geo_tuned': metric_geo_tuned,
            'extra_metric_geo_pct': extra_metric_geo_pct,
            'extra_metric_geo_base': extra_metric_geo_base,
            'extra_metric_geo_tuned': extra_metric_geo_tuned,
        })

        if base_metrics_ref is None:
            base_metrics_ref=metric_geo_base
        if base_extra_metrics_ref is None:
            base_extra_metrics_ref=extra_metric_geo_base

    if base_label in per_kernel_cause_records and per_kernel_cause_records[base_label]:
        def _build_cause_map(records):
            mapping=defaultdict(lambda: defaultdict(dict))
            for rec in records or []:
                bench=rec.get('benchmark')
                kernel_index=rec.get('kernel_index')
                cause=rec.get('cause')
                fails=rec.get('fails')
                if bench is None or kernel_index is None or cause is None:
                    continue
                try:
                    kernel_idx=int(kernel_index)
                    fail_count=int(fails)
                except (TypeError, ValueError):
                    continue
                if fail_count < 0:
                    continue
                mapping[bench].setdefault(kernel_idx, {})[cause]=fail_count
            return mapping

        base_cause_map=_build_cause_map(per_kernel_cause_records.get(base_label, []))
        cause_totals_base=defaultdict(int)
        for bench_map in base_cause_map.values():
            for kernel_map in bench_map.values():
                for cause, count in kernel_map.items():
                    try:
                        cause_totals_base[cause]+=int(count)
                    except (TypeError, ValueError):
                        continue

        aggregated_fail_totals=defaultdict(int)
        for label_records in per_kernel_cause_records.values():
            for rec in label_records or []:
                cause=rec.get('cause')
                fails_val=rec.get('fails')
                if not cause:
                    continue
                try:
                    fails_int=int(fails_val)
                except (TypeError, ValueError):
                    continue
                if fails_int<=0:
                    continue
                aggregated_fail_totals[cause]+=fails_int

        if aggregated_fail_totals:
            tracked_fail_causes=[cause for cause, _ in sorted(aggregated_fail_totals.items(), key=lambda item: (-item[1], item[0]))]
        else:
            tracked_fail_causes=[cause for cause in DEFAULT_FAIL_CAUSE_TYPES if cause_totals_base.get(cause, 0)>0]

        if tracked_fail_causes:
            if fail_total_disabled:
                fail_metric_keys=[]
            else:
                fail_metric_keys=[f"fail::{cause}" for cause in tracked_fail_causes]
                fail_metric_labels={f"fail::{cause}": cause for cause in tracked_fail_causes}
                METRIC_LABELS.update(fail_metric_labels)

            fail_cause_bench_order=sorted(base_cause_map.keys())
            fail_cause_bench_summary={label: {} for label in ordered_variant_labels}
            fail_cause_overall_values=defaultdict(lambda: defaultdict(lambda: {'base': [], 'tuned': []}))

            for label in ordered_variant_labels:
                variant_map=_build_cause_map(per_kernel_cause_records.get(label, []))
                bench_summary=fail_cause_bench_summary.setdefault(label, {})
                for bench in fail_cause_bench_order:
                    base_kernel_map=base_cause_map.get(bench)
                    if not base_kernel_map:
                        continue
                    kernel_indices=sorted(base_kernel_map.keys())
                    if not kernel_indices:
                        continue
                    bench_entry=bench_summary.setdefault(bench, {})
                    for cause in tracked_fail_causes:
                        base_values=[]
                        tuned_values=[]
                        for idx in kernel_indices:
                            base_values.append(int(base_kernel_map[idx].get(cause, 0)))
                            tuned_values.append(int(variant_map.get(bench, {}).get(idx, {}).get(cause, 0)))
                        base_geo=geometric_mean(base_values) if base_values else None
                        tuned_geo=geometric_mean(tuned_values) if tuned_values else None
                        ratio=ratio_from_geomeans(base_geo, tuned_geo)
                        pct=ratio_to_pct(ratio)
                        bench_entry[cause]={
                            'base_geo': base_geo,
                            'tuned_geo': tuned_geo,
                            'ratio': ratio,
                            'pct': pct,
                        }
                        if base_geo is not None:
                            fail_cause_overall_values[label][cause]['base'].append(base_geo)
                        if tuned_geo is not None:
                            fail_cause_overall_values[label][cause]['tuned'].append(tuned_geo)

            fail_cause_overall_entries={}
            base_fail_cause_overall={}
            for label, cause_map in fail_cause_overall_values.items():
                summary={}
                for cause, values in cause_map.items():
                    base_geo=geometric_mean(values['base']) if values['base'] else None
                    tuned_geo=geometric_mean(values['tuned']) if values['tuned'] else None
                    ratio=ratio_from_geomeans(base_geo, tuned_geo)
                    pct=ratio_to_pct(ratio)
                    summary[cause]={
                        'actual': tuned_geo,
                        'pct': pct,
                        'base_actual': base_geo,
                    }
                    if label==base_label:
                        base_fail_cause_overall[cause]=base_geo
                if summary:
                    fail_cause_overall_entries[label]=summary

            overall_entry_map={entry['label']: entry for entry in overall_entries}
            if base_label not in fail_cause_overall_entries:
                fail_cause_overall_entries[base_label]={}
            if base_metrics_ref:
                base_fail_cause_overall['GLOBAL_ACC_R']=base_metrics_ref.get('global_acc_r')
                base_fail_cause_overall['GLOBAL_ACC_W']=base_metrics_ref.get('global_acc_w')
                fail_cause_overall_entries[base_label]['GLOBAL_ACC_R']={
                    'actual': base_metrics_ref.get('global_acc_r'),
                    'pct': None,
                }
                fail_cause_overall_entries[base_label]['GLOBAL_ACC_W']={
                    'actual': base_metrics_ref.get('global_acc_w'),
                    'pct': None,
                }
            for label, entry in overall_entry_map.items():
                summary=fail_cause_overall_entries.setdefault(label, {})
                summary['GLOBAL_ACC_R']={
                    'actual': entry['metric_geo_tuned'].get('global_acc_r'),
                    'pct': entry['metric_geo_pct'].get('global_acc_r'),
                }
                summary['GLOBAL_ACC_W']={
                    'actual': entry['metric_geo_tuned'].get('global_acc_w'),
                    'pct': entry['metric_geo_pct'].get('global_acc_w'),
                }

    if missing_variants:
        print(f"[WARN] no benchmark data found for: {', '.join(missing_variants)}")

    if tracked_fail_causes and not fail_total_disabled:
        for entry in overall_entries:
            fail_summary=fail_cause_overall_entries.get(entry['label'])
            if not fail_summary:
                continue
            for cause in tracked_fail_causes:
                pct_val=(fail_summary.get(cause) or {}).get('pct')
                entry['overall_lines'].append(f"{cause} geomean percent change: {format_pct(pct_val)}%")

    overall_summary_rows=[]
    overall_metric_map={}
    overall_order=[]
    overall_header_labels=None

    # TXT legacy
    txt_lines=[' '.join(csv_header_extended)]
    txt_lines.extend([' '.join(r) for r in rows_all])
    txt_lines.append('')
    txt_lines.append(' '.join(avg_header))
    for a in avg_rows_all:
        txt_lines.append(' '.join(a))
    for entry in overall_entries:
        txt_lines.append('')
        txt_lines.extend(entry['overall_lines'])
    with open(args.txt_file,'w') as f:
        f.write('\n'.join(txt_lines))
    print(f"[INFO] wrote {args.txt_file}")

    import csv
    with open(args.csv_file,'w',newline='') as cf:
        w=csv.writer(cf)
        w.writerow(csv_header_extended)
        for r in rows_all:
            w.writerow(r)
        w.writerow([])
        w.writerow(avg_header)
        for a in avg_rows_all:
            w.writerow(a)
        if overall_entries:
            w.writerow([])
            overall_csv_header=['variant'] + [f"{METRIC_LABELS.get(metric, metric)}_geomean_pct" for metric in primary_overall_metrics]
            if tracked_fail_causes and not fail_total_disabled:
                for cause in tracked_fail_causes:
                    overall_csv_header.append(f"{cause}_geomean_pct")
            w.writerow(overall_csv_header)
            for entry in overall_entries:
                metric_geo_pct=entry['metric_geo_pct']
                row=[entry['label']]
                for metric in primary_overall_metrics:
                    row.append(format_pct(metric_geo_pct.get(metric)))
                if tracked_fail_causes and not fail_total_disabled:
                    fail_summary=fail_cause_overall_entries.get(entry['label'], {})
                    for cause in tracked_fail_causes:
                        pct_val=(fail_summary.get(cause) or {}).get('pct')
                        row.append(format_pct(pct_val))
                w.writerow(row)
    print(f"[INFO] wrote {args.csv_file}")    
    if args.per_benchmark_csv_dir:
        split_overall_csv_by_benchmark(args.csv_file, args.per_benchmark_csv_dir)    

    md_lines=[
        "# Performance Gain Report",
        "",
        "## Per-Kernel Details (colored)",
        "",
        '|'+'|'.join(header_cols)+'|',
        '|'+'|'.join(['---']*len(header_cols))+'|'
    ]
    for r in md_rows_all:
        md_lines.append('|'+'|'.join(r)+'|')
    md_lines.append('')
    md_lines.append('## Averages')
    md_lines.append('')
    md_lines.append('|variant|benchmark|ipc_gain_pct|read_change_pct|write_change_pct|')
    md_lines.append('|---|---|---|---|---|')
    for a in md_avg_rows_all:
        md_lines.append(f"|{a[0]}|{a[1]}|{a[2]}|{a[3]}|{a[4]}|")
    if overall_entries:
        md_lines.append('')
        md_lines.append('## Overall Summary')
        for entry in overall_entries:
            md_lines.append('')
            md_lines.append(f"### {entry['label']}")
            md_lines.append('')
            for metric in primary_overall_metrics:
                label=summary_metric_label(metric)
                pct_val=entry['metric_geo_pct'].get(metric)
                md_lines.append(f"- {label} geomean percent change: <b>{format_pct(pct_val)}%</b>")
            for metric in extra_metric_keys:
                if metric in METRIC_ORDER:
                    continue
                pct_val=entry['extra_metric_geo_pct'].get(metric)
                md_lines.append(f"- {METRIC_LABELS.get(metric, metric)} geomean percent change: <b>{format_pct(pct_val)}%</b>")
            if tracked_fail_causes and not fail_total_disabled:
                fail_summary=fail_cause_overall_entries.get(entry['label'])
                if fail_summary:
                    for cause in tracked_fail_causes:
                        pct_val=(fail_summary.get(cause) or {}).get('pct')
                        md_lines.append(f"- {cause} geomean percent change: <b>{format_pct(pct_val)}%</b>")
        if md_lines and md_lines[-1]=='':
            md_lines.pop()
    with open(args.md_file,'w') as mf:
        mf.write('\n'.join(md_lines))
    print(f"[INFO] wrote {args.md_file}")

    html_lines=["<html><head><meta charset='utf-8'><title>Performance Gain Report</title><style>table{border-collapse:collapse;font-family:monospace;} td,th{border:1px solid #888;padding:4px;} .better{background:#d4f5d4;} .worse{background:#f8d0d0;} .neutral{background:#f0f0f0;}</style></head><body>","<h1>Performance Gain Report</h1>"]
    html_lines.append('<h2>Per-Kernel Details</h2>')
    html_lines.append('<table>')
    html_lines.append('<tr>' + ''.join(f'<th>{c}</th>' for c in header_cols) + '</tr>')
    for raw in rows_all:
        ipc_class=raw[-3]
        read_class=raw[-2]
        write_class=raw[-1]
        html_lines.append('<tr>' +
            f'<td>{raw[0]}</td>' +
            f'<td>{raw[1]}</td>' +
            f'<td>{raw[2]}</td>' +
            f'<td>{raw[3]}</td>' +
            f'<td>{raw[4]}</td>' +
            f'<td class="{ipc_class}">{raw[5]}</td>' +
            f'<td>{raw[6]}</td>' +
            f'<td>{raw[7]}</td>' +
            f'<td class="{read_class}">{raw[8]}</td>' +
            f'<td>{raw[9]}</td>' +
            f'<td>{raw[10]}</td>' +
            f'<td class="{write_class}">{raw[11]}</td>' +
            '</tr>')
    html_lines.append('</table>')
    html_lines.append('<h2>Averages</h2>')
    html_lines.append('<table>')
    html_lines.append('<tr><th>variant</th><th>benchmark</th><th>ipc_gain_pct</th><th>read_change_pct</th><th>write_change_pct</th></tr>')
    for (_, _, pct_map), avg_row in zip(bench_pct_records_ordered, avg_rows_all):
        ipc_class=classify_change(pct_map.get('ipc'), 'ipc')
        read_class=classify_change(pct_map.get('global_acc_r'), 'global_acc_r')
        write_class=classify_change(pct_map.get('global_acc_w'), 'global_acc_w')
        html_lines.append('<tr>' +
            f'<td>{avg_row[0]}</td>' +
            f'<td>{avg_row[1]}</td>' +
            f'<td class="{ipc_class}">{avg_row[2]}</td>' +
            f'<td class="{read_class}">{avg_row[3]}</td>' +
            f'<td class="{write_class}">{avg_row[4]}</td>' +
            '</tr>')
    html_lines.append('</table>')
    if overall_entries:
        html_lines.append('<h2>Overall Summary</h2>')
        for entry in overall_entries:
            html_lines.append(f"<h3>{entry['label']}</h3>")
            html_lines.append('<ul>')
            for metric in primary_overall_metrics:
                label=summary_metric_label(metric)
                pct_val=entry['metric_geo_pct'].get(metric)
                html_lines.append(f"<li>{label} geomean percent change: <b>{format_pct(pct_val)}%</b></li>")
            for metric in extra_metric_keys:
                if metric in METRIC_ORDER:
                    continue
                pct_val=entry['extra_metric_geo_pct'].get(metric)
                html_lines.append(f"<li>{METRIC_LABELS.get(metric, metric)} geomean percent change: <b>{format_pct(pct_val)}%</b></li>")
            if tracked_fail_causes and not fail_total_disabled:
                fail_summary=fail_cause_overall_entries.get(entry['label'])
                if fail_summary:
                    for cause in tracked_fail_causes:
                        pct_val=(fail_summary.get(cause) or {}).get('pct')
                        html_lines.append(f"<li>{cause} geomean percent change: <b>{format_pct(pct_val)}%</b></li>")
            html_lines.append('</ul>')
    html_lines.append('</body></html>')
    with open(args.html_file,'w') as hf:
        hf.write('\n'.join(html_lines))
    print(f"[INFO] wrote {args.html_file}")

    if overall_entries:
        combined_metric_keys=[]

        def _append_metric(metric_key):
            if metric_key and metric_key not in combined_metric_keys:
                combined_metric_keys.append(metric_key)

        for metric in primary_overall_metrics:
            _append_metric(metric)
        for metric in extra_metric_keys:
            _append_metric(metric)
        for metric in fail_metric_keys:
            _append_metric(metric)

        # User preference: keep issue_bw_utilization as the last overall column.
        if 'issue_bw_utilization' in combined_metric_keys:
            combined_metric_keys=[m for m in combined_metric_keys if m!='issue_bw_utilization'] + ['issue_bw_utilization']
        overall_header_labels=['study'] + [METRIC_LABELS.get(metric, metric) for metric in combined_metric_keys]

        def ensure_metric_map(entry=None):
            entry=dict(entry) if entry else {}
            for metric in combined_metric_keys:
                entry.setdefault(metric, {'actual': None, 'pct': None})
            return entry

        existing={}

        if base_metrics_ref:
            base_entry=ensure_metric_map()
            for metric in primary_overall_metrics:
                base_entry[metric]={'actual': base_metrics_ref.get(metric), 'pct': None}
            for metric in extra_metric_keys:
                if metric in METRIC_ORDER:
                    continue
                actual_val=(base_extra_metrics_ref or {}).get(metric) if base_extra_metrics_ref else None
                actual_val=coalesce_metric_actual(metric, actual_val)
                base_entry[metric]={'actual': actual_val, 'pct': None}
            for metric_key in fail_metric_keys:
                cause=metric_key.split('fail::',1)[1]
                base_entry[metric_key]={'actual': base_fail_cause_overall.get(cause), 'pct': None}
            existing['base-config']=base_entry

        base_label=variant_labels.get(base_variant, normalize_variant_name(base_variant))
        if base_metrics_ref and base_label!='base-config':
            base_alias_entry=ensure_metric_map()
            for metric in primary_overall_metrics:
                base_alias_entry[metric]={'actual': base_metrics_ref.get(metric), 'pct': 0.0}
            for metric in extra_metric_keys:
                if metric in METRIC_ORDER:
                    continue
                base_value=(base_extra_metrics_ref or {}).get(metric) if base_extra_metrics_ref else None
                base_value=coalesce_metric_actual(metric, base_value)
                base_alias_entry[metric]={
                    'actual': base_value,
                    'pct': 0.0 if base_value is not None else None,
                }
            for metric_key in fail_metric_keys:
                cause=metric_key.split('fail::',1)[1]
                base_value=base_fail_cause_overall.get(cause)
                base_alias_entry[metric_key]={
                    'actual': base_value,
                    'pct': 0.0 if base_value is not None else None,
                }
            existing[base_label]=base_alias_entry

        for entry in overall_entries:
            study_label=entry['label']
            study_entry=ensure_metric_map()
            for metric in primary_overall_metrics:
                study_entry[metric]={
                    'actual': entry['metric_geo_tuned'].get(metric),
                    'pct': entry['metric_geo_pct'].get(metric),
                }
            for metric in extra_metric_keys:
                if metric in METRIC_ORDER:
                    continue
                actual_val=coalesce_metric_actual(metric, entry['extra_metric_geo_tuned'].get(metric))
                study_entry[metric]={
                    'actual': actual_val,
                    'pct': entry['extra_metric_geo_pct'].get(metric),
                }
            if fail_metric_keys:
                fail_summary=fail_cause_overall_entries.get(study_label, {})
                for metric_key in fail_metric_keys:
                    cause=metric_key.split('fail::',1)[1]
                    stats=fail_summary.get(cause, {})
                    study_entry[metric_key]={
                        'actual': stats.get('actual'),
                        'pct': stats.get('pct'),
                    }
            existing[study_label]=study_entry

        order=[]
        if 'base-config' in existing:
            order.append('base-config')
        if base_label!='base-config' and base_label in existing:
            order.append(base_label)
        for variant in compare_variants:
            label=variant_labels.get(variant, variant)
            if label in existing and label not in order:
                order.append(label)

        overall_order=order
        overall_metric_map={study: existing[study] for study in order}

        formatted_overall_rows=[]
        for study in order:
            metric_map=overall_metric_map[study]
            cells=[]
            for metric in combined_metric_keys:
                entry=metric_map[metric]
                include_pct=(study!='base-config' and entry['pct'] is not None)
                cells.append(format_actual_with_pct(entry['actual'], entry['pct'], include_pct))
            formatted_overall_rows.append((study, cells))

        overall_summary_rows=[overall_header_labels] + [[study] + cells for study, cells in formatted_overall_rows]

        import csv as _csv
        with open(args.overall_csv,'w',newline='') as f:
            w=_csv.writer(f)
            w.writerow(overall_header_labels)
            for study, cells in formatted_overall_rows:
                w.writerow([study] + cells)
        print(f"[INFO] updated {args.overall_csv}")

        md2=[
            '# Overall Performance Study',
            '',
            '|study|' + '|'.join(METRIC_LABELS.get(metric, metric) for metric in combined_metric_keys) + '|',
            '|---|' + '|'.join(['---:']*len(combined_metric_keys)) + '|'
        ]
        for study, cells in formatted_overall_rows:
            md2.append(f"|{study}|{'|'.join(cells)}|")
        with open(args.overall_md,'w') as f:
            f.write('\n'.join(md2))
        print(f"[INFO] updated {args.overall_md}")

        try:
            from openpyxl import Workbook as _WB
            from openpyxl.styles import PatternFill as _PF
            wb=_WB(); ws=wb.active; ws.title='Overall'
            ws.append(overall_header_labels)
            for study, cells in formatted_overall_rows:
                ws.append([study] + cells)
            green='FFD4F5D4'; red='FFF8D0D0'; grey='FFF0F0F0'
            for idx, study in enumerate(order, start=2):
                metric_map=overall_metric_map[study]
                for col_offset, metric in enumerate(combined_metric_keys, start=2):
                    entry=metric_map[metric]
                    pct_val=entry['pct']
                    better_is_greater=METRIC_ORIENTATION.get(metric, False)
                    if metric.startswith('fail::'):
                        better_is_greater=False
                    if study=='base-config' or pct_val is None:
                        fill_color=grey
                    elif pct_val==float('inf'):
                        fill_color=green if better_is_greater else red
                    elif pct_val==float('-inf'):
                        fill_color=red if better_is_greater else green
                    elif pct_val>0:
                        fill_color=green if better_is_greater else red
                    elif pct_val<0:
                        fill_color=red if better_is_greater else green
                    else:
                        fill_color=grey
                    ws.cell(row=idx, column=col_offset).fill=_PF(fill_type='solid', fgColor=fill_color)
            wb.save(args.overall_xlsx)
            print(f"[INFO] updated {args.overall_xlsx}")
        except ImportError:
            print('[WARN] openpyxl not installed; skipping overall XLSX output.')

    fail_cause_output=(args.fail_cause_xlsx or '').strip()
    if fail_cause_output:
        fail_cause_path=os.path.expanduser(os.path.expandvars(fail_cause_output))
        metric_keys=('global_acc_r','global_acc_w')
        base_counts={metric: dict(base_fail_causes[metric]) for metric in metric_keys}
        variant_counts_map={
            variant: {metric: dict(variant_fail_causes[variant][metric]) for metric in metric_keys}
            for variant in compare_variants
        }
        base_totals={metric: sum(base_counts[metric].values()) for metric in metric_keys}
        variant_totals={
            variant: {metric: sum(variant_counts_map[variant][metric].values()) for metric in metric_keys}
            for variant in compare_variants
        }
        has_fail_data=any(base_totals[m]>0 for m in metric_keys) or any(
            variant_totals[variant][m]>0 for variant in compare_variants for m in metric_keys
        )
        if not has_fail_data:
            print('[INFO] no fail cause data available; skipping fail cause breakdown XLSX.')
        else:
            try:
                from openpyxl import Workbook as _FailWorkbook
            except ImportError:
                print('[WARN] openpyxl not installed; skipping fail cause breakdown XLSX.')
            else:
                from openpyxl.styles import PatternFill as _FailPatternFill

                wb=_FailWorkbook()
                summary_ws=wb.active
                summary_ws.title='Summary'
                sheet_name_registry.add('Summary')
                row=1
                summary_ws.cell(row,1).value='Fail Cause Breakdown Summary'
                row+=2
                base_label=variant_labels.get(base_variant, normalize_variant_name(base_variant))
                for metric in metric_keys:
                    row=write_fail_table(
                        summary_ws,
                        row,
                        metric,
                        base_counts[metric],
                        base_totals[metric],
                        base_label,
                        base_counts[metric],
                        base_counts[metric],
                    )
                if row>1:
                    row+=1
                for variant in compare_variants:
                    variant_label=variant_labels.get(variant, variant)
                    sheet=wb.create_sheet(unique_sheet_name(variant_label))
                    r=1
                    sheet.cell(r,1).value=f'Variant: {variant_label}'
                    r+=2
                    for metric in metric_keys:
                        r=write_fail_table(
                            sheet,
                            r,
                            metric,
                            base_counts[metric],
                            base_totals[metric],
                            variant_label,
                            variant_counts_map[variant][metric],
                            variant_counts_map[variant][metric],
                        )

                variant_label_order=[]
                seen_variant_labels=set()

                def register_variant_label(label):
                    if not label or label in seen_variant_labels:
                        return
                    seen_variant_labels.add(label)
                    variant_label_order.append(label)

                register_variant_label(base_label)
                for variant in compare_variants:
                    register_variant_label(variant_labels.get(variant, variant))
                for label in ordered_variant_labels:
                    register_variant_label(label)
                for source in (per_kernel_cause_records, per_kernel_driver_records, per_kernel_bank_conflict_records):
                    for label in source.keys():
                        register_variant_label(label)

                access_sort_priority={'GLOBAL_ACC_R': 0, 'GLOBAL_ACC_W': 1}

                cause_sheet=wb.create_sheet(unique_sheet_name('PerKernel-cause-dist'))
                cause_headers=['benchmark','kernel','access_type','cause','fails','pct']
                cause_sheet.append(cause_headers)
                cause_data_written=False
                for label in variant_label_order:
                    records=per_kernel_cause_records.get(label, [])
                    if not records:
                        continue
                    cause_data_written=True
                    cause_sheet.append([])
                    cause_sheet.append(['Variant', label, '', '', '', ''])
                    grouped=defaultdict(list)
                    for rec in records:
                        key=(rec['benchmark'], rec['kernel_index'], rec['kernel'], rec['access_type'])
                        grouped[key].append(rec)
                    for key in sorted(
                        grouped.keys(),
                        key=lambda k: (
                            k[0],
                            k[1],
                            access_sort_priority.get(k[3], 99),
                            k[2],
                        ),
                    ):
                        rows=grouped[key]
                        rows.sort(key=lambda entry: (-entry['pct'], entry['cause']))
                        for entry in rows:
                            cause_sheet.append([
                                entry['benchmark'],
                                entry['kernel'],
                                entry['access_type'],
                                entry['cause'],
                                entry['fails'],
                                round(entry['pct'], 3),
                            ])
                if not cause_data_written:
                    cause_sheet.append(['No per-kernel fail cause data'])

                driver_sheet=wb.create_sheet(unique_sheet_name('PerKernel-driver-dist'))
                driver_headers=['benchmark','kernel','access_type','cause','driver','fails','pct']
                driver_sheet.append(driver_headers)
                driver_data_written=False
                for label in variant_label_order:
                    records=per_kernel_driver_records.get(label, [])
                    if not records:
                        continue
                    driver_data_written=True
                    driver_sheet.append([])
                    driver_sheet.append(['Variant', label, '', '', '', '', ''])
                    grouped=defaultdict(list)
                    for rec in records:
                        key=(rec['benchmark'], rec['kernel_index'], rec['kernel'], rec['access_type'], rec['cause'])
                        grouped[key].append(rec)
                    for key in sorted(
                        grouped.keys(),
                        key=lambda k: (
                            k[0],
                            k[1],
                            access_sort_priority.get(k[3], 99),
                            k[4],
                            k[2],
                        ),
                    ):
                        rows=grouped[key]
                        rows.sort(key=lambda entry: (-entry['pct'], entry['driver']))
                        for entry in rows:
                            driver_sheet.append([
                                entry['benchmark'],
                                entry['kernel'],
                                entry['access_type'],
                                entry['cause'],
                                entry['driver'],
                                entry['fails'],
                                round(entry['pct'], 3),
                            ])
                if not driver_data_written:
                    driver_sheet.append(['No per-kernel driver data'])

                bank_sheet=wb.create_sheet(unique_sheet_name('PerKernel-bank-conflicts'))
                bank_headers=['benchmark','kernel','bank','raw_conflicts_rate','wr_reg_bank_conflicts_rate']
                bank_sheet.append(bank_headers)
                bank_data_written=False
                for label in variant_label_order:
                    records=per_kernel_bank_conflict_records.get(label, [])
                    if not records:
                        continue
                    bank_data_written=True
                    bank_sheet.append([])
                    bank_sheet.append(['Variant', label, '', '', ''])
                    grouped=defaultdict(list)
                    for rec in records:
                        key=(rec['benchmark'], rec['kernel_index'], rec['kernel'])
                        grouped[key].append(rec)
                    for key in sorted(
                        grouped.keys(),
                        key=lambda k: (k[0], k[1], k[2]),
                    ):
                        rows=grouped[key]
                        rows.sort(key=lambda entry: entry['bank'])
                        for entry in rows:
                            bank_sheet.append([
                                entry['benchmark'],
                                entry['kernel'],
                                entry['bank'],
                                round(entry['raw_conflicts_rate'], 6) if entry['raw_conflicts_rate'] is not None else None,
                                round(entry['wr_reg_bank_conflicts_rate'], 6) if entry['wr_reg_bank_conflicts_rate'] is not None else None,
                            ])
                if not bank_data_written:
                    bank_sheet.append(['No per-kernel bank conflict data'])

                kernel_weight_sheet=wb.create_sheet(unique_sheet_name('PerBenchmark-kernel-avg'))
                kernel_weight_headers=['variant','benchmark','access_type','cause','fails','avg_pct','kernel_count','nonzero_kernel_count']
                kernel_weight_sheet.append(kernel_weight_headers)
                kernel_weight_data_written=False
                for label in variant_label_order:
                    records=per_kernel_cause_records.get(label, [])
                    if not records:
                        continue
                    bench_cause_sum=defaultdict(lambda: defaultdict(int))
                    bench_total_fails=defaultdict(int)
                    bench_kernel_set=defaultdict(set)
                    bench_cause_kernel_set=defaultdict(lambda: defaultdict(set))
                    for rec in records:
                        bench=rec['benchmark']
                        cause=rec['cause']
                        fails_val=rec.get('fails') or 0
                        try:
                            fails_int=int(fails_val)
                        except (TypeError, ValueError):
                            continue
                        kernel=rec.get('kernel')
                        bench_total_fails[bench]+=fails_int
                        bench_cause_sum[bench][cause]+=fails_int
                        if kernel:
                            bench_kernel_set[bench].add(kernel)
                            if fails_int>0:
                                bench_cause_kernel_set[bench][cause].add(kernel)
                    variant_rows=[]
                    for bench in sorted(bench_cause_sum.keys()):
                        total_fails=bench_total_fails.get(bench, 0)
                        kernel_count=len(bench_kernel_set[bench])
                        if kernel_count<=0 or total_fails<=0:
                            continue
                        cause_entries=[]
                        for cause, cause_fails in bench_cause_sum[bench].items():
                            if cause_fails<=0:
                                continue
                            avg_pct=(cause_fails/total_fails*100.0) if total_fails else 0.0
                            nonzero=len(bench_cause_kernel_set[bench][cause])
                            cause_entries.append((cause, cause_fails, avg_pct, nonzero))
                        cause_entries.sort(key=lambda item: (-item[1], item[0]))
                        for cause, cause_fails, avg_pct, nonzero in cause_entries:
                            variant_rows.append([
                                label,
                                bench,
                                'ALL',
                                cause,
                                cause_fails,
                                round(avg_pct, 3),
                                kernel_count,
                                nonzero,
                            ])
                    if variant_rows:
                        kernel_weight_data_written=True
                        kernel_weight_sheet.append([])
                        kernel_weight_sheet.append(['Variant', label, '', '', '', '', '', ''])
                        for row in variant_rows:
                            kernel_weight_sheet.append(row)
                if not kernel_weight_data_written:
                    kernel_weight_sheet.append(['No kernel-weighted fail cause data'])

                overall_entry_lookup={entry['label']: entry for entry in overall_entries}

                if (base_metrics_ref or overall_entries or fail_cause_overall_entries):
                    fail_geomean_sheet=wb.create_sheet(unique_sheet_name('Fail-geomean'))
                    cause_headers=list(tracked_fail_causes)
                    geomean_headers=['variant','GLOBAL_ACC_R fails','GLOBAL_ACC_W fails'] + cause_headers
                    fail_geomean_sheet.append(geomean_headers)
                    data_written=False
                    ordered_labels=ordered_variant_labels or variant_label_order

                total_sheet=wb.create_sheet(unique_sheet_name('Fail-total'))

                def _fail_total_header(metric_key: str) -> str:
                    if metric_key=='global_acc_r':
                        return 'GLOBAL_ACC_R total'
                    if metric_key=='global_acc_w':
                        return 'GLOBAL_ACC_W total'
                    label=METRIC_LABELS.get(metric_key, metric_key)
                    if metric_key in METRIC_DEFINITIONS and metric_key not in ('global_acc_r','global_acc_w'):
                        if label.startswith('L2_'):
                            return label
                        return f"{label} geomean"
                    return label

                fail_total_headers=['variant']
                for metric in fail_total_metric_keys:
                    fail_total_headers.append(_fail_total_header(metric))
                fail_total_headers += cause_headers
                total_sheet.append(fail_total_headers)

                def _lookup_total_counts(label: str):
                    if label == base_label:
                        return {
                            'r_counts': base_counts['global_acc_r'],
                            'w_counts': base_counts['global_acc_w'],
                            'r_total': base_totals['global_acc_r'],
                            'w_total': base_totals['global_acc_w'],
                        }
                    for variant in compare_variants:
                        if variant_labels.get(variant, variant) == label:
                            return {
                                'r_counts': variant_counts_map[variant]['global_acc_r'],
                                'w_counts': variant_counts_map[variant]['global_acc_w'],
                                'r_total': variant_totals[variant]['global_acc_r'],
                                'w_total': variant_totals[variant]['global_acc_w'],
                            }
                    agg_r=defaultdict(int)
                    agg_w=defaultdict(int)
                    total_r=0
                    total_w=0
                    for rec in per_kernel_cause_records.get(label, []):
                        cause=rec.get('cause')
                        access_type=rec.get('access_type')
                        fails_val=rec.get('fails')
                        if not cause:
                            continue
                        try:
                            fails_int=int(fails_val)
                        except (TypeError, ValueError):
                            continue
                        if fails_int<=0:
                            continue
                        if access_type=='GLOBAL_ACC_R':
                            agg_r[cause]+=fails_int
                            total_r+=fails_int
                        elif access_type=='GLOBAL_ACC_W':
                            agg_w[cause]+=fails_int
                            total_w+=fails_int
                    return {
                        'r_counts': agg_r,
                        'w_counts': agg_w,
                        'r_total': total_r,
                        'w_total': total_w,
                    }

                base_total_r = base_totals['global_acc_r']
                base_total_w = base_totals['global_acc_w']
                base_extra_values = extra_metric_actual_by_label.get(base_label, {})
                base_cause_totals = {cause: base_counts['global_acc_r'].get(cause, 0) + base_counts['global_acc_w'].get(cause, 0) for cause in cause_headers}

                def _format_total_cell(label: str, value, base_value):
                    def _format_number(val):
                        if val is None:
                            return 'NA'
                        try:
                            f_val=float(val)
                        except (TypeError, ValueError):
                            return str(val)
                        if math.isfinite(f_val) and abs(f_val-round(f_val))<1e-6:
                            return str(int(round(f_val)))
                        return f"{f_val:.3f}"

                    formatted_value=_format_number(value)
                    if label == base_label:
                        return formatted_value, None
                    if value is None or base_value is None:
                        return formatted_value, None
                    try:
                        val_float=float(value) if value is not None else 0.0
                    except (TypeError, ValueError):
                        val_float=0.0
                    try:
                        base_float=float(base_value) if base_value is not None else 0.0
                    except (TypeError, ValueError):
                        base_float=0.0
                    if base_float == 0.0:
                        if val_float == 0.0:
                            pct_val = 0.0
                            pct_str = '(0.00%)'
                        else:
                            pct_val = math.inf
                            pct_str = '(+∞%)'
                    else:
                        pct_val = (val_float - base_float) / base_float * 100.0
                        pct_str = f"({pct_val:+.2f}%)"
                    return f"{formatted_value} {pct_str}", pct_val

                for label in ordered_labels:
                    totals=_lookup_total_counts(label)
                    r_counts=totals['r_counts']
                    w_counts=totals['w_counts']
                    row=[label]
                    fill_specs=[]

                    for metric in fail_total_metric_keys:
                        if metric=='global_acc_r':
                            value=totals['r_total']
                            base_value=base_total_r
                        elif metric=='global_acc_w':
                            value=totals['w_total']
                            base_value=base_total_w
                        else:
                            metric_values=extra_metric_actual_by_label.get(label, {})
                            value=coalesce_metric_actual(metric, metric_values.get(metric))
                            base_value=coalesce_metric_actual(metric, base_extra_values.get(metric))
                        display_val, pct_val=_format_total_cell(label, value, base_value)
                        row.append(display_val)
                        if pct_val is not None:
                            fill_specs.append({'column': len(row), 'pct': pct_val, 'metric': metric})

                    for cause in cause_headers:
                        combined_val = r_counts.get(cause, 0) + w_counts.get(cause, 0)
                        display_cause, pct_cause=_format_total_cell(label, combined_val, base_cause_totals.get(cause, 0))
                        row.append(display_cause)
                        if pct_cause is not None:
                            fill_specs.append({'column': len(row), 'pct': pct_cause, 'metric': f"fail::{cause}"})

                    total_sheet.append(row)
                    current_row=total_sheet.max_row
                    for spec in fill_specs:
                        pct_val=spec['pct']
                        if pct_val is None or pct_val == 0:
                            continue
                        metric_name=spec.get('metric')
                        better_is_greater=False
                        if metric_name:
                            if metric_name in METRIC_ORIENTATION:
                                better_is_greater=METRIC_ORIENTATION[metric_name]
                            elif isinstance(metric_name, str) and metric_name.startswith('fail::'):
                                better_is_greater=False
                        if math.isinf(pct_val):
                            ratio=1.0
                        else:
                            ratio=min(abs(pct_val)/100.0, 1.0)
                        sign_positive=pct_val>0
                        is_improvement=(sign_positive and better_is_greater) or ((not sign_positive) and (not better_is_greater))
                        if is_improvement:
                            start_rgb=(0xE6, 0xF4, 0xE6)
                            end_rgb=(0x63, 0xB8, 0x63)
                        else:
                            start_rgb=(0xF9, 0xE3, 0xE3)
                            end_rgb=(0xD4, 0x5B, 0x5B)
                        blended_r=int(round(start_rgb[0] + (end_rgb[0]-start_rgb[0])*ratio))
                        blended_g=int(round(start_rgb[1] + (end_rgb[1]-start_rgb[1])*ratio))
                        blended_b=int(round(start_rgb[2] + (end_rgb[2]-start_rgb[2])*ratio))
                        color=f"FF{blended_r:02X}{blended_g:02X}{blended_b:02X}"
                        cell=total_sheet.cell(row=current_row, column=spec['column'])
                        cell.fill=_FailPatternFill(fill_type='solid', fgColor=color)


                fail_cause_dir=os.path.dirname(fail_cause_path)
                if fail_cause_dir and not os.path.isdir(fail_cause_dir):
                    os.makedirs(fail_cause_dir, exist_ok=True)
                wb.save(fail_cause_path)
                print(f"[INFO] wrote {fail_cause_path}")

    if args.xlsx_file:
        try:
            from openpyxl import Workbook
            from openpyxl.styles import PatternFill
            from openpyxl.formatting.rule import CellIsRule
            wb=Workbook(); ws=wb.active; ws.title='PerKernel'
            # header extended
            ws.append(csv_header_extended)
            # Use ARGB colors with full opacity for better compatibility
            color_map={'better':'FFD4F5D4','worse':'FFF8D0D0','neutral':'FFF0F0F0'}
            for r in rows_all:
                ws.append(r)
                # apply fill to classified cells (ipc_gain_pct at col5, read_change_pct at col8, write_change_pct at col11)
                last_row=ws.max_row
                ipc_cell=ws.cell(row=last_row,column=6); ipc_cell.fill=PatternFill(fill_type='solid', fgColor=color_map[r[-3]])
                read_cell=ws.cell(row=last_row,column=9); read_cell.fill=PatternFill(fill_type='solid', fgColor=color_map[r[-2]])
                write_cell=ws.cell(row=last_row,column=12); write_cell.fill=PatternFill(fill_type='solid', fgColor=color_map[r[-1]])
            # Add conditional formatting (works in LibreOffice/Excel)
            green_fill=PatternFill(fill_type='solid', fgColor=color_map['better'])
            red_fill=PatternFill(fill_type='solid', fgColor=color_map['worse'])
            # IPC: greaterThan 0 -> green, lessThan 0 -> red
            if ws.max_row >= 2:
                ws.conditional_formatting.add(f"F2:F{ws.max_row}", CellIsRule(operator='greaterThan', formula=['0'], fill=green_fill))
                ws.conditional_formatting.add(f"F2:F{ws.max_row}", CellIsRule(operator='lessThan', formula=['0'], fill=red_fill))
                # READ fails: lessThan 0 -> green, greaterThan 0 -> red
                ws.conditional_formatting.add(f"I2:I{ws.max_row}", CellIsRule(operator='lessThan', formula=['0'], fill=green_fill))
                ws.conditional_formatting.add(f"I2:I{ws.max_row}", CellIsRule(operator='greaterThan', formula=['0'], fill=red_fill))
                # WRITE fails
                ws.conditional_formatting.add(f"L2:L{ws.max_row}", CellIsRule(operator='lessThan', formula=['0'], fill=green_fill))
                ws.conditional_formatting.add(f"L2:L{ws.max_row}", CellIsRule(operator='greaterThan', formula=['0'], fill=red_fill))
            ws2=wb.create_sheet('Averages')
            ws2.append(avg_header)
            for (_, bench, pct_map), avg_row in zip(bench_pct_records_ordered, avg_rows_all):
                ipc_val_num=pct_map.get('ipc')
                read_val_num=pct_map.get('global_acc_r')
                write_val_num=pct_map.get('global_acc_w')
                ws2.append([
                    avg_row[0],
                    bench,
                    value_for_excel(ipc_val_num),
                    value_for_excel(read_val_num),
                    value_for_excel(write_val_num)
                ])
                lr=ws2.max_row
                ipc_c=classify_change(ipc_val_num,'ipc')
                read_c=classify_change(read_val_num,'global_acc_r')
                write_c=classify_change(write_val_num,'global_acc_w')
                ws2.cell(row=lr,column=3).fill=PatternFill(fill_type='solid', fgColor=color_map[ipc_c])
                ws2.cell(row=lr,column=4).fill=PatternFill(fill_type='solid', fgColor=color_map[read_c])
                ws2.cell(row=lr,column=5).fill=PatternFill(fill_type='solid', fgColor=color_map[write_c])
            avg_section_last_row = ws2.max_row
            if overall_summary_rows:
                ws2.append([])
                summary_header_row = ws2.max_row + 1
                if overall_summary_rows:
                    copied_styles=False
                    try:
                        from openpyxl import load_workbook as _load_wb
                        overall_wb=_load_wb(args.overall_xlsx)
                        overall_ws=overall_wb['Overall']
                        for row in overall_ws.iter_rows(values_only=False):
                            values=[cell.value for cell in row[:len(overall_header_labels)]]
                            ws2.append(values)
                            dest_row=ws2.max_row
                            for col_idx, src_cell in enumerate(row[:len(overall_header_labels)], start=1):
                                ws2.cell(row=dest_row, column=col_idx).fill=copy(src_cell.fill)
                        copied_styles=True
                    except Exception as exc:
                        print(f"[WARN] unable to copy overall XLSX formatting into perf_gain.xlsx: {exc}")
                    if not copied_styles:
                        for row in overall_summary_rows:
                            ws2.append(row)
                ws2.conditional_formatting.add(f"C2:C{avg_section_last_row}", CellIsRule(operator='greaterThan', formula=['0'], fill=green_fill))
                ws2.conditional_formatting.add(f"C2:C{avg_section_last_row}", CellIsRule(operator='lessThan', formula=['0'], fill=red_fill))
                ws2.conditional_formatting.add(f"D2:D{avg_section_last_row}", CellIsRule(operator='lessThan', formula=['0'], fill=green_fill))
                ws2.conditional_formatting.add(f"D2:D{avg_section_last_row}", CellIsRule(operator='greaterThan', formula=['0'], fill=red_fill))
                ws2.conditional_formatting.add(f"E2:E{avg_section_last_row}", CellIsRule(operator='lessThan', formula=['0'], fill=green_fill))
                ws2.conditional_formatting.add(f"E2:E{avg_section_last_row}", CellIsRule(operator='greaterThan', formula=['0'], fill=red_fill))
            wb.save(args.xlsx_file)
            print(f"[INFO] wrote {args.xlsx_file}")
        except ImportError:
            print('[WARN] openpyxl not installed; skipping XLSX output.')

if __name__=='__main__':
    main()
