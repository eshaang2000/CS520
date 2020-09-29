import Grid

s = 0
b = 0
su = []
# for i in range(11):
#     su.append([])
print(su)
for j in range(11):
    s=0
    b=0
    while((s+b) != 100):
        ans = Grid.test(float(j)/10)
        if ans == 1:
            s+=1
        if ans == 0:
            b+=1
        if ans == 3:
            continue
    print("success "+str(s))
    print(str(b))
    su.append([s, b])

print(su)

# for 1a [[736, 264], [556, 444], [375, 625], [316, 684], [181, 819], [162, 838], [95, 905], [75, 925], [59, 941], [42, 958], [37, 963]]