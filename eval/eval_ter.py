import pyter
import sys

#Script arguments
REFERENCE_PATH = sys.argv[1]
HYPOTHESIS_PATH = sys.argv[2]

ref_sents = []
hyp_sents = []
with open(REFERENCE_PATH) as ref, open(HYPOTHESIS_PATH) as hyp:
    for line_ref, line_hyp in zip(ref, hyp):
        ref_sents.append(line_ref.strip())
        hyp_sents.append(line_hyp.strip())

total_ter = 0

for ref, hyp in zip(ref_sents, hyp_sents):
	ter = pyter.ter(hyp.split(), ref.split())
	total_ter += ter
     

print("TER: %6.2f %%"%(total_ter / len(ref_sents) * 100))

