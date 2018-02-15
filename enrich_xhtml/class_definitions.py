# @author Daniel Vliegenthart

# # Add term IDs for term set!!

# Entity as it occurs in extracted entity_set.txt
class Entity(object):

  # Entity can consist of multiple terms
  def __init__(self, text, pdf_terms=None):
    if pdf_terms is None: pdf_terms = []
    self.type = "Entity"
    self.id = id(self)
    self.text = text
    self.words = text.split(" ")
    self.number_words = len(self.words)
    self.pdf_terms = pdf_terms

  def __str__(self):
    return f'<Entity: {self.text}, #pdf_terms: {len(self.pdf_terms)}, pdf_terms: {self.pdf_terms}>'

  def __repr__(self):
    return f'<Entity: {self.text}, #pdf_terms: {len(self.pdf_terms)}, pdf_terms: {self.pdf_terms}>'

  def __dumps__(self):
    self.__dict__

# Occurances of Entities in XHTML document
class PDFTerm(object):

  # PDFTerm can consist of multiple words
  def __init__(self,sent_id, entity_id=None, pdf_words=None):
    if pdf_words is None: pdf_words = []
    self.type = "PDFTerm"
    self.id = id(self)
    self.sent_id = sent_id
    self.pdf_words = pdf_words 
    self.entity_id = entity_id
    self.page_number = ""

  def __str__(self):
    return f'<PDFTerm: {self.entity_id}, sent_id: {self.sent_id}, #pdf_words: {len(self.pdf_words)}, pdf_words: {self.pdf_words}, page_number: {self.page_number}>'

  def __repr__(self):
    return f'<PDFTerm: {self.entity_id}, sent_id: {self.sent_id}, #pdf_words: {len(self.pdf_words)}, pdf_words: {self.pdf_words}, page_number: {self.page_number}>'

  def __dumps__(self):
    self.__dict__

# PDFWords associated with each occurance of PDFTerm
class PDFWord(object):

  # PDFWord is 1 word in the XHTML
  def __init__(self, text, word_id, pdf_term_id):
    self.type = "PDFWord"
    self.id = id(self)
    self.text = text
    self.word_id = word_id
    self.pdf_term_id = pdf_term_id
    self.bdr = ""
    self.facet = ""
    self.page_number = ""

  def __str__(self):
    return f'<PDFWord: {self.text}, word_id: {self.word_id}, bdr: {self.bdr}, facet: {self.facet}, page_number: {self.page_number}>'

  def __repr__(self):
    return f'<PDFWord: {self.text}, word_id: {self.word_id}, bdr: {self.bdr}, facet: {self.facet}, page_number: {self.page_number}>'

  def __dumps__(self):
    self.__dict__


