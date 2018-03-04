# @author Daniel Vliegenthart

import argparse
import os

def main():

  parser = argparse.ArgumentParser(description='Postprocess entity sets')

  parser.add_argument('database', metavar='Database', type=str,
                       help='database name of data collection')

  args = parser.parse_args()
  database = args.database
  entity_set_files = os.listdir(f'data/{database}/entity_set/')

  for i in range(len(entity_set_files)):
    entity_set = read_entity_set(f'data/{database}/entity_set/{entity_set_files[i]}')

    with open(f'data/{database}/entity_set/{entity_set_files[i]}', 'w+') as outputFile:
      for e in entity_set:

        outputFile.write(e.strip(' .,/') + "\n")

def read_entity_set(file_path):
  entity_set_text = open(file_path, 'r').readlines()
  entity_set = []

  for entity in entity_set_text: entity_set.append(entity.strip("\n"))

  return entity_set


if __name__=='__main__':

  main()
