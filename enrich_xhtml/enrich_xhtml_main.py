# @author Daniel Vliegenthart

# import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import re
from process_methods import find_pdf_terms_in_sent_tsv
from process_xhtml import read_xhtml, enrich_xhtml
import statistics

def main():

  # ################### #
  #      SETUP ARGS     #
  # ################### #

  # TODO:
  # For multi-file input support check PDFNLT main.py

  parser = argparse.ArgumentParser(description='Annotate xhtml file with term set')

  parser.add_argument('database', metavar='Database', type=str,
                     help='database name of data collection')
  parser.add_argument('facet', metavar='Facet', type=str,
                     help='facet of specific domain e.g. database, method')
  parser.add_argument('pdf_name', metavar='PDF Name', type=str,
                     help='name of pdf and xhtml file to be annotated')

  args = parser.parse_args()
  database = args.database
  facet = args.facet
  pdf_name = args.pdf_name

  # ####################### #
  #      INIT VARIABLES     #
  # ####################### #
  
  # TODO:
  # Create separate config file for more beautiful setup

  # statistics.init()

  # ############################### #
  #      ENRICH XHTML WITH TERMS    #
  # ############################### #


  pdf_term_info_list = find_pdf_terms_in_sent_tsv(database, facet, pdf_name)

  terms_occurance = [e.text for e in pdf_term_info_list if len(e.pdf_terms) > 0]

  with open(f'data/{database}/{facet}_papers_terms_overview.csv', 'a') as outputFile:
    outputFile.write(pdf_name + "," + str(len(terms_occurance)) + "\n")

  with open(f'data/{database}/term_set/{facet}_{pdf_name}_term_set_0.txt', 'w+') as outputFile:
    for t in terms_occurance:
      outputFile.write(f'{t}\n')

  xhtml_soup = read_xhtml(f'data/{database}/xhtml/{pdf_name}.xhtml')
  enrich_xhtml(pdf_term_info_list, xhtml_soup, database, facet, pdf_name)

if __name__=='__main__':

  main()
