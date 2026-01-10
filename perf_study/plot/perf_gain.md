# Performance Gain Report

## Per-Kernel Details (colored)

|variant|benchmark|kernel_index|ipc_base|ipc_tuned|ipc_gain_pct|read_base|read_tuned|read_change_pct|write_base|write_tuned|write_change_pct|
|---|---|---|---|---|---|---|---|---|---|---|---|
|regress_enable_all_mshr|backprop-rodinia-2.0-ft|1|187.8954|178.8399|<span style='background-color:#f8d0d0'>-4.819</span>|10019|10631|<span style='background-color:#f8d0d0'>6.108</span>|0|0|0.000|
|regress_enable_all_mshr|backprop-rodinia-2.0-ft|2|93.9905|111.0787|<span style='background-color:#d4f5d4'>18.181</span>|173806|133768|<span style='background-color:#d4f5d4'>-23.036</span>|0|0|0.000|
|regress_enable_all_mshr|bfs-rodinia-2.0-ft|1|3.7301|3.7301|0.000|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|bfs-rodinia-2.0-ft|2|8.0535|8.0535|0.000|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|bfs-rodinia-2.0-ft|3|4.023|4.023|0.000|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|bfs-rodinia-2.0-ft|4|8.31|8.31|0.000|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|bfs-rodinia-2.0-ft|5|4.9393|4.9316|<span style='background-color:#f8d0d0'>-0.156</span>|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|bfs-rodinia-2.0-ft|6|8.9388|8.9324|<span style='background-color:#f8d0d0'>-0.072</span>|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|bfs-rodinia-2.0-ft|7|9.0828|9.143|<span style='background-color:#d4f5d4'>0.663</span>|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|bfs-rodinia-2.0-ft|8|11.7318|11.692|<span style='background-color:#f8d0d0'>-0.339</span>|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|bfs-rodinia-2.0-ft|9|15.9535|16.6097|<span style='background-color:#d4f5d4'>4.113</span>|16146|10971|<span style='background-color:#d4f5d4'>-32.051</span>|0|0|0.000|
|regress_enable_all_mshr|bfs-rodinia-2.0-ft|10|13.0263|13.0286|<span style='background-color:#d4f5d4'>0.018</span>|16146|10971|<span style='background-color:#d4f5d4'>-32.051</span>|0|0|0.000|
|regress_enable_all_mshr|bfs-rodinia-2.0-ft|11|16.2414|17.1996|<span style='background-color:#d4f5d4'>5.900</span>|40830|31287|<span style='background-color:#d4f5d4'>-23.373</span>|0|0|0.000|
|regress_enable_all_mshr|bfs-rodinia-2.0-ft|12|8.697|8.683|<span style='background-color:#f8d0d0'>-0.161</span>|40830|31287|<span style='background-color:#d4f5d4'>-23.373</span>|0|0|0.000|
|regress_enable_all_mshr|bfs-rodinia-2.0-ft|13|6.8452|6.8418|<span style='background-color:#f8d0d0'>-0.050</span>|40830|31287|<span style='background-color:#d4f5d4'>-23.373</span>|0|0|0.000|
|regress_enable_all_mshr|bfs-rodinia-2.0-ft|14|8.2617|8.2556|<span style='background-color:#f8d0d0'>-0.074</span>|40830|31287|<span style='background-color:#d4f5d4'>-23.373</span>|0|0|0.000|
|regress_enable_all_mshr|bfs-rodinia-2.0-ft|15|6.4258|6.4826|<span style='background-color:#d4f5d4'>0.884</span>|40830|31287|<span style='background-color:#d4f5d4'>-23.373</span>|0|0|0.000|
|regress_enable_all_mshr|bfs-rodinia-2.0-ft|16|8.2475|8.2445|<span style='background-color:#f8d0d0'>-0.036</span>|40830|31287|<span style='background-color:#d4f5d4'>-23.373</span>|0|0|0.000|
|regress_enable_all_mshr|heartwall-rodinia-2.0-ft|1|167.8718|173.7382|<span style='background-color:#d4f5d4'>3.495</span>|234|3262|<span style='background-color:#f8d0d0'>1294.017</span>|0|0|0.000|
|regress_enable_all_mshr|hotspot-rodinia-2.0-ft|1|213.4151|212.3878|<span style='background-color:#f8d0d0'>-0.481</span>|7387|1725|<span style='background-color:#d4f5d4'>-76.648</span>|0|0|0.000|
|regress_enable_all_mshr|hotspot-rodinia-2.0-ft|2|214.282|210.1712|<span style='background-color:#f8d0d0'>-1.918</span>|14191|2017|<span style='background-color:#d4f5d4'>-85.787</span>|0|0|0.000|
|regress_enable_all_mshr|hotspot-rodinia-2.0-ft|3|213.9514|205.909|<span style='background-color:#f8d0d0'>-3.759</span>|21301|2207|<span style='background-color:#d4f5d4'>-89.639</span>|0|0|0.000|
|regress_enable_all_mshr|hotspot-rodinia-2.0-ft|4|207.4492|207.9291|<span style='background-color:#d4f5d4'>0.231</span>|28305|2362|<span style='background-color:#d4f5d4'>-91.655</span>|0|0|0.000|
|regress_enable_all_mshr|hotspot-rodinia-2.0-ft|5|207.2278|208.8777|<span style='background-color:#d4f5d4'>0.796</span>|35181|2661|<span style='background-color:#d4f5d4'>-92.436</span>|0|0|0.000|
|regress_enable_all_mshr|hotspot-rodinia-2.0-ft|6|215.5191|214.5663|<span style='background-color:#f8d0d0'>-0.442</span>|39003|2978|<span style='background-color:#d4f5d4'>-92.365</span>|0|0|0.000|
|regress_enable_all_mshr|hotspot-rodinia-2.0-ft|7|236.3661|218.3589|<span style='background-color:#f8d0d0'>-7.618</span>|40613|3589|<span style='background-color:#d4f5d4'>-91.163</span>|0|0|0.000|
|regress_enable_all_mshr|lud-rodinia-2.0-ft|1|0.7827|0.7827|0.000|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|lud-rodinia-2.0-ft|2|9.6917|9.6917|0.000|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|lud-rodinia-2.0-ft|3|23.3103|23.3103|0.000|527|527|0.000|0|0|0.000|
|regress_enable_all_mshr|lud-rodinia-2.0-ft|4|0.7872|0.7872|0.000|527|527|0.000|0|0|0.000|
|regress_enable_all_mshr|lud-rodinia-2.0-ft|5|6.7866|6.7866|0.000|527|527|0.000|0|0|0.000|
|regress_enable_all_mshr|lud-rodinia-2.0-ft|6|31.5007|31.5007|0.000|562|562|0.000|0|0|0.000|
|regress_enable_all_mshr|lud-rodinia-2.0-ft|7|0.7872|0.7872|0.000|562|562|0.000|0|0|0.000|
|regress_enable_all_mshr|lud-rodinia-2.0-ft|8|3.3946|3.3946|0.000|562|562|0.000|0|0|0.000|
|regress_enable_all_mshr|lud-rodinia-2.0-ft|9|28.722|28.722|0.000|606|606|0.000|0|0|0.000|
|regress_enable_all_mshr|lud-rodinia-2.0-ft|10|1.0239|1.0239|0.000|606|606|0.000|0|0|0.000|
|regress_enable_all_mshr|nn-rodinia-2.0-ft|1|14.6027|46.0554|<span style='background-color:#d4f5d4'>215.390</span>|887317|55927|<span style='background-color:#d4f5d4'>-93.697</span>|0|0|0.000|
|regress_enable_all_mshr|nn-rodinia-2.0-ft|2|15.1221|46.8968|<span style='background-color:#d4f5d4'>210.121</span>|1736135|119509|<span style='background-color:#d4f5d4'>-93.116</span>|0|0|0.000|
|regress_enable_all_mshr|nn-rodinia-2.0-ft|3|15.0727|46.7871|<span style='background-color:#d4f5d4'>210.410</span>|2587382|177546|<span style='background-color:#d4f5d4'>-93.138</span>|0|0|0.000|
|regress_enable_all_mshr|nn-rodinia-2.0-ft|4|15.1419|46.9718|<span style='background-color:#d4f5d4'>210.211</span>|3426608|241861|<span style='background-color:#d4f5d4'>-92.942</span>|0|0|0.000|
|regress_enable_all_mshr|nw-rodinia-2.0-ft|1|0.9801|0.9801|0.000|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|nw-rodinia-2.0-ft|2|4.3275|4.3275|0.000|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|nw-rodinia-2.0-ft|3|2.1761|2.1761|0.000|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|nw-rodinia-2.0-ft|4|4.3218|4.3218|0.000|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|nw-rodinia-2.0-ft|5|4.7954|4.7954|0.000|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|nw-rodinia-2.0-ft|6|5.7391|5.7391|0.000|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|nw-rodinia-2.0-ft|7|6.6268|6.6268|0.000|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|nw-rodinia-2.0-ft|8|7.5185|7.5185|0.000|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|nw-rodinia-2.0-ft|9|6.6492|6.6492|0.000|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|nw-rodinia-2.0-ft|10|5.7525|5.7525|0.000|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|nw-rodinia-2.0-ft|11|4.8201|4.8201|0.000|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|nw-rodinia-2.0-ft|12|3.8832|3.8832|0.000|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|nw-rodinia-2.0-ft|13|2.9306|2.9306|0.000|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|nw-rodinia-2.0-ft|14|2.1867|2.1867|0.000|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|nw-rodinia-2.0-ft|15|0.9843|0.9843|0.000|0|0|0.000|0|0|0.000|
|regress_enable_all_mshr|pathfinder-rodinia-2.0-ft|1|31.9286|32.3399|<span style='background-color:#d4f5d4'>1.288</span>|390|188|<span style='background-color:#d4f5d4'>-51.795</span>|0|0|0.000|
|regress_enable_all_mshr|pathfinder-rodinia-2.0-ft|2|31.9912|32.376|<span style='background-color:#d4f5d4'>1.203</span>|759|391|<span style='background-color:#d4f5d4'>-48.485</span>|0|0|0.000|
|regress_enable_all_mshr|pathfinder-rodinia-2.0-ft|3|32.6268|33.0523|<span style='background-color:#d4f5d4'>1.304</span>|1153|577|<span style='background-color:#d4f5d4'>-49.957</span>|0|0|0.000|
|regress_enable_all_mshr|pathfinder-rodinia-2.0-ft|4|29.0842|29.3114|<span style='background-color:#d4f5d4'>0.781</span>|1458|707|<span style='background-color:#d4f5d4'>-51.509</span>|0|0|0.000|
|regress_enable_all_mshr|srad_v2-rodinia-2.0-ft|1|184.5683|190.3024|<span style='background-color:#d4f5d4'>3.107</span>|10113|11598|<span style='background-color:#f8d0d0'>14.684</span>|3252|6132|<span style='background-color:#f8d0d0'>88.561</span>|
|regress_enable_all_mshr|srad_v2-rodinia-2.0-ft|2|61.6733|63.6234|<span style='background-color:#d4f5d4'>3.162</span>|53356|51389|<span style='background-color:#d4f5d4'>-3.687</span>|3909|6660|<span style='background-color:#f8d0d0'>70.376</span>|
|regress_enable_all_mshr|srad_v2-rodinia-2.0-ft|3|180.6047|192.8535|<span style='background-color:#d4f5d4'>6.782</span>|62764|57869|<span style='background-color:#d4f5d4'>-7.799</span>|4401|8276|<span style='background-color:#f8d0d0'>88.048</span>|
|regress_enable_all_mshr|srad_v2-rodinia-2.0-ft|4|61.808|62.8953|<span style='background-color:#d4f5d4'>1.759</span>|103653|105421|<span style='background-color:#f8d0d0'>1.706</span>|4717|9264|<span style='background-color:#f8d0d0'>96.396</span>|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|1|13.7913|15.0154|<span style='background-color:#d4f5d4'>8.876</span>|9260|7050|<span style='background-color:#d4f5d4'>-23.866</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|2|14.5374|15.5462|<span style='background-color:#d4f5d4'>6.939</span>|18668|13338|<span style='background-color:#d4f5d4'>-28.552</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|3|27.1378|32.3769|<span style='background-color:#d4f5d4'>19.306</span>|28434|19405|<span style='background-color:#d4f5d4'>-31.754</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|4|14.5661|15.9779|<span style='background-color:#d4f5d4'>9.692</span>|37917|25428|<span style='background-color:#d4f5d4'>-32.938</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|5|27.7657|31.8375|<span style='background-color:#d4f5d4'>14.665</span>|47073|31548|<span style='background-color:#d4f5d4'>-32.981</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|6|14.6599|15.9911|<span style='background-color:#d4f5d4'>9.081</span>|56823|37645|<span style='background-color:#d4f5d4'>-33.750</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|7|14.6863|15.891|<span style='background-color:#d4f5d4'>8.203</span>|66197|43016|<span style='background-color:#d4f5d4'>-35.018</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|8|28.2935|33.9908|<span style='background-color:#d4f5d4'>20.136</span>|76116|49003|<span style='background-color:#d4f5d4'>-35.621</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|9|14.7157|15.922|<span style='background-color:#d4f5d4'>8.197</span>|85603|55548|<span style='background-color:#d4f5d4'>-35.110</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|10|14.7311|16.0675|<span style='background-color:#d4f5d4'>9.072</span>|95380|61600|<span style='background-color:#d4f5d4'>-35.416</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|11|27.7409|33.6655|<span style='background-color:#d4f5d4'>21.357</span>|105101|67319|<span style='background-color:#d4f5d4'>-35.948</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|12|14.7395|16.0792|<span style='background-color:#d4f5d4'>9.089</span>|115700|73684|<span style='background-color:#d4f5d4'>-36.315</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|13|28.1188|33.6728|<span style='background-color:#d4f5d4'>19.752</span>|126123|79423|<span style='background-color:#d4f5d4'>-37.027</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|14|14.6544|16.0126|<span style='background-color:#d4f5d4'>9.268</span>|136327|85073|<span style='background-color:#d4f5d4'>-37.596</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|15|14.7634|15.9878|<span style='background-color:#d4f5d4'>8.293</span>|146300|90669|<span style='background-color:#d4f5d4'>-38.025</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|16|28.2832|32.7745|<span style='background-color:#d4f5d4'>15.880</span>|156844|96388|<span style='background-color:#d4f5d4'>-38.545</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|17|14.6641|15.9796|<span style='background-color:#d4f5d4'>8.971</span>|166419|102312|<span style='background-color:#d4f5d4'>-38.521</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|18|14.7213|16.2496|<span style='background-color:#d4f5d4'>10.382</span>|177417|108525|<span style='background-color:#d4f5d4'>-38.831</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|19|28.2935|33.6509|<span style='background-color:#d4f5d4'>18.935</span>|187274|114118|<span style='background-color:#d4f5d4'>-39.064</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|20|14.7031|15.8861|<span style='background-color:#d4f5d4'>8.046</span>|197659|119743|<span style='background-color:#d4f5d4'>-39.419</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|21|14.8555|15.8942|<span style='background-color:#d4f5d4'>6.992</span>|207092|125665|<span style='background-color:#d4f5d4'>-39.319</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|22|27.9664|34.0132|<span style='background-color:#d4f5d4'>21.622</span>|217050|131693|<span style='background-color:#d4f5d4'>-39.326</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|23|14.6766|16.1496|<span style='background-color:#d4f5d4'>10.036</span>|227064|137561|<span style='background-color:#d4f5d4'>-39.418</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|24|14.8526|15.9631|<span style='background-color:#d4f5d4'>7.477</span>|236575|143162|<span style='background-color:#d4f5d4'>-39.486</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|25|27.8056|33.6509|<span style='background-color:#d4f5d4'>21.022</span>|246277|149315|<span style='background-color:#d4f5d4'>-39.371</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|26|14.678|16.0077|<span style='background-color:#d4f5d4'>9.059</span>|256121|154743|<span style='background-color:#d4f5d4'>-39.582</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|27|14.7718|16.0259|<span style='background-color:#d4f5d4'>8.490</span>|265197|160431|<span style='background-color:#d4f5d4'>-39.505</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|28|28.3194|33.6655|<span style='background-color:#d4f5d4'>18.878</span>|274912|166184|<span style='background-color:#d4f5d4'>-39.550</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|29|14.6947|16.0143|<span style='background-color:#d4f5d4'>8.980</span>|284136|172115|<span style='background-color:#d4f5d4'>-39.425</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|30|14.7577|16.1935|<span style='background-color:#d4f5d4'>9.729</span>|293661|177956|<span style='background-color:#d4f5d4'>-39.401</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|31|28.1751|32.3093|<span style='background-color:#d4f5d4'>14.673</span>|302972|183556|<span style='background-color:#d4f5d4'>-39.415</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|32|14.671|15.9532|<span style='background-color:#d4f5d4'>8.740</span>|312608|189094|<span style='background-color:#d4f5d4'>-39.511</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|33|14.7017|16.0425|<span style='background-color:#d4f5d4'>9.120</span>|322454|194717|<span style='background-color:#d4f5d4'>-39.614</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|34|28.6232|33.111|<span style='background-color:#d4f5d4'>15.679</span>|331917|201838|<span style='background-color:#d4f5d4'>-39.190</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|35|14.6933|16.1227|<span style='background-color:#d4f5d4'>9.728</span>|341756|207408|<span style='background-color:#d4f5d4'>-39.311</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|36|14.7143|16.0242|<span style='background-color:#d4f5d4'>8.902</span>|352723|213738|<span style='background-color:#d4f5d4'>-39.403</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|37|28.2626|33.4256|<span style='background-color:#d4f5d4'>18.268</span>|363231|219277|<span style='background-color:#d4f5d4'>-39.632</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|38|14.671|15.805|<span style='background-color:#d4f5d4'>7.730</span>|372817|225101|<span style='background-color:#d4f5d4'>-39.622</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|39|14.7297|16.2224|<span style='background-color:#d4f5d4'>10.134</span>|382519|231148|<span style='background-color:#d4f5d4'>-39.572</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|40|28.4496|32.4652|<span style='background-color:#d4f5d4'>14.115</span>|391541|237527|<span style='background-color:#d4f5d4'>-39.335</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|41|14.769|16.0691|<span style='background-color:#d4f5d4'>8.803</span>|401088|243167|<span style='background-color:#d4f5d4'>-39.373</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|42|28.2316|33.3177|<span style='background-color:#d4f5d4'>18.016</span>|411778|248840|<span style='background-color:#d4f5d4'>-39.569</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|43|14.6891|15.9106|<span style='background-color:#d4f5d4'>8.316</span>|421151|255006|<span style='background-color:#d4f5d4'>-39.450</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|44|14.7171|15.9516|<span style='background-color:#d4f5d4'>8.388</span>|430655|260647|<span style='background-color:#d4f5d4'>-39.477</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|45|28.5861|33.469|<span style='background-color:#d4f5d4'>17.081</span>|439886|266421|<span style='background-color:#d4f5d4'>-39.434</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|46|14.6877|15.9466|<span style='background-color:#d4f5d4'>8.571</span>|449708|271917|<span style='background-color:#d4f5d4'>-39.535</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|47|14.7311|15.945|<span style='background-color:#d4f5d4'>8.240</span>|459467|277554|<span style='background-color:#d4f5d4'>-39.592</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|48|28.5756|32.3498|<span style='background-color:#d4f5d4'>13.208</span>|469320|283410|<span style='background-color:#d4f5d4'>-39.613</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|49|14.6613|15.8893|<span style='background-color:#d4f5d4'>8.376</span>|479370|289313|<span style='background-color:#d4f5d4'>-39.647</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|50|14.827|15.9614|<span style='background-color:#d4f5d4'>7.651</span>|489032|294766|<span style='background-color:#d4f5d4'>-39.725</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|51|28.1495|15.8649|<span style='background-color:#f8d0d0'>-43.641</span>|498962|300717|<span style='background-color:#d4f5d4'>-39.731</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|52|14.6891|33.556|<span style='background-color:#d4f5d4'>128.441</span>|508363|306492|<span style='background-color:#d4f5d4'>-39.710</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|53|14.6947|16.0425|<span style='background-color:#d4f5d4'>9.172</span>|518075|312243|<span style='background-color:#d4f5d4'>-39.730</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|54|28.2162|32.5471|<span style='background-color:#d4f5d4'>15.349</span>|527557|317971|<span style='background-color:#d4f5d4'>-39.728</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|55|14.8142|15.9368|<span style='background-color:#d4f5d4'>7.578</span>|537259|324216|<span style='background-color:#d4f5d4'>-39.654</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|56|14.7409|15.9746|<span style='background-color:#d4f5d4'>8.369</span>|548149|330696|<span style='background-color:#d4f5d4'>-39.670</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|57|28.2419|33.6728|<span style='background-color:#d4f5d4'>19.230</span>|558734|336371|<span style='background-color:#d4f5d4'>-39.798</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|58|14.7648|15.8503|<span style='background-color:#d4f5d4'>7.352</span>|568212|342026|<span style='background-color:#d4f5d4'>-39.807</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|59|14.7465|16.0925|<span style='background-color:#d4f5d4'>9.128</span>|578621|347893|<span style='background-color:#d4f5d4'>-39.875</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|60|28.1751|32.3296|<span style='background-color:#d4f5d4'>14.745</span>|588769|353803|<span style='background-color:#d4f5d4'>-39.908</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|61|14.6961|16.1699|<span style='background-color:#d4f5d4'>10.029</span>|599416|359907|<span style='background-color:#d4f5d4'>-39.957</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|62|14.7185|16.2003|<span style='background-color:#d4f5d4'>10.068</span>|609582|366023|<span style='background-color:#d4f5d4'>-39.955</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|63|28.639|15.9417|<span style='background-color:#f8d0d0'>-44.336</span>|619132|372631|<span style='background-color:#d4f5d4'>-39.814</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|64|14.6849|33.7683|<span style='background-color:#d4f5d4'>129.953</span>|629453|378424|<span style='background-color:#d4f5d4'>-39.880</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|65|14.7902|16.0043|<span style='background-color:#d4f5d4'>8.209</span>|639205|384507|<span style='background-color:#d4f5d4'>-39.846</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|66|28.4914|33.1039|<span style='background-color:#d4f5d4'>16.189</span>|648263|390099|<span style='background-color:#d4f5d4'>-39.824</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|67|14.6766|15.9911|<span style='background-color:#d4f5d4'>8.956</span>|658213|395790|<span style='background-color:#d4f5d4'>-39.869</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|68|14.7325|16.0043|<span style='background-color:#d4f5d4'>8.633</span>|668586|401713|<span style='background-color:#d4f5d4'>-39.916</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|69|28.2059|33.4328|<span style='background-color:#d4f5d4'>18.531</span>|678142|407353|<span style='background-color:#d4f5d4'>-39.931</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|70|14.6891|15.8942|<span style='background-color:#d4f5d4'>8.204</span>|687883|412880|<span style='background-color:#d4f5d4'>-39.978</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|71|14.7003|15.9138|<span style='background-color:#d4f5d4'>8.255</span>|698220|418377|<span style='background-color:#d4f5d4'>-40.079</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|72|27.921|32.3296|<span style='background-color:#d4f5d4'>15.790</span>|707911|424104|<span style='background-color:#d4f5d4'>-40.091</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|73|14.6905|15.9614|<span style='background-color:#d4f5d4'>8.651</span>|718178|430268|<span style='background-color:#d4f5d4'>-40.089</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|74|27.5189|33.3034|<span style='background-color:#d4f5d4'>21.020</span>|727841|436623|<span style='background-color:#d4f5d4'>-40.011</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|75|14.7017|15.9204|<span style='background-color:#d4f5d4'>8.290</span>|738021|442440|<span style='background-color:#d4f5d4'>-40.050</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|76|28.1188|34.1106|<span style='background-color:#d4f5d4'>21.309</span>|749196|448574|<span style='background-color:#d4f5d4'>-40.126</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|77|14.7423|16.1193|<span style='background-color:#d4f5d4'>9.340</span>|759032|454898|<span style='background-color:#d4f5d4'>-40.069</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|78|28.078|33.5852|<span style='background-color:#d4f5d4'>19.614</span>|769166|460997|<span style='background-color:#d4f5d4'>-40.065</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|79|14.8555|16.0658|<span style='background-color:#d4f5d4'>8.147</span>|778652|467412|<span style='background-color:#d4f5d4'>-39.972</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|80|27.7409|32.8719|<span style='background-color:#d4f5d4'>18.496</span>|788305|473360|<span style='background-color:#d4f5d4'>-39.952</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|81|14.7493|15.8796|<span style='background-color:#d4f5d4'>7.663</span>|798517|479652|<span style='background-color:#d4f5d4'>-39.932</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|82|28.0933|33.8348|<span style='background-color:#d4f5d4'>20.437</span>|808279|485792|<span style='background-color:#d4f5d4'>-39.898</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|83|14.7972|15.9532|<span style='background-color:#d4f5d4'>7.812</span>|819043|492817|<span style='background-color:#d4f5d4'>-39.830</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|84|28.2935|32.9349|<span style='background-color:#d4f5d4'>16.404</span>|828633|498649|<span style='background-color:#d4f5d4'>-39.823</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|85|14.6933|16.2292|<span style='background-color:#d4f5d4'>10.453</span>|838854|504843|<span style='background-color:#d4f5d4'>-39.818</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|86|28.1546|33.1536|<span style='background-color:#d4f5d4'>17.756</span>|849196|511041|<span style='background-color:#d4f5d4'>-39.821</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|87|14.7185|16.0842|<span style='background-color:#d4f5d4'>9.279</span>|858338|517070|<span style='background-color:#d4f5d4'>-39.759</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|88|27.7508|33.1181|<span style='background-color:#d4f5d4'>19.341</span>|868197|523359|<span style='background-color:#d4f5d4'>-39.719</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|89|14.8398|16.0226|<span style='background-color:#d4f5d4'>7.970</span>|877201|529171|<span style='background-color:#d4f5d4'>-39.675</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|90|28.3039|33.0615|<span style='background-color:#d4f5d4'>16.809</span>|886590|535113|<span style='background-color:#d4f5d4'>-39.644</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|91|14.8114|15.9895|<span style='background-color:#d4f5d4'>7.954</span>|895994|541689|<span style='background-color:#d4f5d4'>-39.543</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|92|28.0984|33.4617|<span style='background-color:#d4f5d4'>19.088</span>|906586|547691|<span style='background-color:#d4f5d4'>-39.588</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|93|14.6933|15.904|<span style='background-color:#d4f5d4'>8.240</span>|917646|553610|<span style='background-color:#d4f5d4'>-39.671</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|94|28.2935|33.6362|<span style='background-color:#d4f5d4'>18.883</span>|927066|559618|<span style='background-color:#d4f5d4'>-39.636</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|95|14.7241|16.0275|<span style='background-color:#d4f5d4'>8.852</span>|937727|565652|<span style='background-color:#d4f5d4'>-39.678</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|96|27.8657|32.9489|<span style='background-color:#d4f5d4'>18.242</span>|948211|571913|<span style='background-color:#d4f5d4'>-39.685</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|97|14.7311|15.8568|<span style='background-color:#d4f5d4'>7.642</span>|958075|577922|<span style='background-color:#d4f5d4'>-39.679</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|98|27.7458|32.6984|<span style='background-color:#d4f5d4'>17.850</span>|968253|583628|<span style='background-color:#d4f5d4'>-39.724</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|99|14.7073|16.0375|<span style='background-color:#d4f5d4'>9.044</span>|978378|589901|<span style='background-color:#d4f5d4'>-39.706</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|100|28.1546|33.761|<span style='background-color:#d4f5d4'>19.913</span>|988742|595928|<span style='background-color:#d4f5d4'>-39.729</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|101|14.6655|16.1143|<span style='background-color:#d4f5d4'>9.879</span>|998568|602034|<span style='background-color:#d4f5d4'>-39.710</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|102|28.6656|33.2247|<span style='background-color:#d4f5d4'>15.904</span>|1007461|607850|<span style='background-color:#d4f5d4'>-39.665</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|103|14.7353|15.9581|<span style='background-color:#d4f5d4'>8.298</span>|1018782|613626|<span style='background-color:#d4f5d4'>-39.769</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|104|28.0221|33.2676|<span style='background-color:#d4f5d4'>18.719</span>|1028571|619733|<span style='background-color:#d4f5d4'>-39.748</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|105|14.7269|16.3182|<span style='background-color:#d4f5d4'>10.805</span>|1038650|626057|<span style='background-color:#d4f5d4'>-39.724</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|106|28.0729|33.5415|<span style='background-color:#d4f5d4'>19.480</span>|1049446|632041|<span style='background-color:#d4f5d4'>-39.774</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|107|14.6516|15.8731|<span style='background-color:#d4f5d4'>8.337</span>|1060150|637898|<span style='background-color:#d4f5d4'>-39.829</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|108|28.5914|33.1749|<span style='background-color:#d4f5d4'>16.031</span>|1069128|643618|<span style='background-color:#d4f5d4'>-39.800</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|109|14.7493|15.8373|<span style='background-color:#d4f5d4'>7.377</span>|1080251|649418|<span style='background-color:#d4f5d4'>-39.883</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|110|28.0221|33.111|<span style='background-color:#d4f5d4'>18.160</span>|1090259|655451|<span style='background-color:#d4f5d4'>-39.881</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|111|14.7831|15.9647|<span style='background-color:#d4f5d4'>7.993</span>|1099493|661313|<span style='background-color:#d4f5d4'>-39.853</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|112|27.7907|33.8496|<span style='background-color:#d4f5d4'>21.802</span>|1109215|667761|<span style='background-color:#d4f5d4'>-39.799</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|113|14.7171|16.1614|<span style='background-color:#d4f5d4'>9.814</span>|1118631|674553|<span style='background-color:#d4f5d4'>-39.698</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|114|14.6087|15.945|<span style='background-color:#d4f5d4'>9.147</span>|1129174|681077|<span style='background-color:#d4f5d4'>-39.684</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|115|14.7017|15.6042|<span style='background-color:#d4f5d4'>6.139</span>|1138917|687332|<span style='background-color:#d4f5d4'>-39.650</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|116|14.6156|15.8519|<span style='background-color:#d4f5d4'>8.459</span>|1150055|693380|<span style='background-color:#d4f5d4'>-39.709</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|117|14.6544|15.9631|<span style='background-color:#d4f5d4'>8.930</span>|1159911|699557|<span style='background-color:#d4f5d4'>-39.689</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|118|14.7297|16.0043|<span style='background-color:#d4f5d4'>8.653</span>|1171315|706033|<span style='background-color:#d4f5d4'>-39.723</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|119|14.6933|15.8341|<span style='background-color:#d4f5d4'>7.764</span>|1180935|712678|<span style='background-color:#d4f5d4'>-39.651</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|120|14.7325|15.8877|<span style='background-color:#d4f5d4'>7.841</span>|1190496|719098|<span style='background-color:#d4f5d4'>-39.597</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|121|14.7662|15.8617|<span style='background-color:#d4f5d4'>7.419</span>|1200893|725354|<span style='background-color:#d4f5d4'>-39.599</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|122|14.671|15.9598|<span style='background-color:#d4f5d4'>8.785</span>|1210537|731681|<span style='background-color:#d4f5d4'>-39.557</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|123|14.6613|16.0375|<span style='background-color:#d4f5d4'>9.387</span>|1221977|737616|<span style='background-color:#d4f5d4'>-39.637</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|124|14.7381|15.8535|<span style='background-color:#d4f5d4'>7.568</span>|1231744|744050|<span style='background-color:#d4f5d4'>-39.594</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|125|14.6766|15.8991|<span style='background-color:#d4f5d4'>8.330</span>|1241104|750331|<span style='background-color:#d4f5d4'>-39.543</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|126|14.8029|15.8519|<span style='background-color:#d4f5d4'>7.086</span>|1250831|756401|<span style='background-color:#d4f5d4'>-39.528</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|127|14.7381|16.0558|<span style='background-color:#d4f5d4'>8.941</span>|1260788|762614|<span style='background-color:#d4f5d4'>-39.513</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|128|14.6891|15.9994|<span style='background-color:#d4f5d4'>8.920</span>|1270451|769152|<span style='background-color:#d4f5d4'>-39.458</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|129|14.6752|15.8568|<span style='background-color:#d4f5d4'>8.052</span>|1280782|775880|<span style='background-color:#d4f5d4'>-39.421</span>|0|0|0.000|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|130|14.8015|16.0043|<span style='background-color:#d4f5d4'>8.126</span>|1290823|781989|<span style='background-color:#d4f5d4'>-39.419</span>|0|0|0.000|

