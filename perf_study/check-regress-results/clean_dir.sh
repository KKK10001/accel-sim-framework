sim_root=/home/hjs/dev/accel-sim/accel-sim-framework/sim_run_12.1
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

regress_tag=perf-study-mshr-max-merge-32 # removed
# regress_tag=perf-study-miss-q-entries-32

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
