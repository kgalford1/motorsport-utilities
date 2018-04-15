# To run this program:
#
# python3 logCount.py < thermistorData.txt > brokenThermistors.txt
#
# The < redirects the file thermistorData.txt to stdin for logCount.py
# The > redirects stdout to brokenThermistors.txt


# Used for sys.stdin.
import sys

# Creates an array of 16 zeroes, 6 times.
count = [[0] * 16 for _ in range(6)]

# For each line in stdin. The reason I did it with stdin rather than just a file open is so you can either redirect
# a file into the program, or run it in terminal and copy paste in the log data.
# This demonstrates an example of the 'everything is a file'saying.
for line in sys.stdin:
	data = line.split()	# Lookup .split()
	S = int(data[0][1:])	# Works same as MATLAB.
	C = int(data[1][1])
	T = int(data[3].split('[')[0])
	
	count[C][S - 1] += T < 0	# Remember True = 1 and False = 0.

# Counters used to help output formatting.
S = 1
C = 0

# Finding only S/C combos that yielded negative values.
for channel in count:
	S = 1
	for i in channel:
		if i > 1:
			# Don't worry too much. Just a way of outputting data aligned.
			line = 'Error: S{:<4} C{:<4} -    {}'.format(S, C, i)
			print(line)			
		S += 1
	C += 1

