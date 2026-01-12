mkdir -p ./no_mshr_dumps
cp trace.out ./no_mshr_dumps/
cd ./no_mshr_dumps/
grep 'm_lfb' trace.out | grep -E 'L2' > l2_refill_queue_add
grep 'l2_dram_queue added' trace.out > l2_dram_queue_added

for ((sub=0; sub<8; sub++)); do
  grep "L2_sub\[$sub\]" l2_refill_queue_add > l2_sub_${sub}_refill_queue_add
  awk '{print $NF}' l2_sub_${sub}_refill_queue_add > l2_sub_${sub}_refill_queue_add_addresses
  echo "Generated L2_sub[${sub}]_refill_queue_add_addresses"

  grep "L2_sub\[$sub\]" l2_dram_queue_added > l2_sub_${sub}_dram_queue_added
  awk '{print $NF}' l2_sub_${sub}_dram_queue_added > l2_sub_${sub}_dram_queue_added_addresses
  echo "Generated L2_sub[${sub}]_dram_queue_added_addresses"  
done
cd ../