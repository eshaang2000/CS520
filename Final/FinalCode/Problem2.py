import matplotlib.pyplot as plt
import numpy as np

used = np.zeros((10))

action = []
for i in range(10):
    action.append("USE")
ploter = []
beta = 0.9
for i in range(10):
    ploter.append([])
# print(ploter)
for i in range(80):
    used[0] = 101 + beta * 1 * used[1]
    action[0] = "USE"
    ploter[0].append(used[0])
    for j in range(1,len(used)-1):
        if 100-10*j+beta*((1-j/10)*used[j]+(j/10)*used[j+1]) > -20000 + beta * 1 * used[0]:
            action[j] = "USE"
        else:
            action[j] = "REPLACE"
        used[j] = max(100-10*j+beta*((1-j/10)*used[j]+(j/10)*used[j+1]), -20000 + beta * 1 * used[0])
        ploter[j].append(used[j])
    used[9] = -2000 + beta * 1 * used[0]
    action[9] = "REPLACE"
    ploter[9].append(used[9])

print(used)
print(action)