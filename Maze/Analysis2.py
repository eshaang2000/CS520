import Grid2

s = 0
b = 0
su = []
# for i in range(11):
#     su.append([])
print(su)
for j in range(11):
    s=0
    b=0
    while((s+b) != 10):
        ans = Grid2.test(float(j)/10) #float(j)/10
        if ans == 10:
            s+=1
        if ans == -1:
            b+=1
        if ans == 3:
            continue
        else:
            continue
    print("success "+str(s))
    print(str(b))
    su.append([s, b])

print(su)

# for 1a [[736, 264], [556, 444], [375, 625], [316, 684], [181, 819], [162, 838], [95, 905], [75, 925], [59, 941], [42, 958], [37, 963]]

# for 1b [[913, 87], [706, 294], [451, 549], [353, 647], [241, 759], [172, 828], [134, 866], [70, 930], [68, 932], [46, 954], [52, 948]]