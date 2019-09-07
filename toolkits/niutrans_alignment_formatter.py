import re
import sys

align_token_pattern = re.compile(' \({ [0-9|\s]*}\) ')

def giza_to_niutrans(giza_align_info):
	align_tokens = align_token_pattern.findall(giza_align_info)

	if giza_align_info.startswith("NULL"):
		skip_first = True

	align_info = ""
	src_idx = 0
	for i, t in enumerate(align_tokens):
		if skip_first and i == 0:
			continue
		t = t.replace('({', '')
		t = t.replace('})', '')
		tgt_idxs_strings = t.split()

		tgt_idxs = [int(tgt_idx) - 1 for tgt_idx in tgt_idxs_strings]

		for tgt_idx in tgt_idxs:
			align_info_token = "%i-%i"%(src_idx, tgt_idx)
			align_info += align_info_token + " "
		src_idx += 1

	return align_info

def main():
	print("hello %s"%sys.argv[1])

	giza_alignment_file = sys.argv[1]
	niutrans_alignment_file = sys.argv[2]


	with open(giza_alignment_file, 'r') as f:
		giza_alignment_file_lines = f.readlines()

	with open(niutrans_alignment_file, 'w') as outfile: 
		line_type = 0
		for i, line in enumerate(giza_alignment_file_lines):
			if line_type == 2:
				niutrans_alignment = giza_to_niutrans(line[0:-1])
				outfile.write(niutrans_alignment[0:-1])
				if not i == len(giza_alignment_file_lines) - 1:
					outfile.write("\n")

			line_type += 1
			if line_type == 3:
				line_type = 0



if __name__== "__main__":
	main()


