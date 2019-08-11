import numpy as np
import cv2
from matplotlib import pyplot as plt

# read of game screen in grayscale + edge detection
img = cv2.imread('Jbxg_P.png',cv2.IMREAD_GRAYSCALE)
blurred = cv2.GaussianBlur(img,(5,5),0)
edged = cv2.Canny(blurred,50,200,255)

### Find the digit in the game screen
# read of pattern to find in grayscale + edge detection (example with 9)
template = cv2.imread('nine.png')
t_blurred = cv2.GaussianBlur(template,(5,5),0)
t_edged = cv2.Canny(t_blurred,50,200,255)

#storage of pattern size
w, h = t_edged.shape[::-1]
# pattern recognition in game screen
res = cv2.matchTemplate(edged,t_edged,cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where(res>=threshold)
# rectangle around pattern found (testing purposes)
print(loc)
for pt in zip(*loc[::-1]):
	cv2.rectangle(edged,pt,(pt[0]+w,pt[1]+h), (255,255,255),2)



### Find the circle in the game screen and set them in a given order
# function that automatically find cricle with some parameters (I only change min/max)
circles = cv2.HoughCircles(edged,cv2.HOUGH_GRADIENT,0.9,120, param1=50, param2 = 30, minRadius = 45, maxRadius = 50)
# Rounding for ease of use and hopefully to allow equality for X / y positions (raw values were sometime slightly different)
circles_rounded = np.uint16(np.around(circles))
# creation of a dictionary to store the positional data for ordered cicles
circle_pos= {}
# Creation of set to store the possible X and y position for the circle centers
xaxis = set()
yaxis = set()
# Loop through the circles to store the actual X and y position found in the sets
for i in circles_rounded[0,:]:
	xaxis.add(i[0])
	yaxis.add(i[1]) 
# Sorting of the sets to be used to give an order to the circles
xaxis_sorted = sorted(xaxis)
yaxis_sorted = sorted(yaxis)
# Loop through the circles to find their order based on ordered sets and store their position based on their new ordered name
for i in circles_rounded[0,:]:
	order = yaxis_sorted.index(i[1])*3 + xaxis_sorted.index(i[0])
	circle_pos['C'+str(order)] = (i[1], i[0], i[2])

	


# drawing of the circles for testing purposes
	cv2.circle(edged,(i[0],i[1]), 3, (255,255,255),5)
	cv2.circle(edged,(i[0],i[1]), 50, (255,255,255),5)


# Image outputting for testing purposes

#cv2.imshow('t_image',t_edged)
cv2.imshow('image',edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

