from rouge import FilesRouge
import sys

def prepare_results(p, r, f):
    return '\t{}:\t{}: {:5.2f}\t{}: {:5.2f}\t{}: {:5.2f}'.format(metric, 'P', 100.0 * p, 'R', 100.0 * r, 'F1', 100.0 * f)


#Script arguments
REFERENCE_PATH = sys.argv[1]
HYPOTHESIS_PATH = sys.argv[2]


files_rouge = FilesRouge(HYPOTHESIS_PATH, REFERENCE_PATH)

scores = files_rouge.get_scores(avg=True)

for metric, results in sorted(scores.items(), key=lambda x: x[0]):
	print(prepare_results(results['p'], results['r'], results['f']))
	print()

#print(scores)