## Averages

|variant|benchmark|ipc_gain_pct|read_change_pct|write_change_pct|
|---|---|---|---|---|
|regress_enable_all_mshr|backprop-rodinia-2.0-ft|<span style='background-color:#d4f5d4'>6.059</span>|<span style='background-color:#d4f5d4'>-9.631</span>|0.000|
|regress_enable_all_mshr|bfs-rodinia-2.0-ft|<span style='background-color:#d4f5d4'>0.654</span>|<span style='background-color:#d4f5d4'>-13.845</span>|0.000|
|regress_enable_all_mshr|heartwall-rodinia-2.0-ft|<span style='background-color:#d4f5d4'>3.495</span>|<span style='background-color:#f8d0d0'>1294.017</span>|0.000|
|regress_enable_all_mshr|hotspot-rodinia-2.0-ft|<span style='background-color:#f8d0d0'>-1.923</span>|<span style='background-color:#d4f5d4'>-89.440</span>|0.000|
|regress_enable_all_mshr|lud-rodinia-2.0-ft|0.000|0.000|0.000|
|regress_enable_all_mshr|nn-rodinia-2.0-ft|<span style='background-color:#d4f5d4'>211.525</span>|<span style='background-color:#d4f5d4'>-93.229</span>|0.000|
|regress_enable_all_mshr|nw-rodinia-2.0-ft|0.000|0.000|0.000|
|regress_enable_all_mshr|pathfinder-rodinia-2.0-ft|<span style='background-color:#d4f5d4'>1.144</span>|<span style='background-color:#d4f5d4'>-50.454</span>|0.000|
|regress_enable_all_mshr|srad_v2-rodinia-2.0-ft|<span style='background-color:#d4f5d4'>3.686</span>|<span style='background-color:#f8d0d0'>0.883</span>|<span style='background-color:#f8d0d0'>85.595</span>|
|regress_enable_all_mshr|streamcluster-rodinia-2.0-ft|<span style='background-color:#d4f5d4'>11.780</span>|<span style='background-color:#d4f5d4'>-39.040</span>|0.000|

## Overall Summary

### regress_enable_all_mshr

- IPC geomean percent change: <b>14.746%</b>
- L2_BW geomean percent change: <b>-19.632%</b>
- L2_total_cache_accesses geomean percent change: <b>-29.249%</b>
- L2_GLOBAL_ACC_W_TOTAL_ACCESS geomean percent change: <b>NA%</b>
- MISS_QUEUE_FULL geomean percent change: <b>-72.832%</b>
- MSHR_MERGE_ENTRY_FAIL geomean percent change: <b>inf%</b>
- MSHR_ENTRY_FAIL geomean percent change: <b>inf%</b>
- LINE_ALLOC_FAIL geomean percent change: <b>90.605%</b>