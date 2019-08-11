import numpy as np
import cv2

# read of game screen in grayscale + edge detection
img = cv2.imread('Jbxg_P.png',cv2.IMREAD_GRAYSCALE)
blurred = cv2.GaussianBlur(img,(5,5),0)
edged = cv2.Canny(blurred,50,200,255)

### Find the digit in the game screen
# read of pattern to find in grayscale + edge detection (example with 9)
template = cv2.imread('9.png')
t_blurred = cv2.GaussianBlur(template,(5,5),0)
t_edged = cv2.Canny(t_blurred,50,200,255)
#storage of pattern size
w, h = t_edged.shape[::-1]
# pattern recognition in game screen
res = cv2.matchTemplate(edged,t_edged,cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where(res>=threshold)
print(loc)
# Storage of each number value and location in a list of tuples
numbers_found = []
for pt in zip(*loc[::-1]):
	numbers_found.append((9,pt[1],pt[0]))
# Sorting based on the x axis, to make sure that two digits numbers are always in correct order
numbers_found.sort(key=lambda tup: tup[2])
print (numbers_found)

# rectangle around pattern found (testing purposes)

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



### Find the full number inside every circle
# Dictionary variable to store each digit found (xaxis no longer needed because number_found has been order beforehand)
circle_content = {}
for circle in circle_pos:
	circle_content[circle]=[]
	print(circle, ' - ', circle_pos[circle][0])
	circle_ystart = circle_pos[circle][0] - circle_pos[circle][2]
	circle_yend = circle_pos[circle][0] + circle_pos[circle][2]
	circle_xstart = circle_pos[circle][1] - circle_pos[circle][2]
	circle_xend = circle_pos[circle][1] + circle_pos[circle][2]

	for number, ypos, xpos in numbers_found:
		if circle_ystart<ypos<circle_yend and circle_xstart<xpos<circle_xend:
			circle_content[circle].append(number)

print (circle_content)

circle_number = {}
for circle in circle_content:
	if len(circle_content[circle]) == 0:
		circle_number[circle] = 0
	elif len(circle_content[circle]) == 1:
		circle_number[circle] = circle_content[circle][0]
	elif len(circle_content[circle]) == 2:
		fullnumber = int(str(circle_content[circle][0]) + str(circle_content[circle][1]))
		circle_number[circle] = fullnumber

print(circle_number)
# Image outputting for testing purposes
'''
#cv2.imshow('t_image',t_edged)
cv2.imshow('image',edged)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
