'''
argument 1 - source file with samples each line 
argument 2 - target file with samples each line 
'''

import sys
import os
from math import floor
import random
import numpy as np

DATASET_NAME = 'twb1'
OUTPUT_DIR = '/Users/alp/Documents/TWB/play/tigrinya/smt-data/set-twb1'

TEST_SET_SIZE = 500
DEV_SET_SIZE = 0

SRC_LANG = 'ti'
TGT_LANG = 'en'

LOWER_TGT = False
LOWER_SRC = False

MAX_TOKENS = 100
FILTER = True
CHECK_DUPLICATION_IN_SET = 1 #0 - SRC, 1 - TGT, -1 - don't check 

all_src_filepath = sys.argv[1]
all_tgt_filepath = sys.argv[2]

def shuffle_parallel_lists(list_of_lists):
	list_of_arrays = [np.array(l) for l in list_of_lists]
	inds = list(range(0, len(list_of_arrays[0])))
	random.shuffle(inds)
	return [list(l[inds]) for l in list_of_arrays]

def file_len(fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	return i + 1

def write_to_file(collection, fname):
	with open(fname, 'w') as f:
		for element in collection:
			f.write(element)

#Duplication checking
def pick_unique_testset(allset_src, allset_tgt, testsetsize, check_duplication_in=-1):
	testset_src = []
	testset_tgt = []
	grabbed = []
	for i in range(len(allset_src)):
		found_duplicate = False

		if not check_duplication_in == -1:
			if check_duplication_in == 0:
				s = allset_src[i]
				check_in = allset_src[0:i] + allset_src[i+1:]
			else:
				s = allset_tgt[i]
				check_in = allset_tgt[0:i] + allset_tgt[i+1:]
			
			for x in check_in:
				if s == x:
					found_duplicate = True
					break

		if not found_duplicate:
			testset_src.append(allset_src[i])
			testset_tgt.append(allset_tgt[i])
			grabbed.append(i)

			if len(grabbed) == testsetsize:
				break
				
	restset_src = [s for i, s in enumerate(allset_src) if i not in grabbed]
	restset_tgt = [s for i, s in enumerate(allset_tgt) if i not in grabbed]

	return testset_src, testset_tgt, restset_src, restset_tgt


all_file_src = open(all_src_filepath,"r") 
all_file_tgt = open(all_tgt_filepath,"r") 

all_samples_src = []
all_samples_tgt = []

for line_src, line_tgt in zip(all_file_src, all_file_tgt):
	if FILTER:
		if len(line_src.split(" ")) <= MAX_TOKENS and len(line_tgt.split(" ")) <= MAX_TOKENS:
			all_samples_src.append(line_src)
			all_samples_tgt.append(line_tgt)
	else:
		all_samples_src.append(line_src)
		all_samples_tgt.append(line_tgt)

if LOWER_SRC:
	all_samples_src = [line.lower() for line in all_samples_src]

if LOWER_TGT:
	all_samples_tgt = [line.lower() for line in all_samples_tgt]


samples_src, samples_tgt = shuffle_parallel_lists([all_samples_src, all_samples_tgt])

total_len = len(samples_src)
dev_len = DEV_SET_SIZE
desired_test_len = TEST_SET_SIZE


#first pick dev set
dev_samples_src = samples_src[0:dev_len]
dev_samples_tgt = samples_tgt[0:dev_len]

#reduce sample set to the remaining sents
samples_src = samples_src[dev_len:]
samples_tgt = samples_tgt[dev_len:]

#then pick test and train set
test_samples_src, test_samples_tgt, train_samples_src, train_samples_tgt = pick_unique_testset(samples_src, samples_tgt, desired_test_len, CHECK_DUPLICATION_IN_SET)

test_len = len(test_samples_src)
train_len = len(train_samples_src)

print('total: ', total_len)
print('train: ', train_len)
print('test:', test_len)
print('dev:', dev_len)

train_src_filepath = os.path.join(OUTPUT_DIR, DATASET_NAME + '.train.' + SRC_LANG)
train_tgt_filepath = os.path.join(OUTPUT_DIR, DATASET_NAME + '.train.' + TGT_LANG)
test_src_filepath = os.path.join(OUTPUT_DIR, DATASET_NAME + '.test.' + SRC_LANG)
test_tgt_filepath = os.path.join(OUTPUT_DIR, DATASET_NAME + '.test.' + TGT_LANG)
dev_src_filepath = os.path.join(OUTPUT_DIR, DATASET_NAME + '.dev.' + SRC_LANG)
dev_tgt_filepath = os.path.join(OUTPUT_DIR, DATASET_NAME + '.dev.' + TGT_LANG)

if train_len > 0:
	write_to_file(train_samples_src, train_src_filepath)
	write_to_file(train_samples_tgt, train_tgt_filepath)
if test_len > 0:
	write_to_file(test_samples_src, test_src_filepath)
	write_to_file(test_samples_tgt, test_tgt_filepath)
if dev_len > 0:
	write_to_file(dev_samples_src, dev_src_filepath)
	write_to_file(dev_samples_tgt, dev_tgt_filepath)



