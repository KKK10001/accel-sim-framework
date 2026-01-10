# Overall Performance Study

|study|IPC|L2_BW|L2_total_cache_accesses|L2_GLOBAL_ACC_W_TOTAL_ACCESS|MISS_QUEUE_FULL|MSHR_MERGE_ENTRY_FAIL|MSHR_ENTRY_FAIL|LINE_ALLOC_FAIL|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|base-config|29.887|5.759|12066.076|0.000|13170.213|0.000|0.000|0.864|
|regress_disable_all_mshr|29.887 (+0.000%)|5.759 (+0.000%)|12066.076 (+0.000%)|0.000 (+0.000%)|13170.213 (+0.000%)|0.000 (+0.000%)|0.000 (+0.000%)|0.864 (+0.000%)|
|regress_enable_all_mshr|34.294 (+14.746%)|4.628 (-19.632%)|8536.831 (-29.249%)|0.000|3578.080 (-72.832%)|146.266 (+inf%)|7.106 (+inf%)|1.647 (+90.605%)|