import numpy as np
#cv2 used to transform the image and identify the different element we need for the puzzle
import cv2
#puzzle_solver only use for the test section at the end
from puzzle_solver import TD_puzzle_solver

#function to convert an image to an edged version.
def TD_img2edges(img):
	img = cv2.cvtColor(np.array(img),cv2.COLOR_RGB2GRAY)
	blurred = cv2.GaussianBlur(img,(5,5),0)
	edged = cv2.Canny(blurred,50,200,255)
	return edged

### Find the digit in the game screen
## function that take a digit and a gamescreen and output a list with all occurence of the digit
def digit_finder(digit,gamescreen):
	# read of pattern to find in grayscale + edge detection
	digit_template = cv2.imread(str(digit)+'.png')
	dt_blurred = cv2.GaussianBlur(digit_template,(5,5),0)
	dt_edged = cv2.Canny(dt_blurred,50,200,255)
	# pattern recognition in game screen
	res = cv2.matchTemplate(gamescreen,dt_edged,cv2.TM_CCOEFF_NORMED)
	threshold = 0.80
	loc = np.where(res>=threshold)
	# Storage of each number value and location in a list of tuples
	numbers_found_local = []
	for pt in zip(*loc[::-1]):
		numbers_found_local.append((digit,pt[1],pt[0]))	
	return numbers_found_local



def TD_circle_location(img):
	#transform of the image in edged form
	edged = TD_img2edges(img)

	### Find the circle in the game screen and set them in a given order
	# function that automatically find circle with some parameters (I only change min/max)
	circles = cv2.HoughCircles(edged,cv2.HOUGH_GRADIENT,0.9,120, param1=50, param2 = 30, minRadius = 45, maxRadius = 50)
	# Rounding for ease of use and hopefully to allow equality for X / y positions (raw values were sometime slightly different)
		# the hope of the line above was not good, but I see no reason to remove this line now. 
	circles_rounded = np.uint16(np.around(circles))
	# creation of a dictionary to store the positional data for ordered circles
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
	# there is a need for a better system than match exact value to avoid pixel bug, using bounds to fix it
	xaxis_1bound = xaxis_sorted[0] + 50
	xaxis_2bound = xaxis_sorted[-1] - 50
	yaxis_1bound = yaxis_sorted[0] + 50
	yaxis_2bound = yaxis_sorted[-1] - 50
	# Loop through the circles to find their order based on ordered sets and store their position based on their new ordered name
	for i in circles_rounded[0,:]:
		if i[1] < yaxis_1bound:
			yordervalue = 0
		elif  yaxis_1bound < i[1] < yaxis_2bound:
			yordervalue = 3
		elif yaxis_2bound < i[1]:
			yordervalue = 6
		
		if i[0] < xaxis_1bound:
			xordervalue = 0
		elif  xaxis_1bound < i[0] < xaxis_2bound:
			xordervalue = 1
		elif xaxis_2bound < i[0]:
			xordervalue = 2

		order = yordervalue + xordervalue
		circle_pos['C'+str(order)] = (i[1], i[0], i[2])
	# output the dictionary with hopefuly C0 - C8 with x,y and radius
	return circle_pos

def TD_circle_content(img,circle_pos):
	#transform of the image in edged form
	edged = TD_img2edges(img)

	## Storage of each number value and location in an ordered list of tuples
	numbers_found = []
	# Loop through all digits to retrieve all information from gamescreen
	for digit in range(0,10):
		numbers_found += digit_finder(digit,edged)
	# Sorting based on the x axis, to make sure that two digits numbers are always in correct order (if "37" is in a digit, the 3 must be found in the list before the 7 otherwise the program might read it as "73")
	numbers_found.sort(key=lambda tup: tup[2])



	### Find the full number inside every circle
	# Dictionary variable to store each digit found (xaxis no longer needed because number_found has been order beforehand)
	circle_content = {}
	# Loop through all the C0 - C8
	for circle in circle_pos:
		circle_content[circle]=[]
		# highligh the limit cardinal point of the circle
		circle_ystart = circle_pos[circle][0] - circle_pos[circle][2]
		circle_yend = circle_pos[circle][0] + circle_pos[circle][2]
		circle_xstart = circle_pos[circle][1] - circle_pos[circle][2]
		circle_xend = circle_pos[circle][1] + circle_pos[circle][2]
		# loop through all the digit found in the gamescreen, if the digit is within the 4 cardinal point of the circle, it is added to the circle content list
		for number, ypos, xpos in numbers_found:
			if circle_ystart<ypos<circle_yend and circle_xstart<xpos<circle_xend:
				circle_content[circle].append(number)

	#section to transform the content list of each circle into an int (eg: [8,4] ==> 84)
	circle_number = {}
	for circle in circle_content:
		# empty circle (whitch should never happen) is assign a 0 value
		if len(circle_content[circle]) == 0:
			circle_number[circle] = 0
		elif len(circle_content[circle]) == 1:
			circle_number[circle] = circle_content[circle][0]
		# the more than 2 digit case is not handeled, should review if I try to do the Three Digits
		elif len(circle_content[circle]) == 2:
			fullnumber = int(str(circle_content[circle][0]) + str(circle_content[circle][1]))
			circle_number[circle] = fullnumber
	#output a dictionary with C0 - C8 and their respective value 
	return circle_number


#test section with still image
if __name__ == '__main__':
	img = cv2.imread('Jbxg_P.png',cv2.IMREAD_COLOR)
	circle_pos = TD_circle_location(img)
	circle_number = TD_circle_content(img,circle_pos)

	
	print(circle_pos)
	print(circle_number)
	print(TD_puzzle_solver(circle_number))
