import sys
from nltk.translate.chrf_score import corpus_chrf

#Script arguments
REFERENCE_PATH = sys.argv[1]
HYPOTHESIS_PATH = sys.argv[2]

ref_sents = []
hyp_sents = []
with open(REFERENCE_PATH) as ref, open(HYPOTHESIS_PATH) as hyp:
    for line_ref, line_hyp in zip(ref, hyp):
        ref_sents.append(line_ref.strip())
        hyp_sents.append(line_hyp.strip())
     
chrf = corpus_chrf(ref_sents, hyp_sents)

print("CHRF: %6.2f %%"%(chrf * 100))