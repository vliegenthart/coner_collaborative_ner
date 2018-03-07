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

  rel_to_index = { 'relevant': 1, 'irrelevant': 2}
  feedback_list, papers_dict = read_users_feedback(f'data/{database}/entities_feedback_csv/10_users_entities_feedback.csv', 2)
  paper_keys = [key.strip("\'") for key in papers_dict.keys()]

  papers_entities_dict = dict.fromkeys(paper_keys, {})

  # Populate with numbers
  for paper_id in paper_keys:
    entities_dict = papers_entities_dict[paper_id].copy()
    for feedback in papers_dict[paper_id]:
      if not feedback[5].strip("\'") == facet: continue
      entity_text = feedback[3].strip("\'")
      feedback = feedback[4].strip("\'")
      
      if entity_text not in entities_dict.keys(): entities_dict[entity_text] = [0,0,0]

      entities_dict[entity_text][0] += 1
      entities_dict[entity_text][rel_to_index[feedback]] += 1

    papers_entities_dict[paper_id] = entities_dict.copy()

  # Calculate relevance scores
  for paper_id in paper_keys:
    relevance_dict = papers_entities_dict[paper_id]
    for entity in relevance_dict.keys():
      rel_str = str(relevance_dict[entity][1]) + '/' + str(relevance_dict[entity][0])
      rel_perc = round(float(relevance_dict[entity][1])/relevance_dict[entity][0],2)
      relevance_dict[entity] = [relevance_dict[entity][0], rel_str, rel_perc]

    papers_entities_dict[paper_id] = relevance_dict.copy()

  # Sort by relevance score
  scores_list = []
  for paper_id in paper_keys:
    scores_list_temp = sorted(papers_entities_dict[paper_id].copy().items(), key=lambda e: e[1][2], reverse=True)
    scores_list_temp = [(paper_id, e[0], e[1][0], e[1][1], e[1][2]) for e in scores_list_temp]
    scores_list = scores_list + scores_list_temp
  
  write_tuples_to_csv(scores_list, f'data/{database}/{facet}_relevance_scores.csv', ['paper_id', 'total_votes', 'relevance_score', 'relevance_percentage'])



# Read papers and number entities overview file
def read_users_feedback(file_path, column=1):
  paper_entities_raw = open(file_path, 'r').readlines()
  paper_entities_raw = [line.rstrip('\n') for line in paper_entities_raw]
  paper_entities_raw.pop(0) # Remove header column
  papers_dict = {}
  feedback_list = []

  for line in paper_entities_raw:
    paper_split = line.lower().split(",")
    if paper_split[9].strip("\'") not in papers_dict.keys(): papers_dict[paper_split[9].strip("\'")] = []
    papers_dict[paper_split[9].strip("\'")].append(paper_split)
    feedback_list.append(paper_split)

  return feedback_list, papers_dict

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




