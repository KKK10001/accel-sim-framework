# Performance Gain Report

## Per-Kernel Details (colored)

|variant|benchmark|kernel_index|ipc_base|ipc_tuned|ipc_gain_pct|read_base|read_tuned|read_change_pct|write_base|write_tuned|write_change_pct|
|---|---|---|---|---|---|---|---|---|---|---|---|
|regress_enable_mshr_l2_correlation|backprop-rodinia-2.0-ft|1|187.8954|178.8399|<span style='background-color:#f8d0d0'>-4.819</span>|10019|10631|<span style='background-color:#f8d0d0'>6.108</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|backprop-rodinia-2.0-ft|2|93.9905|111.0787|<span style='background-color:#d4f5d4'>18.181</span>|173806|133768|<span style='background-color:#d4f5d4'>-23.036</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|bfs-rodinia-2.0-ft|1|3.7301|3.7301|0.000|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|bfs-rodinia-2.0-ft|2|8.0535|8.0535|0.000|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|bfs-rodinia-2.0-ft|3|4.023|4.023|0.000|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|bfs-rodinia-2.0-ft|4|8.31|8.31|0.000|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|bfs-rodinia-2.0-ft|5|4.9393|4.9316|<span style='background-color:#f8d0d0'>-0.156</span>|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|bfs-rodinia-2.0-ft|6|8.9388|8.9324|<span style='background-color:#f8d0d0'>-0.072</span>|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|bfs-rodinia-2.0-ft|7|9.0828|9.143|<span style='background-color:#d4f5d4'>0.663</span>|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|bfs-rodinia-2.0-ft|8|11.7318|11.692|<span style='background-color:#f8d0d0'>-0.339</span>|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|bfs-rodinia-2.0-ft|9|15.9535|16.6097|<span style='background-color:#d4f5d4'>4.113</span>|16146|10971|<span style='background-color:#d4f5d4'>-32.051</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|bfs-rodinia-2.0-ft|10|13.0263|13.0286|<span style='background-color:#d4f5d4'>0.018</span>|16146|10971|<span style='background-color:#d4f5d4'>-32.051</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|bfs-rodinia-2.0-ft|11|16.2414|17.1996|<span style='background-color:#d4f5d4'>5.900</span>|40830|31287|<span style='background-color:#d4f5d4'>-23.373</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|bfs-rodinia-2.0-ft|12|8.697|8.683|<span style='background-color:#f8d0d0'>-0.161</span>|40830|31287|<span style='background-color:#d4f5d4'>-23.373</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|bfs-rodinia-2.0-ft|13|6.8452|6.8418|<span style='background-color:#f8d0d0'>-0.050</span>|40830|31287|<span style='background-color:#d4f5d4'>-23.373</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|bfs-rodinia-2.0-ft|14|8.2617|8.2556|<span style='background-color:#f8d0d0'>-0.074</span>|40830|31287|<span style='background-color:#d4f5d4'>-23.373</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|bfs-rodinia-2.0-ft|15|6.4258|6.4826|<span style='background-color:#d4f5d4'>0.884</span>|40830|31287|<span style='background-color:#d4f5d4'>-23.373</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|bfs-rodinia-2.0-ft|16|8.2475|8.2445|<span style='background-color:#f8d0d0'>-0.036</span>|40830|31287|<span style='background-color:#d4f5d4'>-23.373</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|heartwall-rodinia-2.0-ft|1|167.8718|173.7382|<span style='background-color:#d4f5d4'>3.495</span>|234|3262|<span style='background-color:#f8d0d0'>1294.017</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|hotspot-rodinia-2.0-ft|1|213.4151|212.3878|<span style='background-color:#f8d0d0'>-0.481</span>|7387|1725|<span style='background-color:#d4f5d4'>-76.648</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|hotspot-rodinia-2.0-ft|2|214.282|210.1712|<span style='background-color:#f8d0d0'>-1.918</span>|14191|2017|<span style='background-color:#d4f5d4'>-85.787</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|hotspot-rodinia-2.0-ft|3|213.9514|205.909|<span style='background-color:#f8d0d0'>-3.759</span>|21301|2207|<span style='background-color:#d4f5d4'>-89.639</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|hotspot-rodinia-2.0-ft|4|207.4492|207.9291|<span style='background-color:#d4f5d4'>0.231</span>|28305|2362|<span style='background-color:#d4f5d4'>-91.655</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|hotspot-rodinia-2.0-ft|5|207.2278|208.8777|<span style='background-color:#d4f5d4'>0.796</span>|35181|2661|<span style='background-color:#d4f5d4'>-92.436</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|hotspot-rodinia-2.0-ft|6|215.5191|214.5663|<span style='background-color:#f8d0d0'>-0.442</span>|39003|2978|<span style='background-color:#d4f5d4'>-92.365</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|hotspot-rodinia-2.0-ft|7|236.3661|218.3589|<span style='background-color:#f8d0d0'>-7.618</span>|40613|3589|<span style='background-color:#d4f5d4'>-91.163</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|lud-rodinia-2.0-ft|1|0.7827|0.7827|0.000|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|lud-rodinia-2.0-ft|2|9.6917|9.6917|0.000|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|lud-rodinia-2.0-ft|3|23.3103|23.3103|0.000|527|527|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|lud-rodinia-2.0-ft|4|0.7872|0.7872|0.000|527|527|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|lud-rodinia-2.0-ft|5|6.7866|6.7866|0.000|527|527|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|lud-rodinia-2.0-ft|6|31.5007|31.5007|0.000|562|562|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|lud-rodinia-2.0-ft|7|0.7872|0.7872|0.000|562|562|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|lud-rodinia-2.0-ft|8|3.3946|3.3946|0.000|562|562|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|lud-rodinia-2.0-ft|9|28.722|28.722|0.000|606|606|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|lud-rodinia-2.0-ft|10|1.0239|1.0239|0.000|606|606|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|nn-rodinia-2.0-ft|1|14.6027|46.0554|<span style='background-color:#d4f5d4'>215.390</span>|887317|55927|<span style='background-color:#d4f5d4'>-93.697</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|nn-rodinia-2.0-ft|2|15.1221|46.8968|<span style='background-color:#d4f5d4'>210.121</span>|1736135|119509|<span style='background-color:#d4f5d4'>-93.116</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|nn-rodinia-2.0-ft|3|15.0727|46.7871|<span style='background-color:#d4f5d4'>210.410</span>|2587382|177546|<span style='background-color:#d4f5d4'>-93.138</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|nn-rodinia-2.0-ft|4|15.1419|46.9718|<span style='background-color:#d4f5d4'>210.211</span>|3426608|241861|<span style='background-color:#d4f5d4'>-92.942</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|nw-rodinia-2.0-ft|1|0.9801|0.9801|0.000|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|nw-rodinia-2.0-ft|2|4.3275|4.3275|0.000|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|nw-rodinia-2.0-ft|3|2.1761|2.1761|0.000|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|nw-rodinia-2.0-ft|4|4.3218|4.3218|0.000|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|nw-rodinia-2.0-ft|5|4.7954|4.7954|0.000|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|nw-rodinia-2.0-ft|6|5.7391|5.7391|0.000|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|nw-rodinia-2.0-ft|7|6.6268|6.6268|0.000|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|nw-rodinia-2.0-ft|8|7.5185|7.5185|0.000|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|nw-rodinia-2.0-ft|9|6.6492|6.6492|0.000|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|nw-rodinia-2.0-ft|10|5.7525|5.7525|0.000|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|nw-rodinia-2.0-ft|11|4.8201|4.8201|0.000|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|nw-rodinia-2.0-ft|12|3.8832|3.8832|0.000|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|nw-rodinia-2.0-ft|13|2.9306|2.9306|0.000|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|nw-rodinia-2.0-ft|14|2.1867|2.1867|0.000|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|nw-rodinia-2.0-ft|15|0.9843|0.9843|0.000|0|0|0.000|0|0|0.000|
|regress_enable_mshr_l2_correlation|pathfinder-rodinia-2.0-ft|1|31.9286|32.3399|<span style='background-color:#d4f5d4'>1.288</span>|390|188|<span style='background-color:#d4f5d4'>-51.795</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|pathfinder-rodinia-2.0-ft|2|31.9912|32.376|<span style='background-color:#d4f5d4'>1.203</span>|759|391|<span style='background-color:#d4f5d4'>-48.485</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|pathfinder-rodinia-2.0-ft|3|32.6268|33.0523|<span style='background-color:#d4f5d4'>1.304</span>|1153|577|<span style='background-color:#d4f5d4'>-49.957</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|pathfinder-rodinia-2.0-ft|4|29.0842|29.3114|<span style='background-color:#d4f5d4'>0.781</span>|1458|707|<span style='background-color:#d4f5d4'>-51.509</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|srad_v2-rodinia-2.0-ft|1|184.5683|190.3024|<span style='background-color:#d4f5d4'>3.107</span>|10113|11598|<span style='background-color:#f8d0d0'>14.684</span>|3252|6132|<span style='background-color:#f8d0d0'>88.561</span>|
|regress_enable_mshr_l2_correlation|srad_v2-rodinia-2.0-ft|2|61.6733|63.6234|<span style='background-color:#d4f5d4'>3.162</span>|53356|51389|<span style='background-color:#d4f5d4'>-3.687</span>|3909|6660|<span style='background-color:#f8d0d0'>70.376</span>|
|regress_enable_mshr_l2_correlation|srad_v2-rodinia-2.0-ft|3|180.6047|192.8535|<span style='background-color:#d4f5d4'>6.782</span>|62764|57869|<span style='background-color:#d4f5d4'>-7.799</span>|4401|8276|<span style='background-color:#f8d0d0'>88.048</span>|
|regress_enable_mshr_l2_correlation|srad_v2-rodinia-2.0-ft|4|61.808|62.8953|<span style='background-color:#d4f5d4'>1.759</span>|103653|105421|<span style='background-color:#f8d0d0'>1.706</span>|4717|9264|<span style='background-color:#f8d0d0'>96.396</span>|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|1|13.7913|15.0154|<span style='background-color:#d4f5d4'>8.876</span>|9260|7050|<span style='background-color:#d4f5d4'>-23.866</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|2|14.5374|15.5462|<span style='background-color:#d4f5d4'>6.939</span>|18668|13338|<span style='background-color:#d4f5d4'>-28.552</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|3|27.1378|32.3769|<span style='background-color:#d4f5d4'>19.306</span>|28434|19405|<span style='background-color:#d4f5d4'>-31.754</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|4|14.5661|15.9779|<span style='background-color:#d4f5d4'>9.692</span>|37917|25428|<span style='background-color:#d4f5d4'>-32.938</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|5|27.7657|31.8375|<span style='background-color:#d4f5d4'>14.665</span>|47073|31548|<span style='background-color:#d4f5d4'>-32.981</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|6|14.6599|15.9911|<span style='background-color:#d4f5d4'>9.081</span>|56823|37645|<span style='background-color:#d4f5d4'>-33.750</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|7|14.6863|15.891|<span style='background-color:#d4f5d4'>8.203</span>|66197|43016|<span style='background-color:#d4f5d4'>-35.018</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|8|28.2935|33.9908|<span style='background-color:#d4f5d4'>20.136</span>|76116|49003|<span style='background-color:#d4f5d4'>-35.621</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|9|14.7157|15.922|<span style='background-color:#d4f5d4'>8.197</span>|85603|55548|<span style='background-color:#d4f5d4'>-35.110</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|10|14.7311|16.0675|<span style='background-color:#d4f5d4'>9.072</span>|95380|61600|<span style='background-color:#d4f5d4'>-35.416</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|11|27.7409|33.6655|<span style='background-color:#d4f5d4'>21.357</span>|105101|67319|<span style='background-color:#d4f5d4'>-35.948</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|12|14.7395|16.0792|<span style='background-color:#d4f5d4'>9.089</span>|115700|73684|<span style='background-color:#d4f5d4'>-36.315</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|13|28.1188|33.6728|<span style='background-color:#d4f5d4'>19.752</span>|126123|79423|<span style='background-color:#d4f5d4'>-37.027</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|14|14.6544|16.0126|<span style='background-color:#d4f5d4'>9.268</span>|136327|85073|<span style='background-color:#d4f5d4'>-37.596</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|15|14.7634|15.9878|<span style='background-color:#d4f5d4'>8.293</span>|146300|90669|<span style='background-color:#d4f5d4'>-38.025</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|16|28.2832|32.7745|<span style='background-color:#d4f5d4'>15.880</span>|156844|96388|<span style='background-color:#d4f5d4'>-38.545</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|17|14.6641|15.9796|<span style='background-color:#d4f5d4'>8.971</span>|166419|102312|<span style='background-color:#d4f5d4'>-38.521</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|18|14.7213|16.2496|<span style='background-color:#d4f5d4'>10.382</span>|177417|108525|<span style='background-color:#d4f5d4'>-38.831</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|19|28.2935|33.6509|<span style='background-color:#d4f5d4'>18.935</span>|187274|114118|<span style='background-color:#d4f5d4'>-39.064</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|20|14.7031|15.8861|<span style='background-color:#d4f5d4'>8.046</span>|197659|119743|<span style='background-color:#d4f5d4'>-39.419</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|21|14.8555|15.8942|<span style='background-color:#d4f5d4'>6.992</span>|207092|125665|<span style='background-color:#d4f5d4'>-39.319</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|22|27.9664|34.0132|<span style='background-color:#d4f5d4'>21.622</span>|217050|131693|<span style='background-color:#d4f5d4'>-39.326</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|23|14.6766|16.1496|<span style='background-color:#d4f5d4'>10.036</span>|227064|137561|<span style='background-color:#d4f5d4'>-39.418</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|24|14.8526|15.9631|<span style='background-color:#d4f5d4'>7.477</span>|236575|143162|<span style='background-color:#d4f5d4'>-39.486</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|25|27.8056|33.6509|<span style='background-color:#d4f5d4'>21.022</span>|246277|149315|<span style='background-color:#d4f5d4'>-39.371</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|26|14.678|16.0077|<span style='background-color:#d4f5d4'>9.059</span>|256121|154743|<span style='background-color:#d4f5d4'>-39.582</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|27|14.7718|16.0259|<span style='background-color:#d4f5d4'>8.490</span>|265197|160431|<span style='background-color:#d4f5d4'>-39.505</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|28|28.3194|33.6655|<span style='background-color:#d4f5d4'>18.878</span>|274912|166184|<span style='background-color:#d4f5d4'>-39.550</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|29|14.6947|16.0143|<span style='background-color:#d4f5d4'>8.980</span>|284136|172115|<span style='background-color:#d4f5d4'>-39.425</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|30|14.7577|16.1935|<span style='background-color:#d4f5d4'>9.729</span>|293661|177956|<span style='background-color:#d4f5d4'>-39.401</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|31|28.1751|32.3093|<span style='background-color:#d4f5d4'>14.673</span>|302972|183556|<span style='background-color:#d4f5d4'>-39.415</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|32|14.671|15.9532|<span style='background-color:#d4f5d4'>8.740</span>|312608|189094|<span style='background-color:#d4f5d4'>-39.511</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|33|14.7017|16.0425|<span style='background-color:#d4f5d4'>9.120</span>|322454|194717|<span style='background-color:#d4f5d4'>-39.614</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|34|28.6232|33.111|<span style='background-color:#d4f5d4'>15.679</span>|331917|201838|<span style='background-color:#d4f5d4'>-39.190</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|35|14.6933|16.1227|<span style='background-color:#d4f5d4'>9.728</span>|341756|207408|<span style='background-color:#d4f5d4'>-39.311</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|36|14.7143|16.0242|<span style='background-color:#d4f5d4'>8.902</span>|352723|213738|<span style='background-color:#d4f5d4'>-39.403</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|37|28.2626|33.4256|<span style='background-color:#d4f5d4'>18.268</span>|363231|219277|<span style='background-color:#d4f5d4'>-39.632</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|38|14.671|15.805|<span style='background-color:#d4f5d4'>7.730</span>|372817|225101|<span style='background-color:#d4f5d4'>-39.622</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|39|14.7297|16.2224|<span style='background-color:#d4f5d4'>10.134</span>|382519|231148|<span style='background-color:#d4f5d4'>-39.572</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|40|28.4496|32.4652|<span style='background-color:#d4f5d4'>14.115</span>|391541|237527|<span style='background-color:#d4f5d4'>-39.335</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|41|14.769|16.0691|<span style='background-color:#d4f5d4'>8.803</span>|401088|243167|<span style='background-color:#d4f5d4'>-39.373</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|42|28.2316|33.3177|<span style='background-color:#d4f5d4'>18.016</span>|411778|248840|<span style='background-color:#d4f5d4'>-39.569</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|43|14.6891|15.9106|<span style='background-color:#d4f5d4'>8.316</span>|421151|255006|<span style='background-color:#d4f5d4'>-39.450</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|44|14.7171|15.9516|<span style='background-color:#d4f5d4'>8.388</span>|430655|260647|<span style='background-color:#d4f5d4'>-39.477</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|45|28.5861|33.469|<span style='background-color:#d4f5d4'>17.081</span>|439886|266421|<span style='background-color:#d4f5d4'>-39.434</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|46|14.6877|15.9466|<span style='background-color:#d4f5d4'>8.571</span>|449708|271917|<span style='background-color:#d4f5d4'>-39.535</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|47|14.7311|15.945|<span style='background-color:#d4f5d4'>8.240</span>|459467|277554|<span style='background-color:#d4f5d4'>-39.592</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|48|28.5756|32.3498|<span style='background-color:#d4f5d4'>13.208</span>|469320|283410|<span style='background-color:#d4f5d4'>-39.613</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|49|14.6613|15.8893|<span style='background-color:#d4f5d4'>8.376</span>|479370|289313|<span style='background-color:#d4f5d4'>-39.647</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|50|14.827|15.9614|<span style='background-color:#d4f5d4'>7.651</span>|489032|294766|<span style='background-color:#d4f5d4'>-39.725</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|51|28.1495|33.1465|<span style='background-color:#d4f5d4'>17.752</span>|498962|300266|<span style='background-color:#d4f5d4'>-39.822</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|52|14.6891|15.805|<span style='background-color:#d4f5d4'>7.597</span>|508363|306051|<span style='background-color:#d4f5d4'>-39.797</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|53|14.6947|16.1851|<span style='background-color:#d4f5d4'>10.142</span>|518075|311682|<span style='background-color:#d4f5d4'>-39.838</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|54|28.2162|32.7884|<span style='background-color:#d4f5d4'>16.204</span>|527557|317274|<span style='background-color:#d4f5d4'>-39.860</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|55|14.8142|15.9499|<span style='background-color:#d4f5d4'>7.666</span>|537259|323444|<span style='background-color:#d4f5d4'>-39.797</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|56|14.7409|15.9253|<span style='background-color:#d4f5d4'>8.035</span>|548149|329165|<span style='background-color:#d4f5d4'>-39.950</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|57|28.2419|33.2533|<span style='background-color:#d4f5d4'>17.745</span>|558734|334754|<span style='background-color:#d4f5d4'>-40.087</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|58|14.7648|16.1564|<span style='background-color:#d4f5d4'>9.425</span>|568212|340632|<span style='background-color:#d4f5d4'>-40.052</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|59|14.7465|16.1952|<span style='background-color:#d4f5d4'>9.824</span>|578621|346657|<span style='background-color:#d4f5d4'>-40.089</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|60|28.1751|16.0575|<span style='background-color:#f8d0d0'>-43.008</span>|588769|352372|<span style='background-color:#d4f5d4'>-40.151</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|61|14.6961|32.9209|<span style='background-color:#d4f5d4'>124.011</span>|599416|358508|<span style='background-color:#d4f5d4'>-40.190</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|62|14.7185|16.1227|<span style='background-color:#d4f5d4'>9.540</span>|609582|364516|<span style='background-color:#d4f5d4'>-40.202</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|63|28.639|33.5706|<span style='background-color:#d4f5d4'>17.220</span>|619132|370110|<span style='background-color:#d4f5d4'>-40.221</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|64|14.6849|16.2037|<span style='background-color:#d4f5d4'>10.343</span>|629453|376061|<span style='background-color:#d4f5d4'>-40.256</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|65|14.7902|16.0641|<span style='background-color:#d4f5d4'>8.613</span>|639205|381877|<span style='background-color:#d4f5d4'>-40.258</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|66|28.4914|32.8371|<span style='background-color:#d4f5d4'>15.253</span>|648263|388381|<span style='background-color:#d4f5d4'>-40.089</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|67|14.6766|16.1513|<span style='background-color:#d4f5d4'>10.048</span>|658213|394008|<span style='background-color:#d4f5d4'>-40.140</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|68|14.7325|15.9829|<span style='background-color:#d4f5d4'>8.487</span>|668586|400035|<span style='background-color:#d4f5d4'>-40.167</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|69|28.2059|32.4856|<span style='background-color:#d4f5d4'>15.173</span>|678142|405894|<span style='background-color:#d4f5d4'>-40.146</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|70|14.6891|15.8552|<span style='background-color:#d4f5d4'>7.939</span>|687883|411960|<span style='background-color:#d4f5d4'>-40.112</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|71|14.7003|16.0992|<span style='background-color:#d4f5d4'>9.516</span>|698220|417976|<span style='background-color:#d4f5d4'>-40.137</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|72|14.6488|32.8092|<span style='background-color:#d4f5d4'>123.972</span>|708951|423968|<span style='background-color:#d4f5d4'>-40.198</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|73|14.6433|15.8714|<span style='background-color:#d4f5d4'>8.387</span>|718259|429988|<span style='background-color:#d4f5d4'>-40.135</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|74|27.8557|31.6358|<span style='background-color:#d4f5d4'>13.570</span>|727852|435880|<span style='background-color:#d4f5d4'>-40.114</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|75|14.6502|15.7008|<span style='background-color:#d4f5d4'>7.171</span>|737961|442121|<span style='background-color:#d4f5d4'>-40.089</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|76|28.2162|33.3824|<span style='background-color:#d4f5d4'>18.309</span>|747309|447925|<span style='background-color:#d4f5d4'>-40.062</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|77|14.7521|16.0475|<span style='background-color:#d4f5d4'>8.781</span>|757275|453810|<span style='background-color:#d4f5d4'>-40.073</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|78|27.9311|32.7745|<span style='background-color:#d4f5d4'>17.341</span>|767584|459854|<span style='background-color:#d4f5d4'>-40.091</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|79|14.7059|15.9155|<span style='background-color:#d4f5d4'>8.225</span>|777058|465832|<span style='background-color:#d4f5d4'>-40.052</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|80|28.0984|33.3752|<span style='background-color:#d4f5d4'>18.780</span>|786917|472199|<span style='background-color:#d4f5d4'>-39.994</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|81|14.7003|16.1009|<span style='background-color:#d4f5d4'>9.528</span>|798119|478518|<span style='background-color:#d4f5d4'>-40.044</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|82|27.8958|34.0881|<span style='background-color:#d4f5d4'>22.198</span>|807715|484918|<span style='background-color:#d4f5d4'>-39.964</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|83|14.864|16.0143|<span style='background-color:#d4f5d4'>7.739</span>|817347|490832|<span style='background-color:#d4f5d4'>-39.948</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|84|28.129|32.2353|<span style='background-color:#d4f5d4'>14.598</span>|827343|496620|<span style='background-color:#d4f5d4'>-39.974</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|85|14.7339|15.9516|<span style='background-color:#d4f5d4'>8.265</span>|838275|502894|<span style='background-color:#d4f5d4'>-40.008</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|86|28.2316|33.368|<span style='background-color:#d4f5d4'>18.194</span>|848497|508816|<span style='background-color:#d4f5d4'>-40.033</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|87|14.7143|15.8325|<span style='background-color:#d4f5d4'>7.599</span>|859016|514966|<span style='background-color:#d4f5d4'>-40.052</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|88|27.6962|33.7462|<span style='background-color:#d4f5d4'>21.844</span>|869008|521363|<span style='background-color:#d4f5d4'>-40.005</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|89|14.8726|15.8698|<span style='background-color:#d4f5d4'>6.705</span>|878361|527255|<span style='background-color:#d4f5d4'>-39.973</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|90|28.3557|34.0506|<span style='background-color:#d4f5d4'>20.084</span>|887429|533435|<span style='background-color:#d4f5d4'>-39.890</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|91|14.7521|15.8926|<span style='background-color:#d4f5d4'>7.731</span>|898067|539319|<span style='background-color:#d4f5d4'>-39.947</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|92|28.1905|32.8719|<span style='background-color:#d4f5d4'>16.606</span>|908387|545136|<span style='background-color:#d4f5d4'>-39.989</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|93|14.7521|16.0375|<span style='background-color:#d4f5d4'>8.713</span>|918132|551167|<span style='background-color:#d4f5d4'>-39.969</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|94|27.8757|32.7676|<span style='background-color:#d4f5d4'>17.549</span>|928855|557583|<span style='background-color:#d4f5d4'>-39.971</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|95|14.8157|15.8975|<span style='background-color:#d4f5d4'>7.302</span>|938329|563736|<span style='background-color:#d4f5d4'>-39.921</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|96|28.0933|33.9609|<span style='background-color:#d4f5d4'>20.886</span>|948228|570156|<span style='background-color:#d4f5d4'>-39.871</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|97|14.7549|16.0325|<span style='background-color:#d4f5d4'>8.659</span>|958576|576464|<span style='background-color:#d4f5d4'>-39.862</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|98|28.278|33.1252|<span style='background-color:#d4f5d4'>17.141</span>|969173|582359|<span style='background-color:#d4f5d4'>-39.912</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|99|14.6308|15.9829|<span style='background-color:#d4f5d4'>9.241</span>|980855|588654|<span style='background-color:#d4f5d4'>-39.986</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|100|28.4548|34.1633|<span style='background-color:#d4f5d4'>20.062</span>|990177|594927|<span style='background-color:#d4f5d4'>-39.917</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|101|14.635|16.0425|<span style='background-color:#d4f5d4'>9.617</span>|1001329|600818|<span style='background-color:#d4f5d4'>-39.998</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|102|14.7535|33.2247|<span style='background-color:#d4f5d4'>125.199</span>|1011205|606602|<span style='background-color:#d4f5d4'>-40.012</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|103|28.3505|15.8861|<span style='background-color:#f8d0d0'>-43.965</span>|1020894|612978|<span style='background-color:#d4f5d4'>-39.957</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|104|14.6933|32.5676|<span style='background-color:#d4f5d4'>121.649</span>|1030563|619044|<span style='background-color:#d4f5d4'>-39.931</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|105|28.0882|15.8373|<span style='background-color:#f8d0d0'>-43.616</span>|1040423|624963|<span style='background-color:#d4f5d4'>-39.932</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|106|14.7017|32.5814|<span style='background-color:#d4f5d4'>121.617</span>|1051228|631095|<span style='background-color:#d4f5d4'>-39.966</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|107|28.1239|16.0575|<span style='background-color:#f8d0d0'>-42.904</span>|1061087|637042|<span style='background-color:#d4f5d4'>-39.963</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|108|14.7563|33.5706|<span style='background-color:#d4f5d4'>127.500</span>|1070909|642855|<span style='background-color:#d4f5d4'>-39.971</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|109|28.0475|16.0242|<span style='background-color:#f8d0d0'>-42.868</span>|1080439|648754|<span style='background-color:#d4f5d4'>-39.955</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|110|14.6919|33.3034|<span style='background-color:#d4f5d4'>126.679</span>|1090101|654883|<span style='background-color:#d4f5d4'>-39.925</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|111|28.078|16.0842|<span style='background-color:#f8d0d0'>-42.716</span>|1099649|660854|<span style='background-color:#d4f5d4'>-39.903</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|112|14.7045|33.1465|<span style='background-color:#d4f5d4'>125.417</span>|1109261|666940|<span style='background-color:#d4f5d4'>-39.875</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|113|28.1956|16.0442|<span style='background-color:#f8d0d0'>-43.097</span>|1118451|673132|<span style='background-color:#d4f5d4'>-39.816</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|114|14.6156|15.9598|<span style='background-color:#d4f5d4'>9.197</span>|1127686|679334|<span style='background-color:#d4f5d4'>-39.759</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|115|14.4424|15.8991|<span style='background-color:#d4f5d4'>10.086</span>|1139007|685581|<span style='background-color:#d4f5d4'>-39.809</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|116|14.6571|16.0641|<span style='background-color:#d4f5d4'>9.599</span>|1149089|691680|<span style='background-color:#d4f5d4'>-39.806</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|117|14.6267|15.9237|<span style='background-color:#d4f5d4'>8.867</span>|1160142|697675|<span style='background-color:#d4f5d4'>-39.863</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|118|14.6336|16.1935|<span style='background-color:#d4f5d4'>10.660</span>|1170523|704384|<span style='background-color:#d4f5d4'>-39.823</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|119|14.6391|15.9664|<span style='background-color:#d4f5d4'>9.067</span>|1180873|710536|<span style='background-color:#d4f5d4'>-39.830</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|120|14.6225|15.7953|<span style='background-color:#d4f5d4'>8.021</span>|1190698|717120|<span style='background-color:#d4f5d4'>-39.773</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|121|14.7507|16.0641|<span style='background-color:#d4f5d4'>8.904</span>|1200083|723342|<span style='background-color:#d4f5d4'>-39.726</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|122|14.6405|15.8471|<span style='background-color:#d4f5d4'>8.242</span>|1209573|729898|<span style='background-color:#d4f5d4'>-39.657</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|123|14.7381|15.9253|<span style='background-color:#d4f5d4'>8.055</span>|1219225|736012|<span style='background-color:#d4f5d4'>-39.633</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|124|14.7634|16.0792|<span style='background-color:#d4f5d4'>8.913</span>|1228566|742169|<span style='background-color:#d4f5d4'>-39.591</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|125|14.6211|15.9746|<span style='background-color:#d4f5d4'>9.257</span>|1240222|748399|<span style='background-color:#d4f5d4'>-39.656</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|126|14.6794|15.9171|<span style='background-color:#d4f5d4'>8.432</span>|1249807|754496|<span style='background-color:#d4f5d4'>-39.631</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|127|14.7563|16.1969|<span style='background-color:#d4f5d4'>9.763</span>|1259350|761334|<span style='background-color:#d4f5d4'>-39.545</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|128|14.6599|15.8975|<span style='background-color:#d4f5d4'>8.442</span>|1269313|767593|<span style='background-color:#d4f5d4'>-39.527</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|129|14.7437|16.011|<span style='background-color:#d4f5d4'>8.596</span>|1278562|773739|<span style='background-color:#d4f5d4'>-39.484</span>|0|0|0.000|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|130|14.6752|15.9812|<span style='background-color:#d4f5d4'>8.899</span>|1289798|780152|<span style='background-color:#d4f5d4'>-39.514</span>|0|0|0.000|

