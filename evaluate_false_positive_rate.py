# @author Daniel Vliegenthart

# TODO

# ["'2018-03-06t13:18:03'", "'occurrence'", "'letters'", "'letters'", "'relevant'", "'dataset'", "'w-1-0-107-146'", "'4482300168'", "'4462521312'", "'conf_trec_loseysr15'", "'58'", "'user_10'", "'791d1563-a2ff-4e80-99f7-a5005e77cb91'"]

import argparse
import re
import operator
import csv
import statistics
from datetime import datetime, timedelta


def main():
  parser = argparse.ArgumentParser(description='Calculate top papers with most occurances')
  parser.add_argument('database', metavar='Database', type=str,
                     help='database name of data collection')
  parser.add_argument('facet', metavar='Facet', type=str,
                     help='facet of domain e.g. dataset or method')

  args = parser.parse_args()
  database = args.database
  facet = args.facet

  # ################################# #
  #      EVALUATE FALSE POSITIVES     #
  # ################################# #

  print(facet)

  relevance_list = read_users_feedback(f'data/{database}/{facet}_relevance_scores.csv')
  # feedback_list, papers_dict = read_users_feedback(f'data/{database}/entities_feedback_csv/10_users_entities_feedback.csv')
  paper_keys = {'conf_trec_balogsv10': 'conf_trec_BalogSV10', 'conf_trec_bellotcegl02': 'conf_trec_BellotCEGL02', 'conf_trec_loseysr15': 'conf_trec_LoseySR15'}

  paper_tp_rates = { 'conf_trec_balogsv10': [0,0], 'conf_trec_bellotcegl02': [0,0], 'conf_trec_loseysr15': [0,0] }

  for paper_id in paper_tp_rates.keys():
    # print(paper_id)
    for feedback in relevance_list:
      facet_entity = feedback[1].strip("\'")
      if paper_id == feedback[0].strip("\'"):
        # print(float(feedback[4]), float(feedback[4]) >= 0.5)
        if float(feedback[4]) > 0.5:
          paper_tp_rates[paper_id][0] += 1
        
        paper_tp_rates[paper_id][1] += 1


  print(paper_tp_rates)
  final_tp_rate_arr = []

  for paper_id in paper_tp_rates.keys():
    feedback = paper_tp_rates[paper_id]
    tp_rate = feedback[0]/float(feedback[1])
    print(paper_id, " FP rate:", 100 - round(tp_rate*100,2))
    final_tp_rate_arr.append(tp_rate)

  final_tp_rate = round((sum(final_tp_rate_arr)/float(len(final_tp_rate_arr)))*100,2)

  print(f'{facet} TP rate: {final_tp_rate}')
  print(f'{facet} FP rate: {100 - final_tp_rate}')

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





