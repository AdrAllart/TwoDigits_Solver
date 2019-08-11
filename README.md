# TwoDigits_Solver
Working on my programming skills by writing some Python code to automatically solve puzzle from the game "Two Digits"

## Ressources used:
* [Automate the Boring Stuff with Python (ch.18)](https://automatetheboringstuff.com/chapter18/) for pyautogui basics
* [sentdex: OpenCV with Python tutorial series](https://pythonprogramming.net/loading-images-python-opencv-tutorial/) for OpenCV basics
* [Python Programmer : Circle Detection with OpenCV and Python](https://www.youtube.com/watch?v=-o9jNEbR5P8) for circle detection command

## things I learned: 
* `'{0:09b}'.format(number)'` to format int to binary
*  `np.dot()` for dot product of 2 arrays
* `if __name__ == '__main__'` for testing inside files that contains function for other files to use
* `pyautogui.PAUSE = 0.5` to add delay for pyautogui actions
* `pyautogui.screenshot()` to screenshot
* `pyautogui.click(x,y)` to click a location on the screen
* `enumerate(list)` to output index,value
* `cv2.cvtColor(np.array(img),cv2.COLOR_RGB2GRAY)` to convert image to grayscale
* `cv2.GaussianBlur(img,(5,5),0)` to blurr image
* `cv2.Canny(blurred,50,200,255)` to output edges of image (preferably after a blurr)
* `cv2.imread('file.png')` to load an image from a file
* `cv2.matchTemplate(fullimg,sampleIMGtoFind,cv2.TM_CCOEFF_NORMED)`|`threshold = 0.80`|`loc = np.where(res>=threshold)`  to look for an image inside another


* `cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,0.9,120, param1=50, param2 = 30, minRadius = 45, maxRadius = 50)` to find circles location in img
* `circles_rounded = np.uint16(np.around(circles))` round array of float
* `lowlimit < value < highlimit` for double condition 
* `List_of_tuples.sort(key=lambda tup: tup[2])` to sort a list of tuple on a given "column"

## things to go deeper in:
* numpy functionnality
* lambda functions
* opencv functionnality
* 'for pt in zip(*loc[::-1])'

## improvements for the future:
* loop through multiple games
* find the solution with the least amound of clicks
* find the solution with the maximum amount of circles
* create own puzzles
* do same functionnality for Three Digits
* do GUI to click during gameplay as an helper
* Find solutions without looking at content of the circles (prob super long to test a lot of possibility)
* Reset board based on colors
* grab only the game window
* clean the GitHub with subfolder
