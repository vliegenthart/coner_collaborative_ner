# @author Daniel Vliegenthart

import logging

logging_file = 'logging/statistics.log'

def init():
  logging.basicConfig(filename=logging_file,level=logging.INFO)

def log_stat(stat_string):
  logging.info(stat_string)

def print_stats():
  print("\n----------------------------")
  print("-     XHTML STATISTICS     -")
  print("----------------------------")

  with open(logging_file) as f:
    f = f.read().splitlines()

  for line in f:
    split_line = line.split("root:")
    print(line.split(":root:")[1])

    if split_line[0].lower() == 'info':
      print(split_line[1])

  print("")




