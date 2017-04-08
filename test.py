
q_value = {}
with open("q_value") as f:
	for line in f:
		pair = line.split(":")
		q_value[eval(pair[0])] = eval(pair[1])
print q_value