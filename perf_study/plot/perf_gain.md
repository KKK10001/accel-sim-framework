# Performance Gain Report

## Per-Kernel Details (colored)

|variant|benchmark|kernel_index|ipc_base|ipc_tuned|ipc_gain_pct|read_base|read_tuned|read_change_pct|write_base|write_tuned|write_change_pct|
|---|---|---|---|---|---|---|---|---|---|---|---|
|l2_max_merge_zero|backprop-rodinia-2.0-ft|1|834.9478|827.7923|<span style='background-color:#f8d0d0'>-0.857</span>|42836|42852|<span style='background-color:#f8d0d0'>0.037</span>|6884|6037|<span style='background-color:#d4f5d4'>-12.304</span>|
|l2_max_merge_zero|backprop-rodinia-2.0-ft|2|371.7225|372.066|<span style='background-color:#d4f5d4'>0.092</span>|179145|205317|<span style='background-color:#f8d0d0'>14.609</span>|9739|8472|<span style='background-color:#d4f5d4'>-13.010</span>|
|l2_max_merge_zero|bfs-rodinia-2.0-ft|1|3.691|3.691|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|bfs-rodinia-2.0-ft|2|7.9852|7.9852|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|bfs-rodinia-2.0-ft|3|3.9985|3.9985|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|bfs-rodinia-2.0-ft|4|8.286|8.286|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|bfs-rodinia-2.0-ft|5|4.8361|4.8361|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|bfs-rodinia-2.0-ft|6|8.8546|8.8546|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|bfs-rodinia-2.0-ft|7|9.0819|9.1028|<span style='background-color:#d4f5d4'>0.230</span>|71|71|0.000|0|0|0.000|
|l2_max_merge_zero|bfs-rodinia-2.0-ft|8|11.5803|11.5803|0.000|71|71|0.000|0|0|0.000|
|l2_max_merge_zero|bfs-rodinia-2.0-ft|9|21.4818|21.3886|<span style='background-color:#f8d0d0'>-0.434</span>|2399|2396|<span style='background-color:#d4f5d4'>-0.125</span>|111|180|<span style='background-color:#f8d0d0'>62.162</span>|
|l2_max_merge_zero|bfs-rodinia-2.0-ft|10|12.8834|12.8834|0.000|2399|2396|<span style='background-color:#d4f5d4'>-0.125</span>|111|180|<span style='background-color:#f8d0d0'>62.162</span>|
|l2_max_merge_zero|bfs-rodinia-2.0-ft|11|24.0576|24.0218|<span style='background-color:#f8d0d0'>-0.149</span>|4883|4880|<span style='background-color:#d4f5d4'>-0.061</span>|111|180|<span style='background-color:#f8d0d0'>62.162</span>|
|l2_max_merge_zero|bfs-rodinia-2.0-ft|12|8.6567|8.6567|0.000|4883|4880|<span style='background-color:#d4f5d4'>-0.061</span>|111|180|<span style='background-color:#f8d0d0'>62.162</span>|
|l2_max_merge_zero|bfs-rodinia-2.0-ft|13|6.9936|6.9936|0.000|4891|4888|<span style='background-color:#d4f5d4'>-0.061</span>|111|180|<span style='background-color:#f8d0d0'>62.162</span>|
|l2_max_merge_zero|bfs-rodinia-2.0-ft|14|8.1941|8.1941|0.000|4891|4888|<span style='background-color:#d4f5d4'>-0.061</span>|111|180|<span style='background-color:#f8d0d0'>62.162</span>|
|l2_max_merge_zero|bfs-rodinia-2.0-ft|15|6.5952|6.5962|<span style='background-color:#d4f5d4'>0.015</span>|4891|4888|<span style='background-color:#d4f5d4'>-0.061</span>|111|180|<span style='background-color:#f8d0d0'>62.162</span>|
|l2_max_merge_zero|bfs-rodinia-2.0-ft|16|8.5236|8.5236|0.000|4891|4888|<span style='background-color:#d4f5d4'>-0.061</span>|111|180|<span style='background-color:#f8d0d0'>62.162</span>|
|l2_max_merge_zero|heartwall-rodinia-2.0-ft|1|763.9442|718.8986|<span style='background-color:#f8d0d0'>-5.896</span>|17376|29381|<span style='background-color:#f8d0d0'>69.090</span>|68|337|<span style='background-color:#f8d0d0'>395.588</span>|
|l2_max_merge_zero|hotspot-rodinia-2.0-ft|1|596.4451|578.6663|<span style='background-color:#f8d0d0'>-2.981</span>|3307|3307|0.000|0|0|0.000|
|l2_max_merge_zero|hotspot-rodinia-2.0-ft|2|601.9191|574.284|<span style='background-color:#f8d0d0'>-4.591</span>|7159|7121|<span style='background-color:#d4f5d4'>-0.531</span>|0|0|0.000|
|l2_max_merge_zero|hotspot-rodinia-2.0-ft|3|618.4879|618.8033|<span style='background-color:#d4f5d4'>0.051</span>|11093|11064|<span style='background-color:#d4f5d4'>-0.261</span>|0|0|0.000|
|l2_max_merge_zero|hotspot-rodinia-2.0-ft|4|619.7515|619.6724|<span style='background-color:#f8d0d0'>-0.013</span>|15017|14949|<span style='background-color:#d4f5d4'>-0.453</span>|0|0|0.000|
|l2_max_merge_zero|hotspot-rodinia-2.0-ft|5|618.6455|619.198|<span style='background-color:#d4f5d4'>0.089</span>|18931|18853|<span style='background-color:#d4f5d4'>-0.412</span>|0|0|0.000|
|l2_max_merge_zero|hotspot-rodinia-2.0-ft|6|619.9099|618.409|<span style='background-color:#f8d0d0'>-0.242</span>|22865|22719|<span style='background-color:#d4f5d4'>-0.639</span>|0|0|0.000|
|l2_max_merge_zero|hotspot-rodinia-2.0-ft|7|494.2744|494.4827|<span style='background-color:#d4f5d4'>0.042</span>|23828|23698|<span style='background-color:#d4f5d4'>-0.546</span>|0|0|0.000|
|l2_max_merge_zero|lud-rodinia-2.0-ft|1|0.7762|0.7762|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|lud-rodinia-2.0-ft|2|4.9649|4.9649|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|lud-rodinia-2.0-ft|3|26.7007|26.7007|0.000|242|242|0.000|0|0|0.000|
|l2_max_merge_zero|lud-rodinia-2.0-ft|4|0.7811|0.7811|0.000|242|242|0.000|0|0|0.000|
|l2_max_merge_zero|lud-rodinia-2.0-ft|5|3.3975|3.3975|0.000|242|242|0.000|0|0|0.000|
|l2_max_merge_zero|lud-rodinia-2.0-ft|6|12.1465|12.1465|0.000|327|327|0.000|0|0|0.000|
|l2_max_merge_zero|lud-rodinia-2.0-ft|7|0.7811|0.7811|0.000|327|327|0.000|0|0|0.000|
|l2_max_merge_zero|lud-rodinia-2.0-ft|8|1.6993|1.6993|0.000|327|327|0.000|0|0|0.000|
|l2_max_merge_zero|lud-rodinia-2.0-ft|9|3.045|3.045|0.000|360|360|0.000|0|0|0.000|
|l2_max_merge_zero|lud-rodinia-2.0-ft|10|0.7811|0.7811|0.000|360|360|0.000|0|0|0.000|
|l2_max_merge_zero|nn-rodinia-2.0-ft|1|217.5636|217.5636|0.000|12699|12699|0.000|0|0|0.000|
|l2_max_merge_zero|nn-rodinia-2.0-ft|2|227.4201|227.4201|0.000|23765|23765|0.000|0|0|0.000|
|l2_max_merge_zero|nn-rodinia-2.0-ft|3|227.2331|227.2331|0.000|35209|35209|0.000|0|0|0.000|
|l2_max_merge_zero|nn-rodinia-2.0-ft|4|227.5499|227.5499|0.000|46202|46202|0.000|0|0|0.000|
|l2_max_merge_zero|nw-rodinia-2.0-ft|1|0.9613|0.9613|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|nw-rodinia-2.0-ft|2|1.9271|1.9271|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|nw-rodinia-2.0-ft|3|2.8869|2.8869|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|nw-rodinia-2.0-ft|4|3.8546|3.8546|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|nw-rodinia-2.0-ft|5|4.8172|4.8172|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|nw-rodinia-2.0-ft|6|5.7819|5.7819|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|nw-rodinia-2.0-ft|7|6.7426|6.7426|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|nw-rodinia-2.0-ft|8|7.705|7.705|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|nw-rodinia-2.0-ft|9|6.844|6.844|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|nw-rodinia-2.0-ft|10|5.8682|5.8682|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|nw-rodinia-2.0-ft|11|4.8901|4.8901|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|nw-rodinia-2.0-ft|12|3.9138|3.9138|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|nw-rodinia-2.0-ft|13|2.936|2.936|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|nw-rodinia-2.0-ft|14|1.9567|1.9567|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|nw-rodinia-2.0-ft|15|0.9787|0.9787|0.000|0|0|0.000|0|0|0.000|
|l2_max_merge_zero|pathfinder-rodinia-2.0-ft|1|32.268|31.6461|<span style='background-color:#f8d0d0'>-1.927</span>|247|240|<span style='background-color:#d4f5d4'>-2.834</span>|81|81|0.000|
|l2_max_merge_zero|pathfinder-rodinia-2.0-ft|2|32.9355|32.2043|<span style='background-color:#f8d0d0'>-2.220</span>|489|472|<span style='background-color:#d4f5d4'>-3.476</span>|165|165|0.000|
|l2_max_merge_zero|pathfinder-rodinia-2.0-ft|3|32.9272|31.696|<span style='background-color:#f8d0d0'>-3.739</span>|736|697|<span style='background-color:#d4f5d4'>-5.299</span>|249|248|<span style='background-color:#d4f5d4'>-0.402</span>|
|l2_max_merge_zero|pathfinder-rodinia-2.0-ft|4|29.1348|28.4678|<span style='background-color:#f8d0d0'>-2.289</span>|924|883|<span style='background-color:#d4f5d4'>-4.437</span>|339|338|<span style='background-color:#d4f5d4'>-0.295</span>|
|l2_max_merge_zero|srad_v2-rodinia-2.0-ft|1|475.8292|475.8292|0.000|78|78|0.000|4160|4160|0.000|
|l2_max_merge_zero|srad_v2-rodinia-2.0-ft|2|187.5066|187.5066|0.000|2995|2995|0.000|4224|4224|0.000|
|l2_max_merge_zero|srad_v2-rodinia-2.0-ft|3|473.5039|473.5039|0.000|3068|3068|0.000|8384|8384|0.000|
|l2_max_merge_zero|srad_v2-rodinia-2.0-ft|4|188.5967|188.5967|0.000|5953|5953|0.000|8448|8448|0.000|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|1|16.2309|16.0442|<span style='background-color:#f8d0d0'>-1.150</span>|4761|4851|<span style='background-color:#f8d0d0'>1.890</span>|434|413|<span style='background-color:#d4f5d4'>-4.839</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|2|17.2089|17.2108|<span style='background-color:#d4f5d4'>0.011</span>|8788|8879|<span style='background-color:#f8d0d0'>1.036</span>|475|458|<span style='background-color:#d4f5d4'>-3.579</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|3|17.3245|17.3283|<span style='background-color:#d4f5d4'>0.022</span>|12733|12796|<span style='background-color:#f8d0d0'>0.495</span>|476|460|<span style='background-color:#d4f5d4'>-3.361</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|4|17.3478|17.3458|<span style='background-color:#f8d0d0'>-0.012</span>|16757|16772|<span style='background-color:#f8d0d0'>0.090</span>|556|502|<span style='background-color:#d4f5d4'>-9.712</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|5|17.3478|17.3419|<span style='background-color:#f8d0d0'>-0.034</span>|20774|20800|<span style='background-color:#f8d0d0'>0.125</span>|623|562|<span style='background-color:#d4f5d4'>-9.791</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|6|17.5802|17.5802|0.000|24747|24773|<span style='background-color:#f8d0d0'>0.105</span>|629|568|<span style='background-color:#d4f5d4'>-9.698</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|7|17.5942|17.5942|0.000|28787|28813|<span style='background-color:#f8d0d0'>0.090</span>|719|658|<span style='background-color:#d4f5d4'>-8.484</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|8|17.5762|17.5762|0.000|32911|32937|<span style='background-color:#f8d0d0'>0.079</span>|864|803|<span style='background-color:#d4f5d4'>-7.060</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|9|17.6142|17.6142|0.000|36955|36981|<span style='background-color:#f8d0d0'>0.070</span>|889|828|<span style='background-color:#d4f5d4'>-6.862</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|10|17.5862|17.5862|0.000|40973|40999|<span style='background-color:#f8d0d0'>0.063</span>|955|894|<span style='background-color:#d4f5d4'>-6.387</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|11|17.5802|17.5802|0.000|44946|44972|<span style='background-color:#f8d0d0'>0.058</span>|961|900|<span style='background-color:#d4f5d4'>-6.348</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|12|17.5942|17.5942|0.000|48986|49012|<span style='background-color:#f8d0d0'>0.053</span>|1051|990|<span style='background-color:#d4f5d4'>-5.804</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|13|17.5762|17.5762|0.000|53110|53136|<span style='background-color:#f8d0d0'>0.049</span>|1196|1135|<span style='background-color:#d4f5d4'>-5.100</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|14|17.6142|17.6142|0.000|57154|57180|<span style='background-color:#f8d0d0'>0.045</span>|1221|1160|<span style='background-color:#d4f5d4'>-4.996</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|15|17.5862|17.5862|0.000|61172|61198|<span style='background-color:#f8d0d0'>0.043</span>|1287|1226|<span style='background-color:#d4f5d4'>-4.740</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|16|17.6002|17.6002|0.000|65195|65221|<span style='background-color:#f8d0d0'>0.040</span>|1359|1298|<span style='background-color:#d4f5d4'>-4.489</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|17|17.5802|17.5802|0.000|69168|69194|<span style='background-color:#f8d0d0'>0.038</span>|1365|1304|<span style='background-color:#d4f5d4'>-4.469</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|18|17.5942|17.5942|0.000|73208|73234|<span style='background-color:#f8d0d0'>0.036</span>|1455|1394|<span style='background-color:#d4f5d4'>-4.192</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|19|17.5762|17.5762|0.000|77332|77358|<span style='background-color:#f8d0d0'>0.034</span>|1600|1539|<span style='background-color:#d4f5d4'>-3.812</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|20|17.6142|17.6142|0.000|81376|81402|<span style='background-color:#f8d0d0'>0.032</span>|1625|1564|<span style='background-color:#d4f5d4'>-3.754</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|21|17.5762|17.5762|0.000|85500|85526|<span style='background-color:#f8d0d0'>0.030</span>|1770|1709|<span style='background-color:#d4f5d4'>-3.446</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|22|17.5942|17.5942|0.000|89540|89566|<span style='background-color:#f8d0d0'>0.029</span>|1860|1799|<span style='background-color:#d4f5d4'>-3.280</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|23|17.6142|17.6142|0.000|93584|93610|<span style='background-color:#f8d0d0'>0.028</span>|1885|1824|<span style='background-color:#d4f5d4'>-3.236</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|24|17.5762|17.5762|0.000|97708|97734|<span style='background-color:#f8d0d0'>0.027</span>|2030|1969|<span style='background-color:#d4f5d4'>-3.005</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|25|17.5942|17.5942|0.000|101748|101774|<span style='background-color:#f8d0d0'>0.026</span>|2120|2059|<span style='background-color:#d4f5d4'>-2.877</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|26|17.6142|17.6142|0.000|105792|105818|<span style='background-color:#f8d0d0'>0.025</span>|2145|2084|<span style='background-color:#d4f5d4'>-2.844</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|27|17.5762|17.5762|0.000|109916|109942|<span style='background-color:#f8d0d0'>0.024</span>|2290|2229|<span style='background-color:#d4f5d4'>-2.664</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|28|17.5942|17.5942|0.000|113956|113982|<span style='background-color:#f8d0d0'>0.023</span>|2380|2319|<span style='background-color:#d4f5d4'>-2.563</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|29|17.6142|17.6142|0.000|118000|118026|<span style='background-color:#f8d0d0'>0.022</span>|2405|2344|<span style='background-color:#d4f5d4'>-2.536</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|30|17.5762|17.5762|0.000|122124|122150|<span style='background-color:#f8d0d0'>0.021</span>|2550|2489|<span style='background-color:#d4f5d4'>-2.392</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|31|17.6002|17.6002|0.000|126147|126173|<span style='background-color:#f8d0d0'>0.021</span>|2622|2561|<span style='background-color:#d4f5d4'>-2.326</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|32|17.5802|17.5802|0.000|130120|130146|<span style='background-color:#f8d0d0'>0.020</span>|2628|2567|<span style='background-color:#d4f5d4'>-2.321</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|33|17.5942|17.5942|0.000|134160|134186|<span style='background-color:#f8d0d0'>0.019</span>|2718|2657|<span style='background-color:#d4f5d4'>-2.244</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|34|17.5762|17.5762|0.000|138284|138310|<span style='background-color:#f8d0d0'>0.019</span>|2863|2802|<span style='background-color:#d4f5d4'>-2.131</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|35|17.6142|17.6142|0.000|142328|142354|<span style='background-color:#f8d0d0'>0.018</span>|2888|2827|<span style='background-color:#d4f5d4'>-2.112</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|36|17.5862|17.5862|0.000|146346|146372|<span style='background-color:#f8d0d0'>0.018</span>|2954|2893|<span style='background-color:#d4f5d4'>-2.065</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|37|17.6002|17.6002|0.000|150369|150395|<span style='background-color:#f8d0d0'>0.017</span>|3026|2965|<span style='background-color:#d4f5d4'>-2.016</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|38|17.5802|17.5802|0.000|154342|154368|<span style='background-color:#f8d0d0'>0.017</span>|3032|2971|<span style='background-color:#d4f5d4'>-2.012</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|39|17.5942|17.5942|0.000|158382|158408|<span style='background-color:#f8d0d0'>0.016</span>|3122|3061|<span style='background-color:#d4f5d4'>-1.954</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|40|17.5762|17.5762|0.000|162506|162532|<span style='background-color:#f8d0d0'>0.016</span>|3267|3206|<span style='background-color:#d4f5d4'>-1.867</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|41|17.6665|17.5842|<span style='background-color:#f8d0d0'>-0.466</span>|166616|166635|<span style='background-color:#f8d0d0'>0.011</span>|3334|3228|<span style='background-color:#d4f5d4'>-3.179</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|42|17.5802|17.5982|<span style='background-color:#d4f5d4'>0.102</span>|170581|170662|<span style='background-color:#f8d0d0'>0.047</span>|3442|3367|<span style='background-color:#d4f5d4'>-2.179</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|43|17.5484|17.5523|<span style='background-color:#d4f5d4'>0.022</span>|174596|174878|<span style='background-color:#f8d0d0'>0.162</span>|3449|3515|<span style='background-color:#f8d0d0'>1.914</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|44|17.6263|17.5962|<span style='background-color:#f8d0d0'>-0.171</span>|178734|178971|<span style='background-color:#f8d0d0'>0.133</span>|3530|3591|<span style='background-color:#f8d0d0'>1.728</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|45|17.5862|17.6263|<span style='background-color:#d4f5d4'>0.228</span>|182894|182942|<span style='background-color:#f8d0d0'>0.026</span>|3734|3717|<span style='background-color:#d4f5d4'>-0.455</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|46|17.5802|17.5802|0.000|186910|186958|<span style='background-color:#f8d0d0'>0.026</span>|3791|3774|<span style='background-color:#d4f5d4'>-0.448</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|47|17.5962|17.5962|0.000|190987|191035|<span style='background-color:#f8d0d0'>0.025</span>|3870|3853|<span style='background-color:#d4f5d4'>-0.439</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|48|17.5962|17.5962|0.000|195018|195066|<span style='background-color:#f8d0d0'>0.025</span>|4033|4016|<span style='background-color:#d4f5d4'>-0.422</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|49|17.6042|17.6042|0.000|198860|198908|<span style='background-color:#f8d0d0'>0.024</span>|4033|4016|<span style='background-color:#d4f5d4'>-0.422</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|50|17.6183|17.6183|0.000|202855|202903|<span style='background-color:#f8d0d0'>0.024</span>|4127|4110|<span style='background-color:#d4f5d4'>-0.412</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|51|17.3439|17.3439|0.000|207061|207109|<span style='background-color:#f8d0d0'>0.023</span>|4287|4270|<span style='background-color:#d4f5d4'>-0.397</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|52|17.5782|17.5782|0.000|211100|211148|<span style='background-color:#f8d0d0'>0.023</span>|4363|4346|<span style='background-color:#d4f5d4'>-0.390</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|53|17.5683|17.5683|0.000|215198|215246|<span style='background-color:#f8d0d0'>0.022</span>|4406|4389|<span style='background-color:#d4f5d4'>-0.386</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|54|17.5982|17.5982|0.000|219208|219256|<span style='background-color:#f8d0d0'>0.022</span>|4595|4578|<span style='background-color:#d4f5d4'>-0.370</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|55|17.5523|17.5523|0.000|223336|223384|<span style='background-color:#f8d0d0'>0.021</span>|4772|4755|<span style='background-color:#d4f5d4'>-0.356</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|56|17.6504|17.6504|0.000|227298|227346|<span style='background-color:#f8d0d0'>0.021</span>|4790|4773|<span style='background-color:#d4f5d4'>-0.355</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|57|17.3439|17.3439|0.000|231504|231552|<span style='background-color:#f8d0d0'>0.021</span>|4950|4933|<span style='background-color:#d4f5d4'>-0.343</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|58|17.5782|17.5782|0.000|235543|235591|<span style='background-color:#f8d0d0'>0.020</span>|5026|5009|<span style='background-color:#d4f5d4'>-0.338</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|59|17.5683|17.5683|0.000|239641|239689|<span style='background-color:#f8d0d0'>0.020</span>|5069|5052|<span style='background-color:#d4f5d4'>-0.335</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|60|17.5982|17.5982|0.000|243651|243699|<span style='background-color:#f8d0d0'>0.020</span>|5258|5241|<span style='background-color:#d4f5d4'>-0.323</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|61|17.6082|17.6082|0.000|247641|247689|<span style='background-color:#f8d0d0'>0.019</span>|5265|5248|<span style='background-color:#d4f5d4'>-0.323</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|62|17.5962|17.5962|0.000|251718|251766|<span style='background-color:#f8d0d0'>0.019</span>|5344|5327|<span style='background-color:#d4f5d4'>-0.318</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|63|17.5982|17.5982|0.000|255728|255776|<span style='background-color:#f8d0d0'>0.019</span>|5533|5516|<span style='background-color:#d4f5d4'>-0.307</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|64|17.6082|17.6082|0.000|259718|259766|<span style='background-color:#f8d0d0'>0.018</span>|5540|5523|<span style='background-color:#d4f5d4'>-0.307</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|65|17.5962|17.5962|0.000|263795|263843|<span style='background-color:#f8d0d0'>0.018</span>|5619|5602|<span style='background-color:#d4f5d4'>-0.303</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|66|17.5982|17.5982|0.000|267805|267853|<span style='background-color:#f8d0d0'>0.018</span>|5808|5791|<span style='background-color:#d4f5d4'>-0.293</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|67|17.6082|17.6082|0.000|271795|271843|<span style='background-color:#f8d0d0'>0.018</span>|5815|5798|<span style='background-color:#d4f5d4'>-0.292</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|68|17.5962|17.5962|0.000|275872|275920|<span style='background-color:#f8d0d0'>0.017</span>|5894|5877|<span style='background-color:#d4f5d4'>-0.288</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|69|17.5982|17.5982|0.000|279882|279930|<span style='background-color:#f8d0d0'>0.017</span>|6083|6066|<span style='background-color:#d4f5d4'>-0.279</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|70|17.6082|17.6082|0.000|283872|283920|<span style='background-color:#f8d0d0'>0.017</span>|6090|6073|<span style='background-color:#d4f5d4'>-0.279</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|71|17.6504|17.6504|0.000|287834|287882|<span style='background-color:#f8d0d0'>0.017</span>|6108|6091|<span style='background-color:#d4f5d4'>-0.278</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|72|17.5802|17.5802|0.000|291850|291898|<span style='background-color:#f8d0d0'>0.016</span>|6165|6148|<span style='background-color:#d4f5d4'>-0.276</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|73|17.2954|17.2954|0.000|296158|296206|<span style='background-color:#f8d0d0'>0.016</span>|6475|6458|<span style='background-color:#d4f5d4'>-0.263</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|74|17.4731|17.4731|0.000|300582|300630|<span style='background-color:#f8d0d0'>0.016</span>|6716|6707|<span style='background-color:#d4f5d4'>-0.134</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|75|17.5683|17.5683|0.000|304783|304830|<span style='background-color:#f8d0d0'>0.015</span>|7035|7026|<span style='background-color:#d4f5d4'>-0.128</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|76|17.5146|17.5146|0.000|309060|309107|<span style='background-color:#f8d0d0'>0.015</span>|7426|7417|<span style='background-color:#d4f5d4'>-0.121</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|77|17.5623|17.5623|0.000|313395|313442|<span style='background-color:#f8d0d0'>0.015</span>|7798|7789|<span style='background-color:#d4f5d4'>-0.115</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|78|17.5583|17.5583|0.000|317601|317648|<span style='background-color:#f8d0d0'>0.015</span>|8080|8071|<span style='background-color:#d4f5d4'>-0.111</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|79|17.5503|17.5503|0.000|321905|321952|<span style='background-color:#f8d0d0'>0.015</span>|8434|8425|<span style='background-color:#d4f5d4'>-0.107</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|80|17.5324|17.5324|0.000|326366|326413|<span style='background-color:#f8d0d0'>0.014</span>|8735|8726|<span style='background-color:#d4f5d4'>-0.103</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|81|17.5205|17.5603|<span style='background-color:#d4f5d4'>0.227</span>|330598|330720|<span style='background-color:#f8d0d0'>0.037</span>|9153|9116|<span style='background-color:#d4f5d4'>-0.404</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|82|17.5424|17.3128|<span style='background-color:#f8d0d0'>-1.309</span>|334969|335322|<span style='background-color:#f8d0d0'>0.105</span>|9522|9462|<span style='background-color:#d4f5d4'>-0.630</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|83|17.3575|17.5563|<span style='background-color:#d4f5d4'>1.145</span>|339441|339613|<span style='background-color:#f8d0d0'>0.051</span>|9813|9818|<span style='background-color:#f8d0d0'>0.051</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|84|17.5324|17.5902|<span style='background-color:#d4f5d4'>0.330</span>|343744|343935|<span style='background-color:#f8d0d0'>0.056</span>|10160|10196|<span style='background-color:#f8d0d0'>0.354</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|85|17.5324|17.5603|<span style='background-color:#d4f5d4'>0.159</span>|348123|348309|<span style='background-color:#f8d0d0'>0.053</span>|10497|10598|<span style='background-color:#f8d0d0'>0.962</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|86|17.5583|17.5583|0.000|352425|352611|<span style='background-color:#f8d0d0'>0.053</span>|10816|10917|<span style='background-color:#f8d0d0'>0.934</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|87|17.5603|17.5603|0.000|356700|356886|<span style='background-color:#f8d0d0'>0.052</span>|11160|11261|<span style='background-color:#f8d0d0'>0.905</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|88|17.477|17.477|0.000|361148|361334|<span style='background-color:#f8d0d0'>0.052</span>|11551|11652|<span style='background-color:#f8d0d0'>0.874</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|89|17.2993|17.2993|0.000|365670|365856|<span style='background-color:#f8d0d0'>0.051</span>|11783|11884|<span style='background-color:#f8d0d0'>0.857</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|90|17.4357|17.4357|0.000|370009|370195|<span style='background-color:#f8d0d0'>0.050</span>|12191|12292|<span style='background-color:#f8d0d0'>0.828</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|91|17.5942|17.5942|0.000|374197|374383|<span style='background-color:#f8d0d0'>0.050</span>|12563|12664|<span style='background-color:#f8d0d0'>0.804</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|92|17.5503|17.5503|0.000|378404|378590|<span style='background-color:#f8d0d0'>0.049</span>|12839|12940|<span style='background-color:#f8d0d0'>0.787</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|93|17.5484|17.5484|0.000|382819|383005|<span style='background-color:#f8d0d0'>0.049</span>|13258|13359|<span style='background-color:#f8d0d0'>0.762</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|94|17.5324|17.5324|0.000|387220|387406|<span style='background-color:#f8d0d0'>0.048</span>|13596|13697|<span style='background-color:#f8d0d0'>0.743</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|95|17.5305|17.5305|0.000|391536|391722|<span style='background-color:#f8d0d0'>0.048</span>|13879|13980|<span style='background-color:#f8d0d0'>0.728</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|96|17.5663|17.5663|0.000|395874|396060|<span style='background-color:#f8d0d0'>0.047</span>|14298|14399|<span style='background-color:#f8d0d0'>0.706</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|97|17.5942|17.5942|0.000|400062|400248|<span style='background-color:#f8d0d0'>0.046</span>|14670|14771|<span style='background-color:#f8d0d0'>0.688</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|98|17.5503|17.5503|0.000|404269|404455|<span style='background-color:#f8d0d0'>0.046</span>|14946|15047|<span style='background-color:#f8d0d0'>0.676</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|99|17.5484|17.5484|0.000|408684|408870|<span style='background-color:#f8d0d0'>0.046</span>|15365|15466|<span style='background-color:#f8d0d0'>0.657</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|100|17.5324|17.5324|0.000|413085|413271|<span style='background-color:#f8d0d0'>0.045</span>|15703|15804|<span style='background-color:#f8d0d0'>0.643</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|101|17.4593|17.4593|0.000|417558|417744|<span style='background-color:#f8d0d0'>0.045</span>|16107|16208|<span style='background-color:#f8d0d0'>0.627</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|102|17.5902|17.5902|0.000|421782|421968|<span style='background-color:#f8d0d0'>0.044</span>|16429|16530|<span style='background-color:#f8d0d0'>0.615</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|103|17.5324|17.5324|0.000|426183|426369|<span style='background-color:#f8d0d0'>0.044</span>|16767|16868|<span style='background-color:#f8d0d0'>0.602</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|104|17.4593|17.4593|0.000|430656|430842|<span style='background-color:#f8d0d0'>0.043</span>|17171|17272|<span style='background-color:#f8d0d0'>0.588</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|105|17.5902|17.5902|0.000|434880|435066|<span style='background-color:#f8d0d0'>0.043</span>|17493|17594|<span style='background-color:#f8d0d0'>0.577</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|106|17.5324|17.5324|0.000|439281|439467|<span style='background-color:#f8d0d0'>0.042</span>|17831|17932|<span style='background-color:#f8d0d0'>0.566</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|107|17.4593|17.4593|0.000|443754|443940|<span style='background-color:#f8d0d0'>0.042</span>|18235|18336|<span style='background-color:#f8d0d0'>0.554</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|108|17.5902|17.5902|0.000|447978|448164|<span style='background-color:#f8d0d0'>0.042</span>|18557|18658|<span style='background-color:#f8d0d0'>0.544</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|109|17.5324|17.5324|0.000|452379|452565|<span style='background-color:#f8d0d0'>0.041</span>|18895|18996|<span style='background-color:#f8d0d0'>0.535</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|110|17.4593|17.4593|0.000|456852|457038|<span style='background-color:#f8d0d0'>0.041</span>|19299|19400|<span style='background-color:#f8d0d0'>0.523</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|111|17.5643|17.5643|0.000|461158|461344|<span style='background-color:#f8d0d0'>0.040</span>|19680|19781|<span style='background-color:#f8d0d0'>0.513</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|112|17.5583|17.5583|0.000|465629|465815|<span style='background-color:#f8d0d0'>0.040</span>|20006|20107|<span style='background-color:#f8d0d0'>0.505</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|113|17.3672|17.3692|<span style='background-color:#d4f5d4'>0.012</span>|470210|470396|<span style='background-color:#f8d0d0'>0.040</span>|20420|20521|<span style='background-color:#f8d0d0'>0.495</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|114|17.377|17.4435|<span style='background-color:#d4f5d4'>0.383</span>|474970|474966|<span style='background-color:#d4f5d4'>-0.001</span>|20960|20995|<span style='background-color:#f8d0d0'>0.167</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|115|17.4475|17.4475|0.000|479578|479573|<span style='background-color:#d4f5d4'>-0.001</span>|21354|21389|<span style='background-color:#f8d0d0'>0.164</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|116|17.4908|17.4908|0.000|484262|484257|<span style='background-color:#d4f5d4'>-0.001</span>|21766|21801|<span style='background-color:#f8d0d0'>0.161</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|117|17.3867|17.3867|0.000|488916|488911|<span style='background-color:#d4f5d4'>-0.001</span>|22262|22297|<span style='background-color:#f8d0d0'>0.157</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|118|17.4691|17.4691|0.000|493562|493557|<span style='background-color:#d4f5d4'>-0.001</span>|22566|22601|<span style='background-color:#f8d0d0'>0.155</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|119|17.4278|17.4278|0.000|498230|498225|<span style='background-color:#d4f5d4'>-0.001</span>|23046|23081|<span style='background-color:#f8d0d0'>0.152</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|120|17.3264|17.3264|0.000|502934|502929|<span style='background-color:#d4f5d4'>-0.001</span>|23596|23631|<span style='background-color:#f8d0d0'>0.148</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|121|17.4475|17.4553|<span style='background-color:#d4f5d4'>0.045</span>|507639|507579|<span style='background-color:#d4f5d4'>-0.012</span>|24048|24065|<span style='background-color:#f8d0d0'>0.071</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|122|17.3303|17.3672|<span style='background-color:#d4f5d4'>0.213</span>|512287|512151|<span style='background-color:#d4f5d4'>-0.027</span>|24558|24616|<span style='background-color:#f8d0d0'>0.236</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|123|17.4632|17.2492|<span style='background-color:#f8d0d0'>-1.225</span>|516859|516786|<span style='background-color:#d4f5d4'>-0.014</span>|24829|24988|<span style='background-color:#f8d0d0'>0.640</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|124|17.4396|17.4141|<span style='background-color:#f8d0d0'>-0.146</span>|521496|521540|<span style='background-color:#f8d0d0'>0.008</span>|25255|25466|<span style='background-color:#f8d0d0'>0.835</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|125|17.3283|17.4416|<span style='background-color:#d4f5d4'>0.654</span>|526229|526237|<span style='background-color:#f8d0d0'>0.002</span>|25796|25973|<span style='background-color:#f8d0d0'>0.686</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|126|17.4318|17.4318|0.000|530811|530819|<span style='background-color:#f8d0d0'>0.002</span>|26156|26333|<span style='background-color:#f8d0d0'>0.677</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|127|17.3984|17.3984|0.000|535478|535486|<span style='background-color:#f8d0d0'>0.001</span>|26438|26615|<span style='background-color:#f8d0d0'>0.669</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|128|17.3283|17.3283|0.000|540194|540202|<span style='background-color:#f8d0d0'>0.001</span>|26993|27170|<span style='background-color:#f8d0d0'>0.656</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|129|17.4161|17.4161|0.000|544813|544821|<span style='background-color:#f8d0d0'>0.001</span>|27304|27481|<span style='background-color:#f8d0d0'>0.648</span>|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|130|17.4416|17.4416|0.000|549454|549462|<span style='background-color:#f8d0d0'>0.001</span>|27774|27951|<span style='background-color:#f8d0d0'>0.637</span>|

