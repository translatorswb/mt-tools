#!/usr/bin/env python
# coding: utf-8

import re
import sys
from difflib import SequenceMatcher

punkset = [ '፧', '፥', '።', '፥', '፤', '፣', '፦', '፡', '፨', '፠', 
					 '?', ',', '.', '!', '(', ')', '[', ']', ';', ':', '“', '”', 
					 '"', '’', "'", '¶', '/', '...', '>', '<', '{', '}', '—', '-' ]

def tokenize(doc):
	"""
	Splits the document into sentences using end punctuation.

	:param doc: to split
	:return: the list of sentence strings from the document
	"""
	tokens = []
	doc = ' '.join(doc.split())
	
	curr_word = ""
	for c in doc:
		if c == ' ' or c in punkset:
			if curr_word:
				tokens.append(curr_word)
				curr_word = ""
			if c in punkset:
				tokens.append(c)
		else:
			curr_word += c
	if curr_word:
		tokens.append(curr_word)            

	return tokens



#Tokenize document
doc_in = sys.argv[1]
doc_out = sys.argv[2]
with open(doc_in, 'r') as f_in, open(doc_out, 'w') as f_out:
	lines_ti = f_in.readlines()
	
	for line_ti in lines_ti:
		line_tokens = tokenize(line_ti)
		f_out.write(' '.join(line_tokens) + '\n')


