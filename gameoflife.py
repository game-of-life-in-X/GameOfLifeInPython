import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import os

def checkState(x, y):
    neighbourCount = np.sum(grid[x - 1:x + 2, y - 1:y + 2])- grid[x, y]
    
    if grid[x, y] == 1:
        if neighbourCount < 2 or neighbourCount > 3:
            newGrid[x, y] = 0
    elif grid[x, y] == 0:
        if neighbourCount == 3:
            newGrid[x, y] = 1
            
def doTick():
    global grid

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            checkState(i, j)

    grid = np.copy(newGrid)

modelpath = str(input("Enter the name of the model to use...\n"))

try:
    model = np.loadtxt(os.getcwd()+"\\models\\"+modelpath+"\\model", delimiter = ",")
    
    decorate = open(os.getcwd()+"\\models\\"+modelpath+"\\decorate.txt", "r")
    decoratelump = decorate.readlines()
    grid = np.zeros((int(decoratelump[3]), int(decoratelump[4])))
    grid[1:model.shape[0]+1, 1:model.shape[1]+1] = model
    newGrid = np.copy(grid)
    fig = plt.figure()
    fig.suptitle(decoratelump[0], fontsize=20)
except:
    grid = np.zeros((2, 17))
    model = np.array([[0, 0, 0, 0,
                       0, 0, 0, 0,
                       0, 0, 0, 0,
                       0, 0, 0, 0]])
    grid[1:model.shape[0]+1, 1:model.shape[1]+1] = model
    newGrid = np.copy(grid)
    fig = plt.figure()
    fig.suptitle("Error: Failed to load model", fontsize=20)
    decoratelump=[0,0,0,0,0,False]

fig.canvas.set_window_title("Conway's Game of Life")
plt.axis("off")
frames = []

for i in range(int(decoratelump[1])):
    frames.append((plt.imshow(grid, cmap="binary"),))
    doTick()

output = animation.ArtistAnimation(fig, frames, interval=int(decoratelump[2]), blit=True)

if decoratelump[5]=="True":
    output.save(os.getcwd()+"\\output\\"+modelpath+".gif")