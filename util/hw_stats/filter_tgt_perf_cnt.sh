ncu --query-metrics --chip ga106 > GTX_3060_avail_perf_cnt
grep 'issue' GTX_3060_avail_perf_cnt > GTX_3060_issue_perf_cnt
grep 'issue_stalled' GTX_3060_avail_perf_cnt > GTX_3060_issue_stalled_perf_cnt
grep 'microscheduler' GTX_3060_avail_perf_cnt > GTX_3060_microscheduler_perf_cnt
grep 'register file' GTX_3060_avail_perf_cnt > GTX_3060_crf_perf_cnt
