# @author Daniel Vliegenthart

from bs4 import BeautifulSoup
import re
import json
import jsonpickle
import pprint

def read_xhtml(file_path):
  xhtml = open(file_path, 'r').read()
  xhtml_soup = BeautifulSoup(xhtml, 'html.parser')

  return xhtml_soup

def enrich_xhtml(pdf_term_list, xhtml_soup, facet, pdf_name):

  pdf_terms_pages = [[] for _ in range(1000)]
  output_entity_json = "["

  print("Enriching XHTML words with pdf_word meta-data...")
  for entity in pdf_term_list:
    for pdf_term in entity.pdf_terms:
      for pdf_word in pdf_term.pdf_words:
        span_word = xhtml_soup.find("span", class_="word", id=pdf_word.word_id)
        span_word['data-entity_id'] = entity.id
        span_word['data-pdf_term_id'] = pdf_term.id
        span_word['data-pdf_word_id'] = pdf_word.id
        span_word['data-facet'] = facet

        pdf_word.pdf_term_id = pdf_term.id
        pdf_word.bdr = span_word['data-bdr']
        pdf_word.facet = facet
        
        page_number = span_word.parent['data-page']
        pdf_word.page_number = page_number
        pdf_term.page_number = page_number

      pdf_terms_pages[int(pdf_term.page_number)].append(pdf_term)

    output_entity_json += jsonpickle.encode(entity) + ","
  
  pdf_terms_pages = [x for x in pdf_terms_pages if x]
  output_entity_json = output_entity_json[:-1] + "]"

  print(f'Writing JSON file with entity information to json/{pdf_name}_entities.json...')

  with open(f'data/json/{pdf_name}_entities.json', 'w+') as outputFile:
    outputFile.write(output_entity_json + "\n")

  print(f'Writing JSON file with PDFTerms per page information to json/{pdf_name}_pdf_terms_pages.json...')
  
  with open(f'data/json/{pdf_name}_pdf_terms_pages.json', 'w+') as outputFile:
    outputFile.write(jsonpickle.encode(pdf_terms_pages) + "\n")

  print(f'Writing XHTML file with entity information added to xhtml/{pdf_name}.xhtml...')

  with open(f'data/xhtml/{pdf_name}.xhtml', 'w+') as outputFile:
    outputFile.write(str(xhtml_soup.prettify()))

