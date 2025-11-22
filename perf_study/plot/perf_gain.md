# Performance Gain Report

## Per-Kernel Details (colored)

|benchmark|kernel_index|ipc_base|ipc_tuned|ipc_gain_pct|read_base|read_tuned|read_change_pct|write_base|write_tuned|write_change_pct|
|---|---|---|---|---|---|---|---|---|---|---|
|backprop-rodinia-2.0-ft|1|834.9478|829.3835|<span style='background-color:#f8d0d0'>-0.666</span>|42836|38311|<span style='background-color:#d4f5d4'>-10.564</span>|6884|1352|<span style='background-color:#d4f5d4'>-80.360</span>|
|backprop-rodinia-2.0-ft|2|371.7225|374.1901|<span style='background-color:#d4f5d4'>0.664</span>|179145|151065|<span style='background-color:#d4f5d4'>-15.674</span>|9739|1543|<span style='background-color:#d4f5d4'>-84.156</span>|
|bfs-rodinia-2.0-ft|1|3.691|3.691|0.000|0|0|0.000|0|0|0.000|
|bfs-rodinia-2.0-ft|2|7.9852|7.9852|0.000|0|0|0.000|0|0|0.000|
|bfs-rodinia-2.0-ft|3|3.9985|3.9985|0.000|0|0|0.000|0|0|0.000|
|bfs-rodinia-2.0-ft|4|8.286|8.286|0.000|0|0|0.000|0|0|0.000|
|bfs-rodinia-2.0-ft|5|4.8361|4.8361|0.000|0|0|0.000|0|0|0.000|
|bfs-rodinia-2.0-ft|6|8.8546|8.8546|0.000|0|0|0.000|0|0|0.000|
|bfs-rodinia-2.0-ft|7|9.0819|9.0802|<span style='background-color:#f8d0d0'>-0.019</span>|71|0|<span style='background-color:#d4f5d4'>-100.000</span>|0|0|0.000|
|bfs-rodinia-2.0-ft|8|11.5803|11.5803|0.000|71|0|<span style='background-color:#d4f5d4'>-100.000</span>|0|0|0.000|
|bfs-rodinia-2.0-ft|9|21.4818|21.6469|<span style='background-color:#d4f5d4'>0.769</span>|2399|1352|<span style='background-color:#d4f5d4'>-43.643</span>|111|0|<span style='background-color:#d4f5d4'>-100.000</span>|
|bfs-rodinia-2.0-ft|10|12.8834|12.8834|0.000|2399|1352|<span style='background-color:#d4f5d4'>-43.643</span>|111|0|<span style='background-color:#d4f5d4'>-100.000</span>|
|bfs-rodinia-2.0-ft|11|24.0576|24.055|<span style='background-color:#f8d0d0'>-0.011</span>|4883|2961|<span style='background-color:#d4f5d4'>-39.361</span>|111|0|<span style='background-color:#d4f5d4'>-100.000</span>|
|bfs-rodinia-2.0-ft|12|8.6567|8.6567|0.000|4883|2961|<span style='background-color:#d4f5d4'>-39.361</span>|111|0|<span style='background-color:#d4f5d4'>-100.000</span>|
|bfs-rodinia-2.0-ft|13|6.9936|6.983|<span style='background-color:#f8d0d0'>-0.152</span>|4891|2961|<span style='background-color:#d4f5d4'>-39.460</span>|111|0|<span style='background-color:#d4f5d4'>-100.000</span>|
|bfs-rodinia-2.0-ft|14|8.1941|8.1941|0.000|4891|2961|<span style='background-color:#d4f5d4'>-39.460</span>|111|0|<span style='background-color:#d4f5d4'>-100.000</span>|
|bfs-rodinia-2.0-ft|15|6.5952|6.5952|0.000|4891|2961|<span style='background-color:#d4f5d4'>-39.460</span>|111|0|<span style='background-color:#d4f5d4'>-100.000</span>|
|bfs-rodinia-2.0-ft|16|8.5236|8.5236|0.000|4891|2961|<span style='background-color:#d4f5d4'>-39.460</span>|111|0|<span style='background-color:#d4f5d4'>-100.000</span>|
|heartwall-rodinia-2.0-ft|1|763.9442|767.4275|<span style='background-color:#d4f5d4'>0.456</span>|17376|15078|<span style='background-color:#d4f5d4'>-13.225</span>|68|0|<span style='background-color:#d4f5d4'>-100.000</span>|
|hotspot-rodinia-2.0-ft|1|596.4451|595.7861|<span style='background-color:#f8d0d0'>-0.110</span>|3307|1328|<span style='background-color:#d4f5d4'>-59.843</span>|0|0|0.000|
|hotspot-rodinia-2.0-ft|2|601.9191|601.6953|<span style='background-color:#f8d0d0'>-0.037</span>|7159|2949|<span style='background-color:#d4f5d4'>-58.807</span>|0|0|0.000|
|hotspot-rodinia-2.0-ft|3|618.4879|619.5933|<span style='background-color:#d4f5d4'>0.179</span>|11093|4616|<span style='background-color:#d4f5d4'>-58.388</span>|0|0|0.000|
|hotspot-rodinia-2.0-ft|4|619.7515|618.8822|<span style='background-color:#f8d0d0'>-0.140</span>|15017|6258|<span style='background-color:#d4f5d4'>-58.327</span>|0|0|0.000|
|hotspot-rodinia-2.0-ft|5|618.6455|619.989|<span style='background-color:#d4f5d4'>0.217</span>|18931|7937|<span style='background-color:#d4f5d4'>-58.074</span>|0|0|0.000|
|hotspot-rodinia-2.0-ft|6|619.9099|620.7026|<span style='background-color:#d4f5d4'>0.128</span>|22865|9587|<span style='background-color:#d4f5d4'>-58.071</span>|0|0|0.000|
|hotspot-rodinia-2.0-ft|7|494.2744|493.0972|<span style='background-color:#f8d0d0'>-0.238</span>|23828|9929|<span style='background-color:#d4f5d4'>-58.331</span>|0|0|0.000|
|lud-rodinia-2.0-ft|1|0.7762|0.7762|0.000|0|0|0.000|0|0|0.000|
|lud-rodinia-2.0-ft|2|4.9649|4.9649|0.000|0|0|0.000|0|0|0.000|
|lud-rodinia-2.0-ft|3|26.7007|26.6291|<span style='background-color:#f8d0d0'>-0.268</span>|242|0|<span style='background-color:#d4f5d4'>-100.000</span>|0|0|0.000|
|lud-rodinia-2.0-ft|4|0.7811|0.7811|0.000|242|0|<span style='background-color:#d4f5d4'>-100.000</span>|0|0|0.000|
|lud-rodinia-2.0-ft|5|3.3975|3.3975|0.000|242|0|<span style='background-color:#d4f5d4'>-100.000</span>|0|0|0.000|
|lud-rodinia-2.0-ft|6|12.1465|12.1444|<span style='background-color:#f8d0d0'>-0.017</span>|327|0|<span style='background-color:#d4f5d4'>-100.000</span>|0|0|0.000|
|lud-rodinia-2.0-ft|7|0.7811|0.7811|0.000|327|0|<span style='background-color:#d4f5d4'>-100.000</span>|0|0|0.000|
|lud-rodinia-2.0-ft|8|1.6993|1.6993|0.000|327|0|<span style='background-color:#d4f5d4'>-100.000</span>|0|0|0.000|
|lud-rodinia-2.0-ft|9|3.045|3.0492|<span style='background-color:#d4f5d4'>0.138</span>|360|0|<span style='background-color:#d4f5d4'>-100.000</span>|0|0|0.000|
|lud-rodinia-2.0-ft|10|0.7811|0.7811|0.000|360|0|<span style='background-color:#d4f5d4'>-100.000</span>|0|0|0.000|
|nn-rodinia-2.0-ft|1|217.5636|218.2486|<span style='background-color:#d4f5d4'>0.315</span>|12699|8745|<span style='background-color:#d4f5d4'>-31.136</span>|0|0|0.000|
|nn-rodinia-2.0-ft|2|227.4201|226.2898|<span style='background-color:#f8d0d0'>-0.497</span>|23765|15141|<span style='background-color:#d4f5d4'>-36.289</span>|0|0|0.000|
|nn-rodinia-2.0-ft|3|227.2331|228.4328|<span style='background-color:#d4f5d4'>0.528</span>|35209|21813|<span style='background-color:#d4f5d4'>-38.047</span>|0|0|0.000|
|nn-rodinia-2.0-ft|4|227.5499|225.9169|<span style='background-color:#f8d0d0'>-0.718</span>|46202|28066|<span style='background-color:#d4f5d4'>-39.254</span>|0|0|0.000|
|nw-rodinia-2.0-ft|1|0.9613|0.9613|0.000|0|0|0.000|0|0|0.000|
|nw-rodinia-2.0-ft|2|1.9271|1.9271|0.000|0|0|0.000|0|0|0.000|
|nw-rodinia-2.0-ft|3|2.8869|2.8869|0.000|0|0|0.000|0|0|0.000|
|nw-rodinia-2.0-ft|4|3.8546|3.8546|0.000|0|0|0.000|0|0|0.000|
|nw-rodinia-2.0-ft|5|4.8172|4.8172|0.000|0|0|0.000|0|0|0.000|
|nw-rodinia-2.0-ft|6|5.7819|5.7819|0.000|0|0|0.000|0|0|0.000|
|nw-rodinia-2.0-ft|7|6.7426|6.7426|0.000|0|0|0.000|0|0|0.000|
|nw-rodinia-2.0-ft|8|7.705|7.705|0.000|0|0|0.000|0|0|0.000|
|nw-rodinia-2.0-ft|9|6.844|6.844|0.000|0|0|0.000|0|0|0.000|
|nw-rodinia-2.0-ft|10|5.8682|5.8682|0.000|0|0|0.000|0|0|0.000|
|nw-rodinia-2.0-ft|11|4.8901|4.8901|0.000|0|0|0.000|0|0|0.000|
|nw-rodinia-2.0-ft|12|3.9138|3.9138|0.000|0|0|0.000|0|0|0.000|
|nw-rodinia-2.0-ft|13|2.936|2.936|0.000|0|0|0.000|0|0|0.000|
|nw-rodinia-2.0-ft|14|1.9567|1.9567|0.000|0|0|0.000|0|0|0.000|
|nw-rodinia-2.0-ft|15|0.9787|0.9787|0.000|0|0|0.000|0|0|0.000|
|pathfinder-rodinia-2.0-ft|1|32.268|32.244|<span style='background-color:#f8d0d0'>-0.074</span>|247|0|<span style='background-color:#d4f5d4'>-100.000</span>|81|0|<span style='background-color:#d4f5d4'>-100.000</span>|
|pathfinder-rodinia-2.0-ft|2|32.9355|32.9855|<span style='background-color:#d4f5d4'>0.152</span>|489|0|<span style='background-color:#d4f5d4'>-100.000</span>|165|0|<span style='background-color:#d4f5d4'>-100.000</span>|
|pathfinder-rodinia-2.0-ft|3|32.9272|32.8651|<span style='background-color:#f8d0d0'>-0.189</span>|736|0|<span style='background-color:#d4f5d4'>-100.000</span>|249|0|<span style='background-color:#d4f5d4'>-100.000</span>|
|pathfinder-rodinia-2.0-ft|4|29.1348|29.1465|<span style='background-color:#d4f5d4'>0.040</span>|924|0|<span style='background-color:#d4f5d4'>-100.000</span>|339|0|<span style='background-color:#d4f5d4'>-100.000</span>|
|srad_v2-rodinia-2.0-ft|1|475.8292|475.7074|<span style='background-color:#f8d0d0'>-0.026</span>|78|0|<span style='background-color:#d4f5d4'>-100.000</span>|4160|3136|<span style='background-color:#d4f5d4'>-24.615</span>|
|srad_v2-rodinia-2.0-ft|2|187.5066|187.6918|<span style='background-color:#d4f5d4'>0.099</span>|2995|1723|<span style='background-color:#d4f5d4'>-42.471</span>|4224|3136|<span style='background-color:#d4f5d4'>-25.758</span>|
|srad_v2-rodinia-2.0-ft|3|473.5039|474.5914|<span style='background-color:#d4f5d4'>0.230</span>|3068|1723|<span style='background-color:#d4f5d4'>-43.840</span>|8384|6272|<span style='background-color:#d4f5d4'>-25.191</span>|
|srad_v2-rodinia-2.0-ft|4|188.5967|189.1869|<span style='background-color:#d4f5d4'>0.313</span>|5953|3433|<span style='background-color:#d4f5d4'>-42.332</span>|8448|6272|<span style='background-color:#d4f5d4'>-25.758</span>|
|streamcluster-rodinia-2.0-ft|1|16.2309|16.3078|<span style='background-color:#d4f5d4'>0.474</span>|4761|4073|<span style='background-color:#d4f5d4'>-14.451</span>|434|34|<span style='background-color:#d4f5d4'>-92.166</span>|
|streamcluster-rodinia-2.0-ft|2|17.2089|17.2607|<span style='background-color:#d4f5d4'>0.301</span>|8788|7661|<span style='background-color:#d4f5d4'>-12.824</span>|475|34|<span style='background-color:#d4f5d4'>-92.842</span>|
|streamcluster-rodinia-2.0-ft|3|17.3245|17.2858|<span style='background-color:#f8d0d0'>-0.223</span>|12733|11196|<span style='background-color:#d4f5d4'>-12.071</span>|476|34|<span style='background-color:#d4f5d4'>-92.857</span>|
|streamcluster-rodinia-2.0-ft|4|17.3478|17.3516|<span style='background-color:#d4f5d4'>0.022</span>|16757|14836|<span style='background-color:#d4f5d4'>-11.464</span>|556|34|<span style='background-color:#d4f5d4'>-93.885</span>|
|streamcluster-rodinia-2.0-ft|5|17.3478|17.2723|<span style='background-color:#f8d0d0'>-0.435</span>|20774|18388|<span style='background-color:#d4f5d4'>-11.486</span>|623|34|<span style='background-color:#d4f5d4'>-94.543</span>|
|streamcluster-rodinia-2.0-ft|6|17.5802|17.5782|<span style='background-color:#f8d0d0'>-0.011</span>|24747|21942|<span style='background-color:#d4f5d4'>-11.335</span>|629|34|<span style='background-color:#d4f5d4'>-94.595</span>|
|streamcluster-rodinia-2.0-ft|7|17.5942|17.5663|<span style='background-color:#f8d0d0'>-0.159</span>|28787|25568|<span style='background-color:#d4f5d4'>-11.182</span>|719|34|<span style='background-color:#d4f5d4'>-95.271</span>|
|streamcluster-rodinia-2.0-ft|8|17.5762|17.5703|<span style='background-color:#f8d0d0'>-0.034</span>|32911|29185|<span style='background-color:#d4f5d4'>-11.321</span>|864|34|<span style='background-color:#d4f5d4'>-96.065</span>|
|streamcluster-rodinia-2.0-ft|9|17.6142|17.5882|<span style='background-color:#f8d0d0'>-0.148</span>|36955|32744|<span style='background-color:#d4f5d4'>-11.395</span>|889|34|<span style='background-color:#d4f5d4'>-96.175</span>|
|streamcluster-rodinia-2.0-ft|10|17.5862|17.5982|<span style='background-color:#d4f5d4'>0.068</span>|40973|36383|<span style='background-color:#d4f5d4'>-11.202</span>|955|34|<span style='background-color:#d4f5d4'>-96.440</span>|
|streamcluster-rodinia-2.0-ft|11|17.5802|17.5782|<span style='background-color:#f8d0d0'>-0.011</span>|44946|39937|<span style='background-color:#d4f5d4'>-11.144</span>|961|34|<span style='background-color:#d4f5d4'>-96.462</span>|
|streamcluster-rodinia-2.0-ft|12|17.5942|17.5663|<span style='background-color:#f8d0d0'>-0.159</span>|48986|43563|<span style='background-color:#d4f5d4'>-11.071</span>|1051|34|<span style='background-color:#d4f5d4'>-96.765</span>|
|streamcluster-rodinia-2.0-ft|13|17.5762|17.5703|<span style='background-color:#f8d0d0'>-0.034</span>|53110|47180|<span style='background-color:#d4f5d4'>-11.166</span>|1196|34|<span style='background-color:#d4f5d4'>-97.157</span>|
|streamcluster-rodinia-2.0-ft|14|17.6142|17.5882|<span style='background-color:#f8d0d0'>-0.148</span>|57154|50739|<span style='background-color:#d4f5d4'>-11.224</span>|1221|34|<span style='background-color:#d4f5d4'>-97.215</span>|
|streamcluster-rodinia-2.0-ft|15|17.5862|17.5982|<span style='background-color:#d4f5d4'>0.068</span>|61172|54378|<span style='background-color:#d4f5d4'>-11.106</span>|1287|34|<span style='background-color:#d4f5d4'>-97.358</span>|
|streamcluster-rodinia-2.0-ft|16|17.6002|17.5743|<span style='background-color:#f8d0d0'>-0.147</span>|65195|57931|<span style='background-color:#d4f5d4'>-11.142</span>|1359|34|<span style='background-color:#d4f5d4'>-97.498</span>|
|streamcluster-rodinia-2.0-ft|17|17.5802|17.5782|<span style='background-color:#f8d0d0'>-0.011</span>|69168|61485|<span style='background-color:#d4f5d4'>-11.108</span>|1365|34|<span style='background-color:#d4f5d4'>-97.509</span>|
|streamcluster-rodinia-2.0-ft|18|17.5942|17.5663|<span style='background-color:#f8d0d0'>-0.159</span>|73208|65111|<span style='background-color:#d4f5d4'>-11.060</span>|1455|34|<span style='background-color:#d4f5d4'>-97.663</span>|
|streamcluster-rodinia-2.0-ft|19|17.5762|17.5703|<span style='background-color:#f8d0d0'>-0.034</span>|77332|68728|<span style='background-color:#d4f5d4'>-11.126</span>|1600|34|<span style='background-color:#d4f5d4'>-97.875</span>|
|streamcluster-rodinia-2.0-ft|20|17.6142|17.5882|<span style='background-color:#f8d0d0'>-0.148</span>|81376|72287|<span style='background-color:#d4f5d4'>-11.169</span>|1625|34|<span style='background-color:#d4f5d4'>-97.908</span>|
|streamcluster-rodinia-2.0-ft|21|17.5762|17.5703|<span style='background-color:#f8d0d0'>-0.034</span>|85500|75904|<span style='background-color:#d4f5d4'>-11.223</span>|1770|34|<span style='background-color:#d4f5d4'>-98.079</span>|
|streamcluster-rodinia-2.0-ft|22|17.5942|17.5663|<span style='background-color:#f8d0d0'>-0.159</span>|89540|79530|<span style='background-color:#d4f5d4'>-11.179</span>|1860|34|<span style='background-color:#d4f5d4'>-98.172</span>|
|streamcluster-rodinia-2.0-ft|23|17.6142|17.5882|<span style='background-color:#f8d0d0'>-0.148</span>|93584|83089|<span style='background-color:#d4f5d4'>-11.215</span>|1885|34|<span style='background-color:#d4f5d4'>-98.196</span>|
|streamcluster-rodinia-2.0-ft|24|17.5762|17.5703|<span style='background-color:#f8d0d0'>-0.034</span>|97708|86706|<span style='background-color:#d4f5d4'>-11.260</span>|2030|34|<span style='background-color:#d4f5d4'>-98.325</span>|
|streamcluster-rodinia-2.0-ft|25|17.5942|17.5663|<span style='background-color:#f8d0d0'>-0.159</span>|101748|90332|<span style='background-color:#d4f5d4'>-11.220</span>|2120|34|<span style='background-color:#d4f5d4'>-98.396</span>|
|streamcluster-rodinia-2.0-ft|26|17.6142|17.5882|<span style='background-color:#f8d0d0'>-0.148</span>|105792|93891|<span style='background-color:#d4f5d4'>-11.249</span>|2145|34|<span style='background-color:#d4f5d4'>-98.415</span>|
|streamcluster-rodinia-2.0-ft|27|17.5762|17.5703|<span style='background-color:#f8d0d0'>-0.034</span>|109916|97508|<span style='background-color:#d4f5d4'>-11.289</span>|2290|34|<span style='background-color:#d4f5d4'>-98.515</span>|
|streamcluster-rodinia-2.0-ft|28|17.5942|17.5663|<span style='background-color:#f8d0d0'>-0.159</span>|113956|101134|<span style='background-color:#d4f5d4'>-11.252</span>|2380|34|<span style='background-color:#d4f5d4'>-98.571</span>|
|streamcluster-rodinia-2.0-ft|29|17.6142|17.5882|<span style='background-color:#f8d0d0'>-0.148</span>|118000|104693|<span style='background-color:#d4f5d4'>-11.277</span>|2405|34|<span style='background-color:#d4f5d4'>-98.586</span>|
|streamcluster-rodinia-2.0-ft|30|17.5762|17.5703|<span style='background-color:#f8d0d0'>-0.034</span>|122124|108310|<span style='background-color:#d4f5d4'>-11.311</span>|2550|34|<span style='background-color:#d4f5d4'>-98.667</span>|
|streamcluster-rodinia-2.0-ft|31|17.6002|17.5743|<span style='background-color:#f8d0d0'>-0.147</span>|126147|111863|<span style='background-color:#d4f5d4'>-11.323</span>|2622|34|<span style='background-color:#d4f5d4'>-98.703</span>|
|streamcluster-rodinia-2.0-ft|32|17.5802|17.5782|<span style='background-color:#f8d0d0'>-0.011</span>|130120|115417|<span style='background-color:#d4f5d4'>-11.300</span>|2628|34|<span style='background-color:#d4f5d4'>-98.706</span>|
|streamcluster-rodinia-2.0-ft|33|17.5942|17.5663|<span style='background-color:#f8d0d0'>-0.159</span>|134160|119043|<span style='background-color:#d4f5d4'>-11.268</span>|2718|34|<span style='background-color:#d4f5d4'>-98.749</span>|
|streamcluster-rodinia-2.0-ft|34|17.5762|17.5703|<span style='background-color:#f8d0d0'>-0.034</span>|138284|122660|<span style='background-color:#d4f5d4'>-11.298</span>|2863|34|<span style='background-color:#d4f5d4'>-98.812</span>|
|streamcluster-rodinia-2.0-ft|35|17.6142|17.5882|<span style='background-color:#f8d0d0'>-0.148</span>|142328|126219|<span style='background-color:#d4f5d4'>-11.318</span>|2888|34|<span style='background-color:#d4f5d4'>-98.823</span>|
|streamcluster-rodinia-2.0-ft|36|17.5862|17.5982|<span style='background-color:#d4f5d4'>0.068</span>|146346|129858|<span style='background-color:#d4f5d4'>-11.266</span>|2954|34|<span style='background-color:#d4f5d4'>-98.849</span>|
|streamcluster-rodinia-2.0-ft|37|17.6002|17.5743|<span style='background-color:#f8d0d0'>-0.147</span>|150369|133411|<span style='background-color:#d4f5d4'>-11.278</span>|3026|34|<span style='background-color:#d4f5d4'>-98.876</span>|
|streamcluster-rodinia-2.0-ft|38|17.5802|17.5782|<span style='background-color:#f8d0d0'>-0.011</span>|154342|136965|<span style='background-color:#d4f5d4'>-11.259</span>|3032|34|<span style='background-color:#d4f5d4'>-98.879</span>|
|streamcluster-rodinia-2.0-ft|39|17.5942|17.5663|<span style='background-color:#f8d0d0'>-0.159</span>|158382|140591|<span style='background-color:#d4f5d4'>-11.233</span>|3122|34|<span style='background-color:#d4f5d4'>-98.911</span>|
|streamcluster-rodinia-2.0-ft|40|17.5762|17.5703|<span style='background-color:#f8d0d0'>-0.034</span>|162506|144208|<span style='background-color:#d4f5d4'>-11.260</span>|3267|34|<span style='background-color:#d4f5d4'>-98.959</span>|
|streamcluster-rodinia-2.0-ft|41|17.6665|17.5126|<span style='background-color:#f8d0d0'>-0.871</span>|166616|147632|<span style='background-color:#d4f5d4'>-11.394</span>|3334|34|<span style='background-color:#d4f5d4'>-98.980</span>|
|streamcluster-rodinia-2.0-ft|42|17.5802|17.6263|<span style='background-color:#d4f5d4'>0.262</span>|170581|151225|<span style='background-color:#d4f5d4'>-11.347</span>|3442|34|<span style='background-color:#d4f5d4'>-99.012</span>|
|streamcluster-rodinia-2.0-ft|43|17.5484|17.5603|<span style='background-color:#d4f5d4'>0.068</span>|174596|154665|<span style='background-color:#d4f5d4'>-11.415</span>|3449|34|<span style='background-color:#d4f5d4'>-99.014</span>|
|streamcluster-rodinia-2.0-ft|44|17.6263|17.6102|<span style='background-color:#f8d0d0'>-0.091</span>|178734|158221|<span style='background-color:#d4f5d4'>-11.477</span>|3530|34|<span style='background-color:#d4f5d4'>-99.037</span>|
|streamcluster-rodinia-2.0-ft|45|17.5862|17.6062|<span style='background-color:#d4f5d4'>0.114</span>|182894|161680|<span style='background-color:#d4f5d4'>-11.599</span>|3734|37|<span style='background-color:#d4f5d4'>-99.009</span>|
|streamcluster-rodinia-2.0-ft|46|17.5802|17.5882|<span style='background-color:#d4f5d4'>0.046</span>|186910|165016|<span style='background-color:#d4f5d4'>-11.714</span>|3791|37|<span style='background-color:#d4f5d4'>-99.024</span>|
|streamcluster-rodinia-2.0-ft|47|17.5962|17.6464|<span style='background-color:#d4f5d4'>0.285</span>|190987|168542|<span style='background-color:#d4f5d4'>-11.752</span>|3870|37|<span style='background-color:#d4f5d4'>-99.044</span>|
|streamcluster-rodinia-2.0-ft|48|17.5962|17.5723|<span style='background-color:#f8d0d0'>-0.136</span>|195018|172189|<span style='background-color:#d4f5d4'>-11.706</span>|4033|53|<span style='background-color:#d4f5d4'>-98.686</span>|
|streamcluster-rodinia-2.0-ft|49|17.6042|17.6303|<span style='background-color:#d4f5d4'>0.148</span>|198860|175607|<span style='background-color:#d4f5d4'>-11.693</span>|4033|53|<span style='background-color:#d4f5d4'>-98.686</span>|
|streamcluster-rodinia-2.0-ft|50|17.6183|17.6343|<span style='background-color:#d4f5d4'>0.091</span>|202855|178712|<span style='background-color:#d4f5d4'>-11.902</span>|4127|53|<span style='background-color:#d4f5d4'>-98.716</span>|
|streamcluster-rodinia-2.0-ft|51|17.3439|17.6062|<span style='background-color:#d4f5d4'>1.512</span>|207061|182009|<span style='background-color:#d4f5d4'>-12.099</span>|4287|59|<span style='background-color:#d4f5d4'>-98.624</span>|
|streamcluster-rodinia-2.0-ft|52|17.5782|17.6243|<span style='background-color:#d4f5d4'>0.262</span>|211100|185634|<span style='background-color:#d4f5d4'>-12.063</span>|4363|59|<span style='background-color:#d4f5d4'>-98.648</span>|
|streamcluster-rodinia-2.0-ft|53|17.5683|17.5982|<span style='background-color:#d4f5d4'>0.170</span>|215198|189293|<span style='background-color:#d4f5d4'>-12.038</span>|4406|59|<span style='background-color:#d4f5d4'>-98.661</span>|
|streamcluster-rodinia-2.0-ft|54|17.5982|17.6343|<span style='background-color:#d4f5d4'>0.205</span>|219208|192862|<span style='background-color:#d4f5d4'>-12.019</span>|4595|59|<span style='background-color:#d4f5d4'>-98.716</span>|
|streamcluster-rodinia-2.0-ft|55|17.5523|17.6343|<span style='background-color:#d4f5d4'>0.467</span>|223336|196020|<span style='background-color:#d4f5d4'>-12.231</span>|4772|59|<span style='background-color:#d4f5d4'>-98.764</span>|
|streamcluster-rodinia-2.0-ft|56|17.6504|17.6524|<span style='background-color:#d4f5d4'>0.011</span>|227298|199716|<span style='background-color:#d4f5d4'>-12.135</span>|4790|59|<span style='background-color:#d4f5d4'>-98.768</span>|
|streamcluster-rodinia-2.0-ft|57|17.3439|17.6062|<span style='background-color:#d4f5d4'>1.512</span>|231504|203013|<span style='background-color:#d4f5d4'>-12.307</span>|4950|65|<span style='background-color:#d4f5d4'>-98.687</span>|
|streamcluster-rodinia-2.0-ft|58|17.5782|17.6243|<span style='background-color:#d4f5d4'>0.262</span>|235543|206638|<span style='background-color:#d4f5d4'>-12.272</span>|5026|65|<span style='background-color:#d4f5d4'>-98.707</span>|
|streamcluster-rodinia-2.0-ft|59|17.5683|17.5982|<span style='background-color:#d4f5d4'>0.170</span>|239641|210297|<span style='background-color:#d4f5d4'>-12.245</span>|5069|65|<span style='background-color:#d4f5d4'>-98.718</span>|
|streamcluster-rodinia-2.0-ft|60|17.5982|17.6343|<span style='background-color:#d4f5d4'>0.205</span>|243651|213866|<span style='background-color:#d4f5d4'>-12.224</span>|5258|65|<span style='background-color:#d4f5d4'>-98.764</span>|
|streamcluster-rodinia-2.0-ft|61|17.6082|17.5942|<span style='background-color:#f8d0d0'>-0.080</span>|247641|217473|<span style='background-color:#d4f5d4'>-12.182</span>|5265|65|<span style='background-color:#d4f5d4'>-98.765</span>|
|streamcluster-rodinia-2.0-ft|62|17.5962|17.6464|<span style='background-color:#d4f5d4'>0.285</span>|251718|220999|<span style='background-color:#d4f5d4'>-12.204</span>|5344|65|<span style='background-color:#d4f5d4'>-98.784</span>|
|streamcluster-rodinia-2.0-ft|63|17.5982|17.6343|<span style='background-color:#d4f5d4'>0.205</span>|255728|224568|<span style='background-color:#d4f5d4'>-12.185</span>|5533|65|<span style='background-color:#d4f5d4'>-98.825</span>|
|streamcluster-rodinia-2.0-ft|64|17.6082|17.5942|<span style='background-color:#f8d0d0'>-0.080</span>|259718|228175|<span style='background-color:#d4f5d4'>-12.145</span>|5540|65|<span style='background-color:#d4f5d4'>-98.827</span>|
|streamcluster-rodinia-2.0-ft|65|17.5962|17.6464|<span style='background-color:#d4f5d4'>0.285</span>|263795|231701|<span style='background-color:#d4f5d4'>-12.166</span>|5619|65|<span style='background-color:#d4f5d4'>-98.843</span>|
|streamcluster-rodinia-2.0-ft|66|17.5982|17.6343|<span style='background-color:#d4f5d4'>0.205</span>|267805|235270|<span style='background-color:#d4f5d4'>-12.149</span>|5808|65|<span style='background-color:#d4f5d4'>-98.881</span>|
|streamcluster-rodinia-2.0-ft|67|17.6082|17.5942|<span style='background-color:#f8d0d0'>-0.080</span>|271795|238877|<span style='background-color:#d4f5d4'>-12.111</span>|5815|65|<span style='background-color:#d4f5d4'>-98.882</span>|
|streamcluster-rodinia-2.0-ft|68|17.5962|17.6464|<span style='background-color:#d4f5d4'>0.285</span>|275872|242403|<span style='background-color:#d4f5d4'>-12.132</span>|5894|65|<span style='background-color:#d4f5d4'>-98.897</span>|
|streamcluster-rodinia-2.0-ft|69|17.5982|17.6343|<span style='background-color:#d4f5d4'>0.205</span>|279882|245972|<span style='background-color:#d4f5d4'>-12.116</span>|6083|65|<span style='background-color:#d4f5d4'>-98.931</span>|
|streamcluster-rodinia-2.0-ft|70|17.6082|17.5942|<span style='background-color:#f8d0d0'>-0.080</span>|283872|249579|<span style='background-color:#d4f5d4'>-12.080</span>|6090|65|<span style='background-color:#d4f5d4'>-98.933</span>|
|streamcluster-rodinia-2.0-ft|71|17.6504|17.6524|<span style='background-color:#d4f5d4'>0.011</span>|287834|253275|<span style='background-color:#d4f5d4'>-12.007</span>|6108|65|<span style='background-color:#d4f5d4'>-98.936</span>|
|streamcluster-rodinia-2.0-ft|72|17.5802|17.5882|<span style='background-color:#d4f5d4'>0.046</span>|291850|256611|<span style='background-color:#d4f5d4'>-12.074</span>|6165|65|<span style='background-color:#d4f5d4'>-98.946</span>|
|streamcluster-rodinia-2.0-ft|73|17.2954|17.4455|<span style='background-color:#d4f5d4'>0.868</span>|296158|260569|<span style='background-color:#d4f5d4'>-12.017</span>|6475|185|<span style='background-color:#d4f5d4'>-97.143</span>|
|streamcluster-rodinia-2.0-ft|74|17.4731|17.3128|<span style='background-color:#f8d0d0'>-0.917</span>|300582|264536|<span style='background-color:#d4f5d4'>-11.992</span>|6716|262|<span style='background-color:#d4f5d4'>-96.099</span>|
|streamcluster-rodinia-2.0-ft|75|17.5683|17.2453|<span style='background-color:#f8d0d0'>-1.839</span>|304783|268435|<span style='background-color:#d4f5d4'>-11.926</span>|7035|453|<span style='background-color:#d4f5d4'>-93.561</span>|
|streamcluster-rodinia-2.0-ft|76|17.5146|17.5942|<span style='background-color:#d4f5d4'>0.454</span>|309060|272059|<span style='background-color:#d4f5d4'>-11.972</span>|7426|549|<span style='background-color:#d4f5d4'>-92.607</span>|
|streamcluster-rodinia-2.0-ft|77|17.5623|17.5623|0.000|313395|275977|<span style='background-color:#d4f5d4'>-11.940</span>|7798|738|<span style='background-color:#d4f5d4'>-90.536</span>|
|streamcluster-rodinia-2.0-ft|78|17.5583|17.5106|<span style='background-color:#f8d0d0'>-0.272</span>|317601|279703|<span style='background-color:#d4f5d4'>-11.933</span>|8080|855|<span style='background-color:#d4f5d4'>-89.418</span>|
|streamcluster-rodinia-2.0-ft|79|17.5503|17.5543|<span style='background-color:#d4f5d4'>0.023</span>|321905|283653|<span style='background-color:#d4f5d4'>-11.883</span>|8434|1003|<span style='background-color:#d4f5d4'>-88.108</span>|
|streamcluster-rodinia-2.0-ft|80|17.5324|17.5523|<span style='background-color:#d4f5d4'>0.114</span>|326366|287656|<span style='background-color:#d4f5d4'>-11.861</span>|8735|1063|<span style='background-color:#d4f5d4'>-87.831</span>|
|streamcluster-rodinia-2.0-ft|81|17.5205|17.5324|<span style='background-color:#d4f5d4'>0.068</span>|330598|291477|<span style='background-color:#d4f5d4'>-11.833</span>|9153|1173|<span style='background-color:#d4f5d4'>-87.185</span>|
|streamcluster-rodinia-2.0-ft|82|17.5424|17.5543|<span style='background-color:#d4f5d4'>0.068</span>|334969|295423|<span style='background-color:#d4f5d4'>-11.806</span>|9522|1305|<span style='background-color:#d4f5d4'>-86.295</span>|
|streamcluster-rodinia-2.0-ft|83|17.3575|17.5962|<span style='background-color:#d4f5d4'>1.375</span>|339441|299381|<span style='background-color:#d4f5d4'>-11.802</span>|9813|1460|<span style='background-color:#d4f5d4'>-85.122</span>|
|streamcluster-rodinia-2.0-ft|84|17.5324|17.5543|<span style='background-color:#d4f5d4'>0.125</span>|343744|303311|<span style='background-color:#d4f5d4'>-11.763</span>|10160|1607|<span style='background-color:#d4f5d4'>-84.183</span>|
|streamcluster-rodinia-2.0-ft|85|17.5324|17.5523|<span style='background-color:#d4f5d4'>0.114</span>|348123|307398|<span style='background-color:#d4f5d4'>-11.698</span>|10497|1709|<span style='background-color:#d4f5d4'>-83.719</span>|
|streamcluster-rodinia-2.0-ft|86|17.5583|17.5106|<span style='background-color:#f8d0d0'>-0.272</span>|352425|311212|<span style='background-color:#d4f5d4'>-11.694</span>|10816|1893|<span style='background-color:#d4f5d4'>-82.498</span>|
|streamcluster-rodinia-2.0-ft|87|17.5603|17.5027|<span style='background-color:#f8d0d0'>-0.328</span>|356700|315053|<span style='background-color:#d4f5d4'>-11.676</span>|11160|2069|<span style='background-color:#d4f5d4'>-81.461</span>|
|streamcluster-rodinia-2.0-ft|88|17.477|17.5822|<span style='background-color:#d4f5d4'>0.602</span>|361148|318745|<span style='background-color:#d4f5d4'>-11.741</span>|11551|2142|<span style='background-color:#d4f5d4'>-81.456</span>|
|streamcluster-rodinia-2.0-ft|89|17.2993|17.5663|<span style='background-color:#d4f5d4'>1.543</span>|365670|322467|<span style='background-color:#d4f5d4'>-11.815</span>|11783|2239|<span style='background-color:#d4f5d4'>-80.998</span>|
|streamcluster-rodinia-2.0-ft|90|17.4357|17.5563|<span style='background-color:#d4f5d4'>0.692</span>|370009|326185|<span style='background-color:#d4f5d4'>-11.844</span>|12191|2381|<span style='background-color:#d4f5d4'>-80.469</span>|
|streamcluster-rodinia-2.0-ft|91|17.5942|17.5623|<span style='background-color:#f8d0d0'>-0.181</span>|374197|330136|<span style='background-color:#d4f5d4'>-11.775</span>|12563|2539|<span style='background-color:#d4f5d4'>-79.790</span>|
|streamcluster-rodinia-2.0-ft|92|17.5503|17.5643|<span style='background-color:#d4f5d4'>0.080</span>|378404|333952|<span style='background-color:#d4f5d4'>-11.747</span>|12839|2713|<span style='background-color:#d4f5d4'>-78.869</span>|
|streamcluster-rodinia-2.0-ft|93|17.5484|17.6022|<span style='background-color:#d4f5d4'>0.307</span>|382819|337740|<span style='background-color:#d4f5d4'>-11.776</span>|13258|2894|<span style='background-color:#d4f5d4'>-78.172</span>|
|streamcluster-rodinia-2.0-ft|94|17.5324|17.5047|<span style='background-color:#f8d0d0'>-0.158</span>|387220|341532|<span style='background-color:#d4f5d4'>-11.799</span>|13596|3112|<span style='background-color:#d4f5d4'>-77.111</span>|
|streamcluster-rodinia-2.0-ft|95|17.5305|17.5563|<span style='background-color:#d4f5d4'>0.147</span>|391536|345381|<span style='background-color:#d4f5d4'>-11.788</span>|13879|3240|<span style='background-color:#d4f5d4'>-76.655</span>|
|streamcluster-rodinia-2.0-ft|96|17.5663|17.5523|<span style='background-color:#f8d0d0'>-0.080</span>|395874|349145|<span style='background-color:#d4f5d4'>-11.804</span>|14298|3386|<span style='background-color:#d4f5d4'>-76.318</span>|
|streamcluster-rodinia-2.0-ft|97|17.5942|17.5623|<span style='background-color:#f8d0d0'>-0.181</span>|400062|353096|<span style='background-color:#d4f5d4'>-11.740</span>|14670|3544|<span style='background-color:#d4f5d4'>-75.842</span>|
|streamcluster-rodinia-2.0-ft|98|17.5503|17.5643|<span style='background-color:#d4f5d4'>0.080</span>|404269|356912|<span style='background-color:#d4f5d4'>-11.714</span>|14946|3718|<span style='background-color:#d4f5d4'>-75.124</span>|
|streamcluster-rodinia-2.0-ft|99|17.5484|17.6022|<span style='background-color:#d4f5d4'>0.307</span>|408684|360700|<span style='background-color:#d4f5d4'>-11.741</span>|15365|3899|<span style='background-color:#d4f5d4'>-74.624</span>|
|streamcluster-rodinia-2.0-ft|100|17.5324|17.5047|<span style='background-color:#f8d0d0'>-0.158</span>|413085|364492|<span style='background-color:#d4f5d4'>-11.763</span>|15703|4117|<span style='background-color:#d4f5d4'>-73.782</span>|
|streamcluster-rodinia-2.0-ft|101|17.4593|17.5723|<span style='background-color:#d4f5d4'>0.647</span>|417558|368372|<span style='background-color:#d4f5d4'>-11.779</span>|16107|4225|<span style='background-color:#d4f5d4'>-73.769</span>|
|streamcluster-rodinia-2.0-ft|102|17.5902|17.4711|<span style='background-color:#f8d0d0'>-0.677</span>|421782|372220|<span style='background-color:#d4f5d4'>-11.751</span>|16429|4388|<span style='background-color:#d4f5d4'>-73.291</span>|
|streamcluster-rodinia-2.0-ft|103|17.5324|17.5047|<span style='background-color:#f8d0d0'>-0.158</span>|426183|376012|<span style='background-color:#d4f5d4'>-11.772</span>|16767|4606|<span style='background-color:#d4f5d4'>-72.529</span>|
|streamcluster-rodinia-2.0-ft|104|17.4593|17.5723|<span style='background-color:#d4f5d4'>0.647</span>|430656|379892|<span style='background-color:#d4f5d4'>-11.788</span>|17171|4714|<span style='background-color:#d4f5d4'>-72.547</span>|
|streamcluster-rodinia-2.0-ft|105|17.5902|17.4711|<span style='background-color:#f8d0d0'>-0.677</span>|434880|383740|<span style='background-color:#d4f5d4'>-11.760</span>|17493|4877|<span style='background-color:#d4f5d4'>-72.120</span>|
|streamcluster-rodinia-2.0-ft|106|17.5324|17.5047|<span style='background-color:#f8d0d0'>-0.158</span>|439281|387532|<span style='background-color:#d4f5d4'>-11.780</span>|17831|5095|<span style='background-color:#d4f5d4'>-71.426</span>|
|streamcluster-rodinia-2.0-ft|107|17.4593|17.5723|<span style='background-color:#d4f5d4'>0.647</span>|443754|391412|<span style='background-color:#d4f5d4'>-11.795</span>|18235|5203|<span style='background-color:#d4f5d4'>-71.467</span>|
|streamcluster-rodinia-2.0-ft|108|17.5902|17.4711|<span style='background-color:#f8d0d0'>-0.677</span>|447978|395260|<span style='background-color:#d4f5d4'>-11.768</span>|18557|5366|<span style='background-color:#d4f5d4'>-71.084</span>|
|streamcluster-rodinia-2.0-ft|109|17.5324|17.5047|<span style='background-color:#f8d0d0'>-0.158</span>|452379|399052|<span style='background-color:#d4f5d4'>-11.788</span>|18895|5584|<span style='background-color:#d4f5d4'>-70.447</span>|
|streamcluster-rodinia-2.0-ft|110|17.4593|17.5723|<span style='background-color:#d4f5d4'>0.647</span>|456852|402932|<span style='background-color:#d4f5d4'>-11.803</span>|19299|5692|<span style='background-color:#d4f5d4'>-70.506</span>|
|streamcluster-rodinia-2.0-ft|111|17.5643|17.5503|<span style='background-color:#f8d0d0'>-0.080</span>|461158|406850|<span style='background-color:#d4f5d4'>-11.776</span>|19680|5804|<span style='background-color:#d4f5d4'>-70.508</span>|
|streamcluster-rodinia-2.0-ft|112|17.5583|17.3264|<span style='background-color:#f8d0d0'>-1.321</span>|465629|410871|<span style='background-color:#d4f5d4'>-11.760</span>|20006|5941|<span style='background-color:#d4f5d4'>-70.304</span>|
|streamcluster-rodinia-2.0-ft|113|17.3672|17.475|<span style='background-color:#d4f5d4'>0.621</span>|470210|415103|<span style='background-color:#d4f5d4'>-11.720</span>|20420|6164|<span style='background-color:#d4f5d4'>-69.814</span>|
|streamcluster-rodinia-2.0-ft|114|17.377|17.4102|<span style='background-color:#d4f5d4'>0.191</span>|474970|419268|<span style='background-color:#d4f5d4'>-11.727</span>|20960|6450|<span style='background-color:#d4f5d4'>-69.227</span>|
|streamcluster-rodinia-2.0-ft|115|17.4475|17.5225|<span style='background-color:#d4f5d4'>0.430</span>|479578|423341|<span style='background-color:#d4f5d4'>-11.726</span>|21354|6625|<span style='background-color:#d4f5d4'>-68.975</span>|
|streamcluster-rodinia-2.0-ft|116|17.4908|17.4043|<span style='background-color:#f8d0d0'>-0.495</span>|484262|427413|<span style='background-color:#d4f5d4'>-11.739</span>|21766|6904|<span style='background-color:#d4f5d4'>-68.281</span>|
|streamcluster-rodinia-2.0-ft|117|17.3867|17.418|<span style='background-color:#d4f5d4'>0.180</span>|488916|431711|<span style='background-color:#d4f5d4'>-11.700</span>|22262|7193|<span style='background-color:#d4f5d4'>-67.689</span>|
|streamcluster-rodinia-2.0-ft|118|17.4691|17.4259|<span style='background-color:#f8d0d0'>-0.247</span>|493562|436116|<span style='background-color:#d4f5d4'>-11.639</span>|22566|7460|<span style='background-color:#d4f5d4'>-66.941</span>|
|streamcluster-rodinia-2.0-ft|119|17.4278|17.4632|<span style='background-color:#d4f5d4'>0.203</span>|498230|440274|<span style='background-color:#d4f5d4'>-11.632</span>|23046|7663|<span style='background-color:#d4f5d4'>-66.749</span>|
|streamcluster-rodinia-2.0-ft|120|17.3264|17.42|<span style='background-color:#d4f5d4'>0.540</span>|502934|444429|<span style='background-color:#d4f5d4'>-11.633</span>|23596|7943|<span style='background-color:#d4f5d4'>-66.338</span>|
|streamcluster-rodinia-2.0-ft|121|17.4475|17.481|<span style='background-color:#d4f5d4'>0.192</span>|507639|448575|<span style='background-color:#d4f5d4'>-11.635</span>|24048|8112|<span style='background-color:#d4f5d4'>-66.267</span>|
|streamcluster-rodinia-2.0-ft|122|17.3303|17.3283|<span style='background-color:#f8d0d0'>-0.012</span>|512287|452818|<span style='background-color:#d4f5d4'>-11.609</span>|24558|8418|<span style='background-color:#d4f5d4'>-65.722</span>|
|streamcluster-rodinia-2.0-ft|123|17.4632|17.3945|<span style='background-color:#f8d0d0'>-0.393</span>|516859|456836|<span style='background-color:#d4f5d4'>-11.613</span>|24829|8713|<span style='background-color:#d4f5d4'>-64.908</span>|
|streamcluster-rodinia-2.0-ft|124|17.4396|17.5087|<span style='background-color:#d4f5d4'>0.396</span>|521496|461146|<span style='background-color:#d4f5d4'>-11.572</span>|25255|8890|<span style='background-color:#d4f5d4'>-64.799</span>|
|streamcluster-rodinia-2.0-ft|125|17.3283|17.3614|<span style='background-color:#d4f5d4'>0.191</span>|526229|465256|<span style='background-color:#d4f5d4'>-11.587</span>|25796|9171|<span style='background-color:#d4f5d4'>-64.448</span>|
|streamcluster-rodinia-2.0-ft|126|17.4318|17.4475|<span style='background-color:#d4f5d4'>0.090</span>|530811|469281|<span style='background-color:#d4f5d4'>-11.592</span>|26156|9433|<span style='background-color:#d4f5d4'>-63.936</span>|
|streamcluster-rodinia-2.0-ft|127|17.3984|17.4672|<span style='background-color:#d4f5d4'>0.395</span>|535478|473385|<span style='background-color:#d4f5d4'>-11.596</span>|26438|9660|<span style='background-color:#d4f5d4'>-63.462</span>|
|streamcluster-rodinia-2.0-ft|128|17.3283|17.3342|<span style='background-color:#d4f5d4'>0.034</span>|540194|477710|<span style='background-color:#d4f5d4'>-11.567</span>|26993|9966|<span style='background-color:#d4f5d4'>-63.079</span>|
|streamcluster-rodinia-2.0-ft|129|17.4161|17.4652|<span style='background-color:#d4f5d4'>0.282</span>|544813|481857|<span style='background-color:#d4f5d4'>-11.556</span>|27304|10260|<span style='background-color:#d4f5d4'>-62.423</span>|
|streamcluster-rodinia-2.0-ft|130|17.4416|17.4988|<span style='background-color:#d4f5d4'>0.328</span>|549454|485762|<span style='background-color:#d4f5d4'>-11.592</span>|27774|10449|<span style='background-color:#d4f5d4'>-62.378</span>|

