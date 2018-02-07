# @author Daniel Vliegenthart

# import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import re
from process_sent_tsv import find_pdf_terms_in_sent_tsv
from process_xhtml import read_xhtml, enrich_xhtml
import statistics

def main():

  # ################### #
  #      SETUP ARGS     #
  # ################### #

  # TODO:
  # For multi-file input support check PDFNLT main.py

  parser = argparse.ArgumentParser(description='Annotate xhtml file with term set')
  parser.add_argument('pdf_name', metavar='PDF Name', type=str,
                     help='name of pdf and xhtml file to be annotated')
  parser.add_argument('facet', metavar='Facet', type=str,
                     help='facet of specific domain e.g. database, method')

  args = parser.parse_args()
  pdf_name = args.pdf_name
  facet = args.facet

  # ####################### #
  #      INIT VARIABLES     #
  # ####################### #
  
  # TODO:
  # Create separate config file for more beautiful setup
  
  statistics.init()

  # ############################### #
  #      ENRICH XHTML WITH TERMS    #
  # ############################### #

  pdf_term_info_list = find_pdf_terms_in_sent_tsv(pdf_name)

  xhtml_soup = read_xhtml(f"../PDFNLT/pdfanalyzer/xhtml/{pdf_name}.xhtml")
  enrich_xhtml(pdf_term_info_list, xhtml_soup, facet, pdf_name)

  # TODO:
  # [DONE] output_pdf_terms_metadata(pdf_term_info_list)
  # More advanced statistics method, save all statistics, and print at the end of execution!!

  statistics.print_stats()

if __name__=='__main__':

  main()
