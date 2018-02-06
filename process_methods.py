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

# Process and create list of sentences with meta-data
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

    # Add extra metadata to word-array adn add sentence to list and object
    else:
      word_set_info = []
      word_set = []
      for i, word in enumerate(word_array):
        if word not in word_set:
          temp_word = { 'text': word, 'word_id': word_ids[i] }
          word_set_info.append(temp_word)
          word_set.append(word)

      sent_obj_obj['word_set_info'] = word_set_info
      # print(sent_obj_obj['word_array_info'])

      sent_list.append(sent_obj_obj)
      sent_obj[sent_id] = sent_obj_obj

  # Print some sentence split processing stats
  print(f'# sentences incorrectly split by PDFNLT: {len(error_sents)}/{len(sent_list)}')
  print(f'# entities rejected because entity.number_words > max_entity_words ({max_entity_words}): {number_entities_rejected}')

  # print(sent_obj['s-3-1-0-2']['word_set_info'])
  return sent_list, sent_obj, error_sents


# Create the set of PDFTerms occurances in PDf from Entity set
def create_terms_info(entity_set, sent_list, sent_obj):

  # Entity to sentence match possible cases:
  # - 1 word entity
  # - multi-word entity
  # - partly match, but not entity
  # - muliple occurance of entity

  # LIMITATIONS:
  # - Only the 1st occurance for each sentence captured (matched through set of words in sentence without duplicates),
  #   so assumed that that words in entities only occur once (no entity without duplicate words)


  term_info_list = []

  for entity in entity_set:
    for sent in sent_list:
      if entity.text in sent['text']:
        pdf_term = PDFTerm(sent['sent_id'])

        for word in sent['word_set_info']:
          if word['text'] in entity.words:
            pdf_term.pdf_words.append(PDFWord(word['text'], word['word_id']))

        entity.pdf_terms.append(pdf_term)
        # print(len(entity.pdf_terms))
        # print(pdf_term)

        # if entity.number_words > 1:
        #   print(entity.text, ": ", entity.number_words)

    print(entity)

  


  # [DONE] Use word array to match with term
  # Create PDFTerm with words meta-data
  # Enrich XHTML with word-id to add attribute
  # Add config file with meta-data about each word, or add all in xhtml attributes






















