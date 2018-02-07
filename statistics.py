# @author Daniel Vliegenthart

def init():
  global stat_list
  stat_list = []

def print_stats():
  print("\n----------------------")
  print("-     STATISTICS     -")
  print("----------------------")

  for stat in stat_list:
    print(stat)

  print("")