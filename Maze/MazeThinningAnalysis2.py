import MazeThinning

manhattanNodes = 0
thinNodes = 0

compare = []

for j in range(11):

    manhattanNodes = 0
    thinNodes = 0
    i = 0

    while (i != 1000):
        fail = (-1, -1)
        ans = MazeThinning.test2(float(j)/10)
        if ans == fail:
            continue
        else:
            manhattanNodes += ans[0]
            thinNodes += ans[1]
            i += 1

    
    
    compare.append([manhattanNodes, thinNodes])

print(compare)
