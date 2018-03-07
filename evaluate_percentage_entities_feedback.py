# @author Daniel Vliegenthart

# TODO
# Qualitative: Add table with top INCORRECT and CORRECT entities for papers and explanation why

# ["'2018-03-06t13:18:03'", "'occurrence'", "'letters'", "'letters'", "'relevant'", "'dataset'", "'w-1-0-107-146'", "'4482300168'", "'4462521312'", "'conf_trec_loseysr15'", "'58'", "'user_10'", "'791d1563-a2ff-4e80-99f7-a5005e77cb91'"]

import argparse
import re
import operator
import csv
import statistics
from config import entity_weight, term_weight, number_top_papers, facets

def main():
  parser = argparse.ArgumentParser(description='Calculate top papers with most occurances')
  parser.add_argument('database', metavar='Database', type=str,
                     help='database name of data collection')
  parser.add_argument('facet', metavar='Facet', type=str,
                     help='facet of domain e.g. dataset or method')

  args = parser.parse_args()
  database = args.database
  facet = args.facet

  # ########################################### #
  #      EVALUATE USER FEEDBACK ON ENTITIES     #
  # ########################################### #

  relevance_list = read_users_feedback(f'data/{database}/{facet}_relevance_scores.csv')
  paper_keys = ['conf_trec_BalogSV10', 'conf_trec_BellotCEGL02', 'conf_trec_LoseySR15']

  ref_entities = set()
  human_entities = set()

  for paper_id in paper_keys:
    file_path = f'data/{database}/entity_set/{facet}_{paper_id}_entity_set_0.txt'
    ref_entities.update([x.lower().strip("\n") for x in open(file_path, 'r').readlines()])
  

  for entity in relevance_list:
    human_entities.add(entity[1])

  print(facet)
  print(str(len(human_entities)) + "/" + str(len(ref_entities)))

  print(float(len(human_entities))/len(ref_entities))

# Read papers and number entities overview file
def read_users_feedback(file_path, column=1):
  paper_entities_raw = open(file_path, 'r').readlines()
  paper_entities_raw = [line.rstrip('\n') for line in paper_entities_raw]
  paper_entities_raw.pop(0) # Remove header column
  feedback_list = []

  for line in paper_entities_raw:
    paper_split = line.lower().split(",")
    feedback_list.append(paper_split)

  return feedback_list

def multiply_dict_values(dict, mult):
  return {k: int(v)*mult for k, v in dict.items()}

def combine_dicts(a, b, op=operator.add):
  return dict(list(a.items()) + list(b.items()) +
      [(k, op(a[k], b[k])) for k in set(b) & set(a)])

# Write list of tuples to csv file
def write_tuples_to_csv(tuples_list, csv_file, column_names):
  with open(csv_file, 'w+') as outputFile:
    csv_out=csv.writer(outputFile)
    csv_out.writerow(column_names)
    
    for tuple1 in tuples_list:
      csv_out.writerow(tuple1)

if __name__=='__main__':

  main()




