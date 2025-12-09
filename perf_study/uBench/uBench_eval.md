# L1D
|用例|实测值|config/预期行为|
|-|-|-|
|l1_lat</br>(orig)|23.9961|20|
|l1_wr_miss_then_hit</br>(modified based on l1_lat)|Total_core_cache_stats_breakdown</br>[GLOBAL_ACC_W][HIT] = 14336|l1_lat</br>Total_core_cache_stats_breakdown[GLOBAL_ACC_W][HIT] = 6144</br></br>l1_wr_miss_then_hit</br>理论上应该符合下面的推论：</br>第一部分：第一次写array的时候，行为与l1_lat的完全一致，应该有6144次hit</br>此阶段，每4次wr中的后3次是hit，因此可以直接推断得到总writes=(6144*4/3)=8192</br></br>第二部分：用例构造了对上述已经构建完成的array的重复写入，此时每次都应该hit，即此时应该有8192次hits</br></br>综上，l1_hit_miss用例的Total_core_cache_stats_breakdown[GLOBAL_ACC_W][HIT] = (6144+8192) = 14336|
|l1_rd_miss</br>(modified based on l1_lat)|*.o中的记录</br>Total_core_cache_stats_breakdown[GLOBAL_ACC_R][TOTAL_ACCESS] = 513</br><font color=red>Total_core_cache_stats_breakdown[GLOBAL_ACC_R][MISS] = 16</font></br><font color=red>Total_core_cache_stats_breakdown[GLOBAL_ACC_R][SECTOR_MISS] = 48</font></br>Total_core_cache_stats_breakdown[GLOBAL_ACC_W][TOTAL_ACCESS] = 8195</br></br>trace.out中捕捉"L1D READ_REQUEST SECTOR_MISS"或者"L1D READ_REQUEST MISS"得到了总共<font color=red>64</font>条记录，与.o中的结论一致|一开始显存中有posArray，但是L1D中是没有对应的line的。</br>总共REPEAT_TIMES=256，256次连续读取，每次读取8B，每一行有128B (4 Sectors)，总共读取256*8/128=16行 。每行开头第一个Sector属于MISS、剩余3个Sector属于SECTOR_MISS。综上，[GLOBAL_ACC_R]应该出现16次MISS、48次SECTOR_MISS|

