# @author Daniel Vliegenthart

# # Add term IDs for term set!!

# Entity as it occurs in extracted entity_set.txt
class Entity(object):
  pdf_terms, text, words, number_words = ([], '', [], '')

  def __init__(self, text):
    self.text = text
    self.words = text.split(" ")
    self.number_words = len(self.words)

# Occurances of Entities in PDF document
class PDFTerm(object):
  words = []
  number_words = 1

  def __init__(self, words):
    self.words = words
    number_words = len(words)

    print("NEW TERM")

  # Term can consist of multiple words!

# PDFWords associated with each occurance of PDFTerm
class PDFWord(object):
  def __init__(self):
    print("NEW WORD")
