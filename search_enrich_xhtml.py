from html.parser import HTMLParser
import argparse
import re
from utility_methods import intersect
from process_methods import read_term_set, read_xhtml, process_sentences
from class_definitions import Term

# @author Daniel Vliegenthart

# Can also do it the other way around! Go through term set and search each term
# in the entire XHTML/TSV/CSV. For multi word, search in sentence, then lookup in the
# words after that sentence. Enrich & create TSV/CSV with Term info that way.
# Use Term class or no??
# Words: Any special characters except for 'space' and '-'

def main():

  # ################### #
  #      SETUP ARGS     #
  # ################### #

  # TODO:
  # For multi-file input support check PDFNLT main.py

  parser = argparse.ArgumentParser(description='Annotate xhtml file with term set')
  parser.add_argument('pdf_name', metavar='PDF Name', type=str,
                     help='name of pdf and xhtml file to be annotated')

  args = parser.parse_args()
  pdf_name = args.pdf_name

  # ####################### #
  #      INIT VARIABLES     #
  # ####################### #

  # TODO:
  # Create separate config file for more beautiful setup

  max_term_words = 3
  multi_term_list = []
  term_information_list = []
  tag_attrs = { 'class': '', 'id': '', 'data-bdr': '', 'data-ftype': '', 'data-space': ''}
  VES = []
  word_split_pattern = r'([` \t\=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?])'
  error_sents = []

  # ##################### #
  #      ENRICH XHMTL     #
  # ##################### #

  term_set = read_term_set(f"data/term_set/{pdf_name}_set_0.txt")
  xhtml_soup = read_xhtml(f"../PDFNLT/pdfanalyzer/xhtml/{pdf_name}.xhtml")
  sent_list, sent_obj = process_sentences(f"../PDFNLT/pdfanalyzer/text/{pdf_name}.sent.tsv")
  
if __name__=='__main__':
    
    main()


# ################################ #
#      FIND TERMS IDs for XHTML    #
# ################################ #

for term in term_set:
  for sent in sent_list:
    if term in sent['text']:

        # print(len(word_array), len(word_ids))
        # print(word_array, "\n", sent['text'])

        # ERROR HANDLNG!
        # quit()
      # print(sent['sent_id'], ": ", sent['text'])

      # print(sent['sent_id'], ": ", term)
      # i=2

# Add term IDs for term set!!









