# [(3, 2392), (3, 352), (3, 602), (2, 183), (2, 2604), (2, 241), (2, 242), (3, 1757), (4, 665), (2, 532), (4, 1946), (2, 2854), (3, 1157), (0, 5000), (1, 311), (4, 832), (2, 622), (2, 37), (3, 3167), (4, 4572), (0, 5000), (3, 223), (3, 1146), (3, 3047), (3, 220), (1, 90), (1, 517), (2, 499), (1, 464), (0, 5000), (3, 4214), (2, 498), (0, 5000), (3, 1004), (3, 1704), (4, 1263), (3, 3113), (1, 500), (3, 3153), (2, 2623), (2, 453), (2, 330), (1, 507), (0, 5000), (0, 5000), (3, 1160), (4, 2906), (1, 6), (3, 11), (1, 585), (3, 3502), (1, 544), (2, 401), (4, 3203), (1, 580), (3, 304), (4, 347), (1, 402), (2, 248), (2, 45), (3, 3065), (2, 114), (1, 32), (3, 49), (0, 5000), (1, 599), (3, 2305), (3, 1116), (2, 601), (2, 192), (3, 118), (2, 301), (2, 153), (2, 216), (4, 1246), (1, 536), (4, 569), (3, 1751), (1, 4529), (2, 615), (2, 11), (3, 331), (2, 264), (1, 596), (2, 185), (4, 977), (1, 4496), (3, 1130), (3, 1090), (1, 330), (4, 3017), (0, 5000), (1, 494), (3, 116), (0, 5000), (1, 229), (1, 4732), (2, 4686), (1, 9), (3, 2485)]
count = 0
ans = 0
arr = [0, 0, 0, 0]
counts = [0, 0, 0, 0]
l1 = [(4, 5338), (2, 3599), (1, 2932), (2, 155), (3, 11466), (3, 1784), (2, 1040), (4, 5272), (1, 1685), (3, 12000), (3, 2837), (1, 440), (4, 5526), (2, 257), (2, 9837), (2, 1116), (3, 847), (3, 12582), (2, 240), (4, 2229), (2, 1604), (2, 1060), (1, 766), (1, 829), (4, 197), (1, 65), (1, 1941), (1, 85), (3, 3376), (1, 701), (2, 1425), (1, 782), (2, 5962), (2, 585), (0, 22030), (3, 1115), (4, 4388), (0, 22107), (1, 1333), (4, 639), (2, 356), (3, 1734), (1, 1096), (3, 5684), (3, 162), (2, 3220), (1, 136), (2, 91), (2, 21705), (4, 7053), (1, 1761), (1, 536), (1, 982), (4, 1876), (2, 184), (2, 10738), (3, 1572), (1, 1190), (3, 46), (2, 6921), (1, 248), (3, 114), (4, 7794), (3, 1682), (4, 2813), (1, 105), (1, 1179), (3, 3725), (2, 639), (2, 1488), (2, 844), (3, 2583), (1, 885), (1, 1591), (2, 545), (2, 1192), (4, 1727), (3, 716), (3, 2569), (2, 768), (3, 8164), (2, 1087), (2, 4033), (2, 1978), (2, 46), (4, 1326), (4, 5514), (2, 63), (3, 6451), (2, 42), (3, 2915), (3, 6482), (2, 3750), (3, 10596), (4, 5321), (3, 10373), (3, 3022), (4, 18990), (3, 4508), (3, 977)]
for i in l1:
    if not i[0] == 0:
        if i[0] ==1:
            arr[0]+=i[1]
            counts[0]+=1
        if i[0] ==2:
            arr[1]+=i[1]
            counts[1]+=1
        if i[0] ==3:
            arr[2]+=i[1]
            counts[2]+=1
        if i[0] ==4:
            arr[3]+=i[1]
            counts[3]+=1
        ans+=i[1]
        count+=1

print(ans)
print(count)
print(ans/count)

print(arr)
print(counts)
for i in range(len(arr)):
    print(arr[i]/counts[i])

# Test 1
# 1188.6263736263736
# [21088, 19750, 45784, 21543]
# [22, 27, 30, 12]
# 958.5454545454545
# 731.4814814814815
# 1526.1333333333334
# 1795.25

# Test 2
# 1035.6666666666667
# [3916, 13891, 34681, 46936]
# [18, 29, 30, 19]
# 217.55555555555554
# 479.0
# 1156.0333333333333
# 2470.315789473684

# Agent 1
# 25238.917525773195
# [333075, 503194, 850465, 761441]
# [20, 27, 31, 19]
# 16653.75
# 18636.814814814814
# 27434.354838709678
# 40075.84210526316

# Agent 2
# 17751.74193548387
# [181295, 178223, 620663, 670731]
# [27, 25, 25, 16]
# 6714.62962962963
# 7128.92
# 24826.52
# 41920.6875