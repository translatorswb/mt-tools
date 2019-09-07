import sys
import os

src_filepath = sys.argv[1]
tgt_filepath = sys.argv[2]
out_filepath = sys.argv[3]
no_lines = int(sys.argv[4])

file_src = open(src_filepath,"r") 
file_tgt = open(tgt_filepath,"r") 
file_out = open(out_filepath,"w") 

count = 0
for line_src, line_tgt in zip(file_src, file_tgt):
	file_out.write(line_src)
	file_out.write("\n")
	file_out.write(line_tgt)
	count += 1
	if count == no_lines:
		break

