from html.parser import HTMLParser
import argparse
import re

# #################### #
#      XHTMLParser     #
# #################### #

max_entity_words = 3
multi_term_list = []
term_information_list = []
tag_attrs = { 'class': '', 'id': '', 'data-bdr': '', 'data-ftype': '', 'data-space': ''}
VES = []

def intersect(a, b):
  return list(set(a) & set(b))

class Term(number_words, word_information):
  def __init__(self):
    print("NEW TERM")

  # Term consists of multiple words!



class XHTMLParser(HTMLParser):

  def handle_starttag(self, tag, attrs):
    if tag == 'span':
      for attr,value in attrs:
        tag_attrs[attr] = value

    print(tag_attrs)

    # print("Encountered a start tag:", tag)
    x=2

  def handle_endtag(self, tag):
    tag_attrs = {}
    # print("Encountered an end tag :", tag)
    x=1

  def handle_data(self, data):
    x=1
    print(self.get_starttag_text())
    Clean word to match term format
    cleaned_data = re.sub('[^A-Za-z0-9\-]+', '', data).lower()
    if not cleaned_data: return
    cand_list = [cleaned_data]

    # Multi word term support
    for term in cand_list:
      term += " " + cleaned_data


    multi_term_list.append({ "text": cleaned_data:})
    if len(multi_term_list) > max_term_words: 
      del multi_term_list[0] 

    if len(multi_term_list) > 1:
      for i in range(len(multi_term_list)-1):
        cand_list.append(" ".join(multi_term_list[0:i+2]))

    match_list = intersect(cand_list, term_set)
    
    if match_list:
      for match in match_list
        # Create new term
        # Assign information to term



      term_set.remove(term_set[term_set.index(cleaned_data)])

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

# ##################### #
#      READ TERMSET     #
# ##################### #

term_set_file = f"term_set/{pdf_name}_set_0.txt"
term_set = open(term_set_file, 'r').readlines()
term_set = [term.rstrip('\n') for term in term_set]

# #################### #
#      PARSE XHTML     #
# #################### #

xhtml_file = f"../PDFNLT/pdfanalyzer/xhtml/{pdf_name}.xhtml"
xhtml = open(xhtml_file, 'r').read()

parser = XHTMLParser()
parser.feed(xhtml)

print(term_set)