## Averages

|variant|benchmark|ipc_gain_pct|read_change_pct|write_change_pct|
|---|---|---|---|---|
|regress_enable_mshr_l2_correlation|backprop-rodinia-2.0-ft|<span style='background-color:#d4f5d4'>6.059</span>|<span style='background-color:#d4f5d4'>-9.631</span>|0.000|
|regress_enable_mshr_l2_correlation|bfs-rodinia-2.0-ft|<span style='background-color:#d4f5d4'>0.654</span>|<span style='background-color:#d4f5d4'>-13.845</span>|0.000|
|regress_enable_mshr_l2_correlation|heartwall-rodinia-2.0-ft|<span style='background-color:#d4f5d4'>3.495</span>|<span style='background-color:#f8d0d0'>1294.017</span>|0.000|
|regress_enable_mshr_l2_correlation|hotspot-rodinia-2.0-ft|<span style='background-color:#f8d0d0'>-1.923</span>|<span style='background-color:#d4f5d4'>-89.440</span>|0.000|
|regress_enable_mshr_l2_correlation|lud-rodinia-2.0-ft|0.000|0.000|0.000|
|regress_enable_mshr_l2_correlation|nn-rodinia-2.0-ft|<span style='background-color:#d4f5d4'>211.525</span>|<span style='background-color:#d4f5d4'>-93.229</span>|0.000|
|regress_enable_mshr_l2_correlation|nw-rodinia-2.0-ft|0.000|0.000|0.000|
|regress_enable_mshr_l2_correlation|pathfinder-rodinia-2.0-ft|<span style='background-color:#d4f5d4'>1.144</span>|<span style='background-color:#d4f5d4'>-50.454</span>|0.000|
|regress_enable_mshr_l2_correlation|srad_v2-rodinia-2.0-ft|<span style='background-color:#d4f5d4'>3.686</span>|<span style='background-color:#f8d0d0'>0.883</span>|<span style='background-color:#f8d0d0'>85.595</span>|
|regress_enable_mshr_l2_correlation|streamcluster-rodinia-2.0-ft|<span style='background-color:#d4f5d4'>12.318</span>|<span style='background-color:#d4f5d4'>-39.145</span>|0.000|

## Overall Summary

### regress_enable_mshr_l2_correlation

- IPC geomean percent change: <b>14.801%</b>
- L2_BW geomean percent change: <b>-19.594%</b>
- L2_total_cache_accesses geomean percent change: <b>-29.249%</b>
- L2_GLOBAL_ACC_W_TOTAL_ACCESS geomean percent change: <b>NA%</b>
- MISS_QUEUE_FULL geomean percent change: <b>-72.838%</b>
- MSHR_MERGE_ENTRY_FAIL geomean percent change: <b>inf%</b>
- MSHR_ENTRY_FAIL geomean percent change: <b>inf%</b>
- LINE_ALLOC_FAIL geomean percent change: <b>90.605%</b>