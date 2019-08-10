import numpy as np

def TD_bin (number):
	return [int(i) for i in list('{0:09b}'.format(number))]
def TD_bin_comptability_checker (numb1,numb2):

	first_combi = TD_bin(numb1)
	second_combi = TD_bin(numb2)

	compatibility = True
	for i in range (0,len(first_combi)):
		if first_combi[i] + second_combi[i] ==2:
			compatibility = False
	return compatibility

def TD_puzzle_solver (puzzle_tuple):

	result_table = {}
	for i in range(1,256):
		puzzle_mask = TD_bin(i)
		result_table[i] = np.dot(puzzle_numbers,puzzle_mask)


	for key in result_table:
		result = result_table[key]
		if result != 'winner':
			for challenger in result_table:
				challenger_result = result_table[challenger]
				if  result == challenger_result and TD_bin_comptability_checker(key,challenger):
					return(key,challenger)

					#print ('winner : ', str(result), ' selection1:', TD_bin(key), 'selection2', TD_bin(challenger) )
					#print(sum(TD_bin(key))+sum(TD_bin(challenger)))
					#result_table[challenger]= 'winner'


if __name__ == '__main__':
	puzzle_numbers = (92,38,78,97,52,60,41,75,57)

	winners = TD_puzzle_solver(puzzle_numbers)

	print(winners)