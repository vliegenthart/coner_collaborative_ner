# @author Daniel Vliegenthart

from utility_methods import intersect
from process_methods import read_entity_set, read_xhtml, process_sentences, create_terms_info
from class_definitions import Entity, PDFTerm, PDFWord

# Can also do it the other way around! Go through term set and search each term
# in the entire XHTML/TSV/CSV. For multi word, search in sentence, then lookup in the
# words after that sentence. Enrich & create TSV/CSV with Term info that way.
# Use Term class or no??
# Words: Any special characters except for 'space' and '-'
# Changed Term to Entity!!!!!!!: Every word in the entity_set.txt is considered 1 entity. 


# Find Entities with associated pdf_terms and pdf_words in the {pdf_name}.sent.tsv file
def find_pdf_terms_in_sent_tsv(pdf_name):

  # ############################ #
  #      FIND TERMS FOR XHTML    #
  # ############################ #

  entity_set = read_entity_set(f"data/entity_set/{pdf_name}_set_0.txt")
  xhtml_soup = read_xhtml(f"../PDFNLT/pdfanalyzer/xhtml/{pdf_name}.xhtml")
  sent_list, sent_obj, error_sents = process_sentences(f"../PDFNLT/pdfanalyzer/text/{pdf_name}.sent.tsv")
  pdf_term_info_list = create_terms_info(entity_set, sent_list, sent_obj)

  return pdf_term_info_list
