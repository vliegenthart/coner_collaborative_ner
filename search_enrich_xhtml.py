# @author Daniel Vliegenthart

from html.parser import HTMLParser
import argparse
import re
from utility_methods import intersect
from process_methods import read_entity_set, read_xhtml, process_sentences, create_terms_info
from class_definitions import Entity, PDFTerm, PDFWord

# Can also do it the other way around! Go through term set and search each term
# in the entire XHTML/TSV/CSV. For multi word, search in sentence, then lookup in the
# words after that sentence. Enrich & create TSV/CSV with Term info that way.
# Use Term class or no??
# Words: Any special characters except for 'space' and '-'
# Changed Term to Entity!!!!!!!: Every word in the entity_set.txt is considered 1 entity. 


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

  VES = []

  # TODO:
  # Create separate config file for more beautiful setup

  # ##################### #
  #      ENRICH XHMTL     #
  # ##################### #

  entity_set = read_entity_set(f"data/entity_set/{pdf_name}_set_0.txt")
  xhtml_soup = read_xhtml(f"../PDFNLT/pdfanalyzer/xhtml/{pdf_name}.xhtml")
  sent_list, sent_obj, error_sents = process_sentences(f"../PDFNLT/pdfanalyzer/text/{pdf_name}.sent.tsv")
  
  term_info_list = create_terms_info(entity_set, sent_list, sent_obj)

if __name__=='__main__':
    
    main()


# ################################ #
#      FIND TERMS IDs for XHTML    #
# ################################ #






