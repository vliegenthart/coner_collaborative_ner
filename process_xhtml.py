# @author Daniel Vliegenthart

from bs4 import BeautifulSoup
import re

def read_xhtml(file_path):
  xhtml = open(file_path, 'r').read()
  xhtml_soup = BeautifulSoup(xhtml, 'html.parser')

  return xhtml_soup

def enrich_xhtml(pdf_term_list, xhtml_soup):
  print("Enriching XHTML words with pdf_word meta-data...")
  for entity in pdf_term_list:
    for pdf_term in entity.pdf_terms:
      for pdf_word in pdf_term.pdf_words:
        span_word = xhtml_soup.find("span", class_="word", id=pdf_word.word_id)
        span_word['data-entity_id'] = entity.id
        span_word['data-pdf_term_id'] = pdf_term.id
        span_word['data-pdf_word_id'] = pdf_word.id
