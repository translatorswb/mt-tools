#!/usr/bin/env python
# coding: utf-8

from optparse import OptionParser
from bs4 import BeautifulSoup
import re
import os
import sys

def clean_sent(text):
    text = text.replace("\n", '')
    text = text.replace("&#10;", '')
    text = text.replace("\r", '')
    text = text.replace("\t", ' ')
    
    tag_cleaner = re.compile('<.*?>')
    clean_text = re.sub(tag_cleaner, '', text)
    return clean_text



def get_doc_lang_tags(parsed_xml_content, src_lang_tags, tgt_lang_tags):
    segments = parsed_xml_content.findAll("tuv")
    try:
        seg0_tag = segments[0]['xml:lang']
        seg1_tag = segments[1]['xml:lang']
    except:
        return "", ""
    
    
    if seg0_tag == seg1_tag:
        print("\tFirst two segments have the same language tag")
        return "", ""

    if seg0_tag in src_lang_tags and seg1_tag in tgt_lang_tags:
        doc_src_tag = segments[0]['xml:lang']
        doc_tgt_tag = segments[1]['xml:lang']
        return doc_src_tag, doc_tgt_tag
    elif seg1_tag in src_lang_tags and seg0_tag in tgt_lang_tags:
        doc_src_tag = segments[1]['xml:lang']
        doc_tgt_tag = segments[0]['xml:lang']
        return doc_src_tag, doc_tgt_tag
    
    #Something's wrong
    if seg0_tag not in src_lang_tags and seg0_tag not in tgt_lang_tags:
        print("\tUnrecognized language tag", seg0_tag)
    if seg1_tag not in src_lang_tags and seg1_tag not in tgt_lang_tags:
        print("\tUnrecognized language tag", seg1_tag)
    
    return "", ""


def main(options):

    input_path = options.input_path
    src_lang_tags = options.src_lang_tags
    tgt_lang_tags = options.tgt_lang_tags
    src_output_path = options.src_output_path
    tgt_output_path = options.tgt_output_path

    if not input_path:
        print("Specify input path with TMX files")
        sys.exit()

    if os.path.isdir(input_path):
        tmx_paths = [os.path.join(input_path, i) for i in os.listdir(input_path) if i.endswith('.tmx')]
    elif os.path.splitext(input_path)[1] == '.tmx':
        tmx_paths = [input_path]
    else:
        print("Input path needs to be a directory or a TMX file")
        sys.exit()

    if not src_lang_tags:
        print("src_lang_tags cannot be empty (-s)")
        sys.exit()

    if not tgt_lang_tags:
        print("tgt_lang_tags cannot be empty (-t)")
        sys.exit()

    if not src_output_path:
        print("Specify output path for source sentences (-o)")
        sys.exit()

    if not tgt_output_path:
        print("Specify output path for target sentences (-g)")
        sys.exit()
        
    print("%i files"%len(tmx_paths))

    print("Source tags:", src_lang_tags)
    print("Target tags:", tgt_lang_tags)

    src_sents = []
    tgt_sents = []
    no_processed_docs = 0

    for tmx_path in tmx_paths:
        print("Processing", os.path.basename(tmx_path))
        
        doc_src_sents = []
        doc_tgt_sents = []
        doc_problems = 0
        with open(tmx_path) as f:
            content = f.read()
            
            soup = BeautifulSoup(content, features="lxml")
            
            doc_src_tag, doc_tgt_tag = get_doc_lang_tags(soup, src_lang_tags, tgt_lang_tags)
            if not doc_src_tag or not doc_tgt_tag:
                print("\tCouldn't get language tags from document", os.path.basename(tmx_path))
                continue

            skip_file = False
            segments = soup.findAll("tu")
            for segment in segments:
                try:
                    src_text = segment.find("tuv", {"xml:lang": doc_src_tag}).seg.text
                    tgt_text = segment.find("tuv", {"xml:lang": doc_tgt_tag}).seg.text

                    doc_src_sents.append(clean_sent(src_text))
                    doc_tgt_sents.append(clean_sent(tgt_text))
                except Exception as e:
                    print("\tProblem at segment", segment['tuid'])
                    doc_problems += 1

            if skip_file:
                print("\tProblem in file ", tmx_path)
                continue

            if not len(doc_src_sents) == len(doc_tgt_sents):
                print("\t# sentences don't match in file ", tmx_path)
                continue
                
            print("\tExtracted %i segments"%len(doc_src_sents), end="")
            if doc_problems:
                print("(Found %i problems)"%doc_problems)
            else:
                print("")
                
            src_sents.extend(doc_src_sents)
            tgt_sents.extend(doc_tgt_sents)
            
            no_processed_docs += 1
            
    print("\nProcessed %i documents. %i segments in total"%(no_processed_docs, len(src_sents)))


    with open(src_output_path, 'w') as f_src, open(tgt_output_path, 'w') as f_tgt:
        for s, t in zip(src_sents, tgt_sents):
            f_src.write(s + "\n")
            f_tgt.write(t + "\n") 


if __name__ == "__main__":
    usage = "usage: %prog [-s infile] [option]"
    parser = OptionParser(usage=usage)
    parser.add_option("-i", "--input", dest="input_path", default=None, help="input TMX or directory with TMX files", type="string")
    parser.add_option("-s", "--src_tags", dest="src_lang_tags", default=[], help="list of source language tags", type="string", action='append')
    parser.add_option("-t", "--tgt_tags", dest="tgt_lang_tags", default=[], help="list of source language tags", type="string", action='append')
    parser.add_option("-o", "--out_src", dest="src_output_path", default=None, help="Source output path", type="string")
    parser.add_option("-g", "--out_tgt", dest="tgt_output_path", default=None, help="Target output path", type="string")

    (options, args) = parser.parse_args()
    main(options)

