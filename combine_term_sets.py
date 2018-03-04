# @author Daniel Vliegenthart

import argparse

def main():

  parser = argparse.ArgumentParser(description='Combine Term Sets')

  parser.add_argument('database', metavar='Database', type=str,
                       help='database name of data collection')
  parser.add_argument('facet', metavar='Facet', type=str,
                       help='facet of specific domain e.g. database, method')
  parser.add_argument('number_sets', metavar='Number sets', type=int,
                       help='number of term sets')

  args = parser.parse_args()
  database = args.database
  facet = args.facet
  number_sets = args.number_sets
  final_term_set = []

  for i in range(number_sets):

    term_set = read_term_set(f'data/{database}/model_term_set/{facet}_model_1_term_set_{i}_100.txt')
    final_term_set = list(set().union(final_term_set, term_set))


  with open(f'data/{database}/model_term_set/{facet}_model_1_term_set_final_100.txt', 'w+') as outputFile:
    for t in final_term_set:
      outputFile.write(f'{t}')

def read_term_set(file_path):
  term_set_text = open(file_path, 'r').readlines()
  term_set = []

  for term in term_set_text: term_set.append(term.lower())

  return term_set


if __name__=='__main__':

  main()
