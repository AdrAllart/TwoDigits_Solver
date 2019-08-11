import numpy as np
## function that convert and int into 9 bits
def TD_bin (number):
	return [int(i) for i in list('{0:09b}'.format(number))]

## function that return true if two int does not use the sames bits in their binary form (don't use the same circle in game)
def TD_bin_comptability_checker (numb1,numb2):

	first_combi = TD_bin(numb1)
	second_combi = TD_bin(numb2)

	compatibility = True
	for i in range (0,len(first_combi)):
		if first_combi[i] + second_combi[i] ==2:
			compatibility = False
	return compatibility


def TD_puzzle_solver (puzzle_dict):
	''' 
	Function that compute all possible combination of the circle value of a game and return the first match it finds for combination with the same values that do not use the same circle.
	The function is fed a dictionnary on the form {C0:15,C1:2...}
	'''
	puzzle_dict_extract= []
	for circle_number in range(0,9):
		puzzle_dict_extract.append(puzzle_dict['C'+str(circle_number)])

	result_table = {}
	for i in range(1,256):
		puzzle_mask = TD_bin(i)
		result_table[i] = np.dot(puzzle_dict_extract,puzzle_mask)


	for key in result_table:
		result = result_table[key]
		# the winner condition was used initialy when the program outputted all the possible results to prevent duplicate results. No longer necessary
		if result != 'winner':
			for challenger in result_table:
				challenger_result = result_table[challenger]
				if  result == challenger_result and TD_bin_comptability_checker(key,challenger):
					return(key,challenger)

					#print ('winner : ', str(result), ' selection1:', TD_bin(key), 'selection2', TD_bin(challenger) )
					#print(sum(TD_bin(key))+sum(TD_bin(challenger)))
					#result_table[challenger]= 'winner'


# test section
if __name__ == '__main__':
	puzzle_numbers = {'C0':1,'C1':18,'C2':50,'C3':23,'C4':48,'C5':31,'C6':27,'C7':85,'C8':35}

	winners = TD_puzzle_solver(puzzle_numbers)

	print(winners)