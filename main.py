import cv2 
from matplotlib import pyplot as plt
import Queue

img = cv2.imread('e905c759-8b85-48ec-9855-18eeb6fcb002.jpg',0)

cv2.imwrite("canny.jpg", cv2.Canny(img, 180, 200))
img2 = cv2.imread("canny.jpg")

lefti = 192
leftj = 91

righti = 377
rightj = 696 

threshold = 12

mark = dict()
rect = dict()
for i in range(lefti, righti + 1):
    for j in range(leftj, rightj + 1):
        R,G,B = img2[i,j]
        #if R <= 200 and G <= 200 and B <= 200:
        if R <= 20 and G <= 20 and B <= 20:
            continue
        if mark.has_key(i):
            mark[i][j] = (i,j)
        else:
            mark[i] = dict()
            mark[i][j] = (i,j)
        #fine prev elements to check if there is something we can merge
        for ti in range(-threshold,threshold + 1):
            for tj in range(-threshold,threshold + 1):
                curi = i + ti
                curj = j + tj
                if curi == i and curj == j:
                    continue
                if mark.has_key(curi) and mark[curi].has_key(curj):
                    mark[i][j] = mark[curi][curj]
                    break
            nowi,nowj = mark[i][j]
            if nowi != i or nowj != j:
                break

        rooti, rootj = mark[i][j]
        if rect.has_key(rooti) :
            if rect[rooti].has_key(rootj):
                mini,minj,maxi,maxj = rect[rooti][rootj]
                rect[rooti][rootj] = (min(mini,i), min(minj,j), max(maxi,i), max(maxj,j))
            else:
                rect[rooti][rootj] = (i,j,i,j)
        else:
            rect[rooti] = dict()
            rect[rooti][rootj] = (i,j,i,j)

for i in rect.keys():
    for j in rect[i].keys():
        mini,minj,maxi,maxj = rect[i][j]
        if (maxi - mini) * (maxj - minj) > 200:
            cv2.rectangle(img2, (minj,mini), (maxj,maxi), (255,0,0), 2)



cv2.imwrite("canny_x.jpg", img2)
plt.imshow(img2), plt.show()
