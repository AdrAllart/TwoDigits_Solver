#pyautogui used for screenshot + clicks
import pyautogui
#screen_analysis contains the functions to retrive location of each circle + the value inside each
import screen_analysis
#puzzle_solver find 2 groups of number with the same total, solving the puzzle (+ the int to bin function)
import puzzle_solver

# set a pause period between each action that pyautogui is taking to not overwhelm the game
pyautogui.PAUSE = 0.5
# get a screenshot of the screen where the game is showing
img = pyautogui.screenshot()
# retrieval of the pixel location of each circle on the screen in circle_loc
circle_loc = screen_analysis.TD_circle_location(img)
# retrieval of the value inside of each circle
circle_values = screen_analysis.TD_circle_content(img,circle_loc)
# retrieval of the 2 groups that are the solution to the puzzle
group1, group2 = puzzle_solver.TD_puzzle_solver(circle_values)
# changing the format of the answer from int to binary (should be done in the return of TD_puzzle_Solver directly)
group1_bin = puzzle_solver.TD_bin(group1)
group2_bin = puzzle_solver.TD_bin(group2)

#loop to iterate over each circle of group 1
for i,value in enumerate(group1_bin):
	# if there is a 1 in the binary version of the group, we want to click the circle once to put the circle in the first group
	if value == 1:
		pyautogui.click(circle_loc['C'+str(i)][1],circle_loc['C'+str(i)][0])
#loop to iterate over each circle of group 2
for i, value in enumerate(group2_bin):
	# if there is a 1 in the binary version of the group, we want to click the circle twice to put the circle in the first group
	if value == 1:
		pyautogui.click(circle_loc['C'+str(i)][1],circle_loc['C'+str(i)][0])
		pyautogui.click(circle_loc['C'+str(i)][1],circle_loc['C'+str(i)][0])
