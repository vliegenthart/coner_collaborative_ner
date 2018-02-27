# @author Daniel Vliegenthart

# Enable imports from modules in parent directory
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from process_methods import read_entity_set, process_sentences, create_terms_info, extend_terms_info
from class_definitions import Entity, PDFTerm, PDFWord

# Can also do it the other way around! Go through term set and search each term
# in the entire XHTML/TSV/CSV. For multi word, search in sentence, then lookup in the
# words after that sentence. Enrich & create TSV/CSV with Term info that way.
# Use Term class or no??
# Words: Any special characters except for 'space' and '-'
# Changed Term to Entity!!!!!!!: Every word in the entity_set.txt is considered 1 entity. 


# Find Entities with associated pdf_terms and pdf_words in the {pdf_name}.sent.tsv file
def find_pdf_terms_in_sent_tsv(pdf_name, xhtml_soup):

  # ############################ #
  #      FIND TERMS FOR XHTML    #
  # ############################ #

  # print("Analysing & processing sentences...")

  entity_set = read_entity_set(f"data/term_set/model_1_term_set_0.txt")
  sent_list, sent_obj, error_sents = process_sentences(f"../PDFNLT/pdfanalyzer/text/{pdf_name}.sent.tsv")

  pdf_term_info_list = create_terms_info(entity_set, sent_list, sent_obj)

  # pdf_term_info_list = extend_terms_info(pdf_term_info_list, error_sents, xhtml_soup)

  # TODO
  # Math Formulations are replaced in text with 1 tag, so can't be directly directly recognized!
  # [DONE] RVM CREATE file to switch to jruby

  return pdf_term_info_list
