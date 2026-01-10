grep 'TPC:0 SM:0 WARP:3 req_uid:989 addr:0xfffdc000000000' trace.out > first_miss_flow
grep 'into MSHR' trace.out | grep -E 'L2' > l2_mshr_hit
grep 'L2 traffic blocked' trace.out > l2_traffic_blocked
grep 'L2 fill responses L2_sub' trace.out > l2_fill_resp
grep 'pushed into m_rop' trace.out > m_rop_push
grep 'm_rop.pop' trace.out > m_rop_pop
grep 'current cycle is' trace.out > curr_cycle
grep 'dram_cycle' trace.out > dram_cycle

grep 'mshr_resp_q added' trace.out | grep -E 'L2' > l2_refill_mshr
grep 'mshr_resp_q popped' trace.out | grep -E 'L2' > l2_release_mshr

# Compare refill and release MSHR addresses for each L2 sub-partition (particular example)
# grep 'L2_sub\[7\]' l2_refill_mshr > l2_sub_7_refill_mshr
# grep 'L2_sub\[7\]' l2_release_mshr > l2_sub_7_release_mshr
# awk '{print $5}' l2_sub_7_refill_mshr > l2_sub_7_refill_mshr_addresses
# awk '{print $5}' l2_sub_7_release_mshr > l2_sub_7_release_mshr_addresses
# awk '{print $1}' l2_sub_7_refill_mshr > l2_sub_7_refill_mshr_cycles
# awk '{print $1}' l2_sub_7_release_mshr > l2_sub_7_release_mshr_cycles
# vimdiff l2_sub_7_refill_mshr_cycles l2_sub_7_release_mshr_cycles

# Compare refill and release MSHR addresses for each L2 sub-partition
for ((sub=0; sub<8; sub++)); do
  grep "L2_sub\[$sub\]" l2_refill_mshr > l2_sub_${sub}_refill_mshr
  grep "L2_sub\[$sub\]" l2_release_mshr > l2_sub_${sub}_release_mshr
  awk '{print $NF}' l2_sub_${sub}_refill_mshr > l2_sub_${sub}_refill_mshr_addresses
  awk '{print $NF}' l2_sub_${sub}_release_mshr > l2_sub_${sub}_release_mshr_addresses
  if diff -q l2_sub_${sub}_refill_mshr_addresses l2_sub_${sub}_release_mshr_addresses; then
    echo "L2_sub[${sub}] refill and release MSHR addresses match."
  else
    echo "L2_sub[${sub}] refill and release MSHR addresses DO NOT match!"
  fi
done
echo "--------------------------- Verified MSHR refill/release addresses ---------------------------"
echo 

grep 'm_L2_icnt_queue' trace.out > l2_icnt_queue_add
# grep 'm_L2_icnt_queue_all_req_types' trace.out > l2_icnt_queue_add
for ((sub=0; sub<8; sub++)); do
  grep "L2_sub\[$sub\]" l2_icnt_queue_add > l2_sub_${sub}_icnt_queue_add
  awk '{print $(NF-1)}' l2_sub_${sub}_icnt_queue_add > l2_sub_${sub}_icnt_queue_add_addresses
  if diff -q l2_sub_${sub}_icnt_queue_add_addresses l2_sub_${sub}_release_mshr_addresses; then
    echo "L2_sub[${sub}] release_mshr_addresses and icnt_queue_add_addresses match."
  else
    if [ $sub -eq 0 ]; then
      icnt_q_lines=$(wc -l < l2_sub_${sub}_icnt_queue_add_addresses)
      release_mshr_lines=$(wc -l < l2_sub_${sub}_release_mshr_addresses)
      if [ $icnt_q_lines -ne $release_mshr_lines ]; then
        echo "L2_sub[${sub}] icnt_queue_add has ${icnt_q_lines} lines, release_mshr has ${release_mshr_lines} lines."
        echo "Skipping vimdiff due to line count mismatch."
        vimdiff l2_sub_${sub}_release_mshr_addresses l2_sub_${sub}_icnt_queue_add_addresses
      fi
    fi
    echo "L2_sub[${sub}] release_mshr_addresses and icnt_queue_add_addresses DO NOT match!"
  fi
done

