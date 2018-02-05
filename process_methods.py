from bs4 import BeautifulSoup

def read_term_set(file_path):
  term_set = open(file_path, 'r').readlines()
  term_set = [term.rstrip('\n') for term in term_set]

  return term_set

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

  return sent_list, sent_obj