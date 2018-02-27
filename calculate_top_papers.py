# @author Daniel Vliegenthart

import argparse
import re
import operator
import statistics

def main():
  parser = argparse.ArgumentParser(description='Calculate top papers with most occurances')
  parser.add_argument('facet', metavar='Facet', type=str,
                     help='facet of specific domain e.g. database, method')
  parser.add_argument('number_top_papers', metavar='Number Top Papers', type=int,
                     help='number of top papers to keep')

  args = parser.parse_args()
  facet = args.facet
  number_top_papers = args.number_top_papers

  # ############################# #
  #      CALCULATE TOP PAPERS     #
  # ############################# #

  paper_entities = read_papers_occs("data/papers_entities_overview.csv", number_top_papers)
  paper_terms = read_paper_occs("data/papers_terms_overview.csv", number_top_papers)

  # paper_entities = sorted(paper_entities.items(), key=operator.itemgetter(1), reverse=True)

  print(paper_entities, paper_terms)


# Read papers and number entities overview file
def read_papers_occs(file_path, number_top_papers):
  paper_entities_raw = open(file_path, 'r').readlines()
  paper_entities_raw = [line.rstrip('\n') for line in paper_entities_raw]
  paper_entities_raw.pop(0) # Remove header column
  paper_entities = {}

  for line in paper_entities_raw:
    paper_split = line.lower().split(",")
    paper_entities[paper_split[0]] = int(paper_split[1])

  return paper_entities

if __name__=='__main__':

  main()




