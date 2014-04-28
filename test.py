json_string='{"term":"Take out the trash"}'
begin_pos=json_string.find(':')+2
end_pos=json_string.find('"',begin_pos)
str=json_string[begin_pos:end_pos]
word_list=str.split()
arr=[]
for j in range (len(word_list)):
	prefix_str=''
	for i in range (len(word_list[j])):
		prefix_str=prefix_str+word_list[j][i]
		arr.append(prefix_str)
print arr