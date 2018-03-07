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

  # ############################ #
  #      EVALUATE TIME TAKEN     #
  # ############################ #

  # user_1 0:05:13
  # user_2 0:06:42
  # user_3 0:19:38
  # user_4 0:10:37
  # user_5 0:12:37
  # user_6 0:03:21
  # user_7 0:03:51
  # user_8 0:07:03
  # user_9 0:03:14
  # user_10 0:07:18

  # Shortest:  '0:03:14', 'user_9', '12:50:44', '12:53:58', conf_trec_BalogSV10
  # Longest: '0:19:38', 'user_3', '04:54:41', '05:14:19', conf_trec_BellotCEGL02
  # Average time: '00:07:57 minutes'


  user_time = [
    ['user_1','12:38:25', '12:43:38'],
    ['user_2', '11:02:52', '11:09:34'],
    ['user_3', '04:54:41', '05:14:19'],
    ['user_4', '05:35:37', '05:46:14'],
    ['user_5', '07:18:18', '07:30:55'],
    ['user_6', '07:43:04', '07:46:25'],
    ['user_7', '10:32:24', '10:36:15'],
    ['user_8', '11:59:51', '12:06:54'],
    ['user_9', '12:50:44', '12:53:58'],
    ['user_10', '13:10:45', '13:18:03']
  ]

  for index, usr in enumerate(user_time):
    print(index, usr)
    FMT = '%H:%M:%S'
    tdelta = datetime.strptime(usr[2], FMT) - datetime.strptime(usr[1], FMT)

    user_time[index].append(str(tdelta))

  user_time = sorted(user_time, key=operator.itemgetter(3))

  times = ['0:05:13','0:06:42','0:19:38','0:10:37','0:12:37', '0:03:21', '0:03:51', '0:07:03', '0:03:14', '0:07:18']
  print(str(timedelta(seconds=sum(map(lambda f: int(f[0])*3600 + int(f[1])*60 + int(f[2]), map(lambda f: f.split(':'), times)))/len(times))))
  
  # print(user_time)

  # ##################################### #
  #      EVALUATE % FEEDBACK GIVEN ON     #
  # ##################################### #

  feedback_list, papers_dict = read_users_feedback(f'data/{database}/entities_feedback_csv/10_users_entities_feedback.csv')
  paper_keys = {'conf_trec_balogsv10': 'conf_trec_BalogSV10', 'conf_trec_bellotcegl02': 'conf_trec_BellotCEGL02', 'conf_trec_loseysr15': 'conf_trec_LoseySR15'}

  user_entities_rated = [['paper', 0] for e in range(10)]

  for feedback in feedback_list:
    user_index = int(feedback[11].strip("\'").split("_")[1])
    facet_entity = feedback[5].strip("\'")
    if facet_entity == facet:
      user_entities_rated[user_index-1][0] = feedback[9].strip("\'")
      user_entities_rated[user_index-1][1] += 1

  for index, user in enumerate(user_entities_rated):
    paper_id = paper_keys[user[0]]
    file_path = f'data/{database}/entity_set/{facet}_{paper_id}_entity_set_0.txt'
    filtered_entity_set = list(set(open(file_path, 'r').readlines()))
    user_entities_rated[index][1] = round(user_entities_rated[index][1]/float(len([x.lower().strip("\n") for x in filtered_entity_set]))*100,1)

  user_entities_rated =  sorted(user_entities_rated, key=operator.itemgetter(0,1))

  print(facet)
  total_perc = 0
  for user in user_entities_rated:
    print(user)
    total_perc += user[1]

  print(f'Total percentage of entities with feedback: {round(total_perc/float(len(user_entities_rated)),2)}')

# Read papers and number entities overview file
def read_users_feedback(file_path):
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