## Averages

|variant|benchmark|ipc_gain_pct|read_change_pct|write_change_pct|
|---|---|---|---|---|
|l2_max_merge_zero|backprop-rodinia-2.0-ft|<span style='background-color:#f8d0d0'>-0.383</span>|<span style='background-color:#f8d0d0'>7.076</span>|<span style='background-color:#d4f5d4'>-12.657</span>|
|l2_max_merge_zero|bfs-rodinia-2.0-ft|<span style='background-color:#f8d0d0'>-0.021</span>|<span style='background-color:#d4f5d4'>-0.039</span>|<span style='background-color:#f8d0d0'>29.955</span>|
|l2_max_merge_zero|heartwall-rodinia-2.0-ft|<span style='background-color:#f8d0d0'>-5.896</span>|<span style='background-color:#f8d0d0'>69.090</span>|<span style='background-color:#f8d0d0'>395.588</span>|
|l2_max_merge_zero|hotspot-rodinia-2.0-ft|<span style='background-color:#f8d0d0'>-1.108</span>|<span style='background-color:#d4f5d4'>-0.406</span>|0.000|
|l2_max_merge_zero|lud-rodinia-2.0-ft|0.000|0.000|0.000|
|l2_max_merge_zero|nn-rodinia-2.0-ft|0.000|0.000|0.000|
|l2_max_merge_zero|nw-rodinia-2.0-ft|0.000|0.000|0.000|
|l2_max_merge_zero|pathfinder-rodinia-2.0-ft|<span style='background-color:#f8d0d0'>-2.547</span>|<span style='background-color:#d4f5d4'>-4.016</span>|<span style='background-color:#d4f5d4'>-0.174</span>|
|l2_max_merge_zero|srad_v2-rodinia-2.0-ft|0.000|0.000|0.000|
|l2_max_merge_zero|streamcluster-rodinia-2.0-ft|<span style='background-color:#f8d0d0'>-0.008</span>|<span style='background-color:#f8d0d0'>0.057</span>|<span style='background-color:#d4f5d4'>-1.214</span>|

## Overall Summary

### l2_max_merge_zero

- IPC geomean percent change: <b>-1.013%</b>
- L2_BW geomean percent change: <b>-1.013%</b>
- L2_total_cache_accesses geomean percent change: <b>0.000%</b>
- L2_GLOBAL_ACC_W_TOTAL_ACCESS geomean percent change: <b>0.000%</b>
- MISS_QUEUE_FULL geomean percent change: <b>22.602%</b>
- MSHR_MERGE_ENTRY_FAIL geomean percent change: <b>12.356%</b>