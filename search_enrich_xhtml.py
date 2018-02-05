from html.parser import HTMLParser
from bs4 import BeautifulSoup
import argparse
import re
from functions import intersect


# Can also do it the other way around! Go through term set and search each term
# in the entire XHTML/TSV/CSV. For multi word, search in sentence, then lookup in the
# words after that sentence. Enrich & create TSV/CSV with Term info that way.
# Use Term class or no??
# Words: Any special characters except for 'space' and '-'

# ################### #
#      SETUP ARGS     #
# ################### #

parser = argparse.ArgumentParser(description='Annotate xhtml file with term set')
parser.add_argument('pdf_name', metavar='PDF Name', type=str,
                   help='name of pdf and xhtml file to be annotated')

args = parser.parse_args()
pdf_name = args.pdf_name

# ####################### #
#      INIT VARIABLES     #
# ####################### #

max_term_words = 3
multi_term_list = []
term_information_list = []
tag_attrs = { 'class': '', 'id': '', 'data-bdr': '', 'data-ftype': '', 'data-space': ''}
VES = []
word_split_pattern = r'([` \t\=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?])'
error_sents = []

# ######################################## #
#      READ TERMSET, XHTML AND SENT.TSV    #
# ######################################## #

term_set_file = f"data/term_set/{pdf_name}_set_0.txt"
term_set = open(term_set_file, 'r').readlines()
term_set = [term.rstrip('\n') for term in term_set]

xhtml_file = f"../PDFNLT/pdfanalyzer/xhtml/{pdf_name}.xhtml"
xhtml = open(xhtml_file, 'r').read()
xhtml_soup = BeautifulSoup(xhtml, 'html.parser')

sent_list_file = f"../PDFNLT/pdfanalyzer/text/{pdf_name}.sent.tsv"
sent_list_raw = open(sent_list_file, 'r').readlines()
sent_list_raw = [sent.rstrip('\n') for sent in sent_list_raw]
sent_list_raw.pop(0) # Remove header column
sent_list = []
sent_obj = {}

for sent in sent_list_raw:
  sent_split = sent.split("\t")
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

# ################################ #
#      FIND TERMS IDs for XHTML    #
# ################################ #

for term in term_set:
  for sent in sent_list:
    if term in sent['text']:
      word_array = sent['word_array']
      word_ids = sent['word_ids']
      if len(word_array) != len(word_ids):
        error_sent_ids.append(sent['sent_id'])
      else:



        # print(len(word_array), len(word_ids))
        # print(word_array, "\n", sent['text'])

        # ERROR HANDLNG!
        # quit()
      # print(sent['sent_id'], ": ", sent['text'])

      # print(sent['sent_id'], ": ", term)
      # i=2

# Add term IDs for term set!!


# ###################### #
#      PROCESS XHTML     #
# ###################### #


# words = xhtml_soup.find_all("span", class_="word")
# print(words)

# for word in words:
#   print(word['id'])








