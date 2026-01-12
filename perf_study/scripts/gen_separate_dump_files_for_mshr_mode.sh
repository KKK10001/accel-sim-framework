mkdir -p ./mshr_dumps
cp trace.out ./mshr_dumps/
cd ./mshr_dumps/
grep 'mshr_resp_q added' trace.out | grep -E 'L2' > l2_refill_mshr
grep 'mshr_resp_q popped' trace.out | grep -E 'L2' > l2_release_mshr
grep 'l2_dram_queue added' trace.out > l2_dram_queue_added

for ((sub=0; sub<8; sub++)); do
  grep "L2_sub\[$sub\]" l2_refill_mshr > l2_sub_${sub}_refill_mshr
  awk '{print $NF}' l2_sub_${sub}_refill_mshr > l2_sub_${sub}_refill_mshr_addresses
  echo "Generated L2_sub[${sub}]_refill_mshr_addresses"

  grep "L2_sub\[$sub\]" l2_release_mshr > l2_sub_${sub}_release_mshr
  awk '{print $NF}' l2_sub_${sub}_release_mshr > l2_sub_${sub}_release_mshr_addresses
  echo "Generated L2_sub[${sub}]_release_mshr_addresses"  

  grep "L2_sub\[$sub\]" l2_dram_queue_added > l2_sub_${sub}_dram_queue_added
  awk '{print $NF}' l2_sub_${sub}_dram_queue_added > l2_sub_${sub}_dram_queue_added_addresses
  echo "Generated L2_sub[${sub}]_dram_queue_added_addresses"    
done
cd ../