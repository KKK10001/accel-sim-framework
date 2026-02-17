grep 'warp_interfere\[' perf_rpt_warp_interfere_awared_cache_replace.o > warp_interfere_appearances_tune
awk '{sum += $NF} END {print sum}' warp_interfere_appearances_tune > sum_warp_interfere_appearances_tune

grep 'warp_interfere\[' perf_rpt_warp_schedule_base.o > warp_interfere_appearances_base
awk '{sum1 += $NF} END {print sum1}' warp_interfere_appearances_base > sum_warp_interfere_appearances_base

vimdiff sum_warp_interfere_appearances_tune sum_warp_interfere_appearances_base
