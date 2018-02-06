# @author Daniel Vliegenthart

from bs4 import BeautifulSoup
import re
from class_definitions import Entity, PDFTerm, PDFWord

# all occurences of 1 entity in 1 documents are pdfterms under that entity: entity.pdf_terms
# Each term consists of it's subwords in the document
# Wrote description of classes, sent_list etc


max_entity_words = 3
tag_attrs = { 'class': '', 'id': '', 'data-bdr': '', 'data-ftype': '', 'data-space': ''}
word_split_pattern = r'([` \t\=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?])'
error_sents = []
number_entities_rejected = 0

def read_entity_set(file_path):
  global number_entities_rejected
  entity_set_text = open(file_path, 'r').readlines()
  entity_set = []

  for entity in entity_set_text:
    entity_temp = entity.rstrip('\n')
    if len(entity_temp.split(' ')) <= max_entity_words:
      entity_set.append(Entity(entity_temp))
    else:
      number_entities_rejected+=1

  return entity_set

def read_xhtml(file_path):
  xhtml = open(file_path, 'r').read()
  xhtml_soup = BeautifulSoup(xhtml, 'html.parser')

  return xhtml_soup

def process_sentences(file_path):
  sent_list_raw = open(file_path, 'r').readlines()
  sent_list_raw = [sent.rstrip('\n') for sent in sent_list_raw]
  sent_list_raw.pop(0) # Remove header column
  sent_list = []
  sent_obj = {}

  for sent in sent_list_raw:
    sent_split = sent.lower().split("\t")
    sent_id = sent_split.pop(0)
    sect_name = sent_split.pop(0)
    box_name = sent_split.pop(0)
    word_ids = sent_split.pop().split(",")
    word_array_spaces = re.split(word_split_pattern, " ".join(sent_split))
    word_array = [x for x in word_array_spaces if x not in [" ", "\t", ""]]
    sent_obj_obj = { 'sent_id': sent_id, 'sect_name': sect_name, 'box_name': box_name, 'text': " ".join(sent_split), 'word_array': word_array, 'word_ids': word_ids }

    # Filter out & ignore incorrectly split sentences by PDFNLT (incorrect word displayed in XHTML)
    if len(word_array) != len(word_ids):
      error_sents.append(sent_obj_obj)

    # Add sentence to list and object
    else:
      sent_list.append(sent_obj_obj)
      sent_obj[sent_id] = sent_obj_obj

  # Print some sentence split processing stats
  print(f'# sentences incorrectly split by PDFNLT: {len(error_sents)}/{len(sent_list)}')
  print(f'# entities rejected because entity.number_words > max_entity_words ({max_entity_words}): {number_entities_rejected}')

  return sent_list, sent_obj, error_sents

def create_terms_info(entity_set, sent_list, sent_obj):

  term_info_list = []

  for entity in entity_set:
    for sent in sent_list:

      # if sent['sent_id'] == 's-4-1-1-0':
        # print(sent['text'])

      if entity.text in sent['text']:
        if entity.number_words > 1:
          print(entity.text, ": ", entity.number_words)





