## Averages

|benchmark|ipc_gain_pct|read_change_pct|write_change_pct|
|---|---|---|---|
|backprop-rodinia-2.0-ft|<span style='background-color:#f8d0d0'>-0.004</span>|<span style='background-color:#d4f5d4'>-13.157</span>|<span style='background-color:#d4f5d4'>-82.360</span>|
|bfs-rodinia-2.0-ft|<span style='background-color:#d4f5d4'>0.037</span>|<span style='background-color:#d4f5d4'>-55.311</span>|<span style='background-color:#d4f5d4'>-100.000</span>|
|heartwall-rodinia-2.0-ft|<span style='background-color:#d4f5d4'>0.456</span>|<span style='background-color:#d4f5d4'>-13.225</span>|<span style='background-color:#d4f5d4'>-100.000</span>|
|hotspot-rodinia-2.0-ft|<span style='background-color:#f8d0d0'>-0.000</span>|<span style='background-color:#d4f5d4'>-58.553</span>|0.000|
|lud-rodinia-2.0-ft|<span style='background-color:#f8d0d0'>-0.015</span>|<span style='background-color:#d4f5d4'>-100.000</span>|0.000|
|nn-rodinia-2.0-ft|<span style='background-color:#f8d0d0'>-0.094</span>|<span style='background-color:#d4f5d4'>-36.255</span>|0.000|
|nw-rodinia-2.0-ft|0.000|0.000|0.000|
|pathfinder-rodinia-2.0-ft|<span style='background-color:#f8d0d0'>-0.018</span>|<span style='background-color:#d4f5d4'>-100.000</span>|<span style='background-color:#d4f5d4'>-100.000</span>|
|srad_v2-rodinia-2.0-ft|<span style='background-color:#d4f5d4'>0.154</span>|<span style='background-color:#d4f5d4'>-77.954</span>|<span style='background-color:#d4f5d4'>-25.332</span>|
|streamcluster-rodinia-2.0-ft|<span style='background-color:#d4f5d4'>0.055</span>|<span style='background-color:#d4f5d4'>-11.694</span>|<span style='background-color:#d4f5d4'>-94.720</span>|

## Overall Summary

- IPC geomean percent change: <b>0.057%</b>
- GLOBAL_ACC_R geomean percent change: <b>-77.481%</b>
- GLOBAL_ACC_W geomean percent change: <b>-83.148%</b>