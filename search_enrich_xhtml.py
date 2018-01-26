from html.parser import HTMLParser
from bs4 import BeautifulSoup
import argparse
import re
from functions import intersect

# #################### #
#      XHTMLParser     #
# #################### #

max_term_words = 3
multi_term_list = []
term_information_list = []
tag_attrs = { 'class': '', 'id': '', 'data-bdr': '', 'data-ftype': '', 'data-space': ''}
VES = []


# class Term(number_words, word_information):
#   def __init__(self):
#     print("NEW TERM")

  # Term consists of multiple words!



# class XHTMLParser(HTMLParser):

#   def handle_starttag(self, tag, attrs):
#     if tag == 'span':
#       for attr,value in attrs:
#         tag_attrs[attr] = value

#     print(tag_attrs)

#     # print("Encountered a start tag:", tag)
#     x=2

#   def handle_endtag(self, tag):
#     tag_attrs = {}
#     # print("Encountered an end tag :", tag)
#     x=1

#   def handle_data(self, data):
#     x=1
#     print(self.get_starttag_text())
#     Clean word to match term format
#     cleaned_data = re.sub('[^A-Za-z0-9\-]+', '', data).lower()
#     if not cleaned_data: return
#     cand_list = [cleaned_data]

#     # Multi word term support
#     for term in cand_list:
#       term += " " + cleaned_data


#     multi_term_list.append({ "text": cleaned_data:})
#     if len(multi_term_list) > max_term_words: 
#       del multi_term_list[0] 

#     if len(multi_term_list) > 1:
#       for i in range(len(multi_term_list)-1):
#         cand_list.append(" ".join(multi_term_list[0:i+2]))

#     match_list = intersect(cand_list, term_set)
    
#     if match_list:
#       for match in match_list
#         # Create new term
#         # Assign information to term



#       term_set.remove(term_set[term_set.index(cleaned_data)])

    # Can also do it the other way around! Go through term set and search each term
    # in the entire XHTML/TSV/CSV. For multi word, search in sentence, then lookup in the
    # words after that sentence. Enrich & create TSV/CSV with Term info that way.
    # Use Term class or no??


# ################### #
#      SETUP ARGS     #
# ################### #

parser = argparse.ArgumentParser(description='Annotate xhtml file with term set')
parser.add_argument('pdf_name', metavar='PDF Name', type=str,
                   help='name of pdf and xhtml file to be annotated')

args = parser.parse_args()
pdf_name = args.pdf_name

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
  # print(sent_split)
  sent_id = sent_split.pop(0)
  sect_name = sent_split.pop(0)
  box_name = sent_split.pop(0)
  word_ids = sent_split.pop()
  sent_obj_obj = { 'sent_id': sent_id, 'sect_name': sect_name, 'box_name': box_name, 'text': " ".join(sent_split), 'word_ids': word_ids }

  sent_list.append(sent_obj_obj)
  sent_obj[sent_id] = sent_obj_obj

# print(sent_obj['s-2-0-0-0'], "\n", sent_obj['s-13-1-1-3'])
print(sent_list[40])

# ################################ #
#      FIND TERMS IDs for XHTML    #
# ################################ #

# Words: Any special characters except for 'space'
# s-13-1-1-3  Subsection  Body  For comparison, two supervised text categorization methods, naive Bayes and Support Vector Machine (SVM), were also applied to the same training and test sets. 
# w-13-1-2-0,w-13-1-2-1,w-13-1-2-2,w-13-1-2-3,w-13-1-2-4,w-13-1-2-5,w-13-1-2-6,w-13-1-2-8,w-13-1-2-9,w-13-1-2-10,w-13-1-2-11,w-13-1-2-12,w-13-1-2-13,w-13-1-2-14,w-13-1-2-15,w-13-1-2-16,w-13-1-2-17,w-13-1-2-18,w-13-1-2-19,w-13-1-2-20,w-13-1-2-21,w-13-1-2-22,w-13-1-2-23,w-13-1-2-24,w-13-1-2-25,w-13-1-2-26,w-13-1-2-27,w-13-1-2-28,w-13-1-2-29,w-13-1-2-30

# for term in term_set:
#   for sent in sent_list:
#     if term in sent['sent_text']:
#       print(sent['sent_id'], ": ", sent['sent_text'])


# ###################### #
#      PROCESS XHTML     #
# ###################### #


# words = xhtml_soup.find_all("span", class_="word")
# print(words)

# for word in words:
#   print(word['id'])








