# Overall Performance Study

|study|IPC|L2_BW|L2_total_cache_accesses|L2_GLOBAL_ACC_W_TOTAL_ACCESS|MISS_QUEUE_FULL|MSHR_MERGE_ENTRY_FAIL|MSHR_ENTRY_FAIL|LINE_ALLOC_FAIL|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|base-config|29.871|5.756|12066.066|0.000|13170.246|0.000|0.000|0.864|
|regress_disable_mshr_l2_correlation|29.871 (+0.000%)|5.756 (+0.000%)|12066.066 (+0.000%)|0.000 (+0.000%)|13170.246 (+0.000%)|0.000 (+0.000%)|0.000 (+0.000%)|0.864 (+0.000%)|
|regress_enable_mshr_l2_correlation|34.293 (+14.801%)|4.628 (-19.594%)|8536.831 (-29.249%)|0.000|3577.276 (-72.838%)|146.261 (+inf%)|7.180 (+inf%)|1.647 (+90.605%)|