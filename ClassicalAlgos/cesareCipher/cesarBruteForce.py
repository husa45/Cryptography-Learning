

string=input("")
for i in range(0,26):
	result=""
	for char in string:
		result+=chr(((ord(char)-65)+i)%26 +65)
	print(result)
	
