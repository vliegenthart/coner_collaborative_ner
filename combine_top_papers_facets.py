# @author Daniel Vliegenthart

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

  args = parser.parse_args()
  database = args.database

  # ############################# #
  #      CALCULATE TOP PAPERS     #
  # ############################# #

  top_papers_weight = {}
  top_papers_occs = {}
  final_top_papers = []

  # Read top papers for each set

  # Combine occurrences for all facet top paper overviwes
  for facet in facets:
    top_papers_weight = combine_dicts(top_papers_weight, read_papers_occs(f'data/{database}/{facet}_top_papers_overview.csv', 2))
    top_papers_occs = combine_dicts(top_papers_occs, read_papers_occs(f'data/{database}/{facet}_top_papers_overview.csv', 1))

  top_papers_weight = sorted(top_papers_weight.items(), key=operator.itemgetter(1), reverse=True)
  top_papers_occs = sorted(top_papers_occs.items(), key=operator.itemgetter(1), reverse=True)

  for i, (paper_id, weighted_occurances) in enumerate(top_papers_weight):
    final_top_papers.append((paper_id, top_papers_occs[i][1], weighted_occurances))

  # Write occurances and top papers to csv files
  print("Writing occurances and top papers to csv files...")
  write_tuples_to_csv(final_top_papers, f'data/{database}/final_top_papers_overview.csv', ['paper_id', 'number_occurrences', 'weighted_occurrences'])

# Read papers and number entities overview file
def read_papers_occs(file_path, column=1):
  paper_entities_raw = open(file_path, 'r').readlines()
  paper_entities_raw = [line.rstrip('\n') for line in paper_entities_raw]
  paper_entities_raw.pop(0) # Remove header column
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




