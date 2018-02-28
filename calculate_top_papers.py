# @author Daniel Vliegenthart

import argparse
import re
import operator
import csv
import statistics
from config import entity_weight, term_weight, number_top_papers

def main():
  parser = argparse.ArgumentParser(description='Calculate top papers with most occurances')
  parser.add_argument('facet', metavar='Facet', type=str,
                     help='facet of specific domain e.g. dataset, method')

  args = parser.parse_args()
  facet = args.facet

  # ############################# #
  #      CALCULATE TOP PAPERS     #
  # ############################# #

  # Read entity and term overviews
  paper_entities = read_papers_occs("data/papers_journal_entities_overview.csv", number_top_papers, 2)
  paper_terms = read_papers_occs("data/papers_terms_overview.csv", number_top_papers)

  # Calculate number of occcurances for papers
  paper_occs = combine_dicts(paper_entities, paper_terms)
  papers_sorted_number = sorted(paper_occs.items(), key=operator.itemgetter(1), reverse=True)

  # Apply occurance importance weights to entities and terms
  paper_entities = multiply_dict_values(paper_entities, entity_weight)
  paper_terms = multiply_dict_values(paper_terms, term_weight)

  # Combine dictionaries to get final counts for weighted occurances in each paper
  paper_occs = combine_dicts(paper_entities, paper_terms)
  papers_sorted_weight = sorted(paper_occs.items(), key=operator.itemgetter(1), reverse=True)
  papers_sorted = []

  for i, (paper_name, number_occurances) in enumerate(papers_sorted_number):
    papers_sorted.append((paper_name, number_occurances, papers_sorted_weight[i][1]))

  top_papers = papers_sorted[:number_top_papers]

  # Write occurances and top papers to csv files
  print("Writing occurances and top papers to csv files...")
  write_tuples_to_csv(papers_sorted, 'data/papers_occurances_overview.csv', ['paper_name', 'number_occurances', 'weighted_occurances'])
  write_tuples_to_csv(top_papers, 'data/top_papers_overview.csv', ['paper_name', 'number_occurances', 'weighted_occurances'])

# Read papers and number entities overview file
def read_papers_occs(file_path, number_top_papers, column=1):
  paper_entities_raw = open(file_path, 'r').readlines()
  paper_entities_raw = [line.rstrip('\n') for line in paper_entities_raw]
  print(paper_entities_raw.pop(0)) # Remove header column
  paper_entities = {}

  for line in paper_entities_raw:
    paper_split = line.lower().split(",")
    # print(paper_split[column])
    paper_entities[paper_split[0]] = int(paper_split[column])

  return paper_entities

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




