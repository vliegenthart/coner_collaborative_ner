#/bin/bash

# BEFORE RUNNING THIS SCRIPT, MAKE SURE ALL PDF FILES AND PDF_NAME_entities.json ARE THERE!

# TODO
# - EXTRACT ALLLLLLL THE DATA DANIEL!
# - Add supports and parameter passing for FACETS
# - Fix facet for enrichment XHTML
# ############## #
#      SETUP     #
# ############## #

script=$(cd $(dirname $0) && pwd)

usage() {
  echo -e "Usage: $0 <sample_number_papers>"
}

# ##################### #
#      DEPENDENCIES     #
# ##################### #

echo "---------------------------------"
echo "-     CHECKING DEPENDENCIES     -"
echo "---------------------------------"
# echo '✓'
# echo '×' 

if [ -d "$script/../PDFNLT/" ]; then
  echo "✓ PDFNLT"
else
  echo -e "× PDFNLT required in parent directory"
  exit -1
fi

if [ -d "$script/../named_entity_recognizer/" ]; then
  echo "✓ NER"
else
  echo -e "× NER required in parent directory"
  exit -1
fi

# Load RVM into a shell session *as a function*
# Loading RVM *as a function* is mandatorygit ac
# so that we can use 'rvm use <specific version>'
if [[ -s "$HOME/.rvm/scripts/rvm" ]] ; then
  # First try to load from a user install
  source "$HOME/.rvm/scripts/rvm"
  echo "✓ RVM user install found: $HOME/.rvm/scripts/rvm"
elif [[ -s "/usr/local/rvm/scripts/rvm" ]] ; then
  # Then try to load from a root install
  source "/usr/local/rvm/scripts/rvm"
  echo "✓ RVM root install found: /usr/local/rvm/scripts/rvm"
else
  echo -e "RVM installation was not found"
  exit -1
fi

echo ""

sample_number_papers=$1

# ################################ #
#      EXTRACT PDFS & ENTITIES     #
# ################################ #

string_lines="------------------------------------------------"

echo $string_lines
echo "-     TSE-NER: EXTRACT $sample_number_papers PDFS & ENTITIES     -"
echo $string_lines

if [ -f "../named_entity_recognizer/data/papers_journal_entities_overview.csv" ]; then
  python "../named_entity_recognizer/create_papers_journal_entities_overview.py"
fi

echo "Copying papers_journal_entities overview to data/ directory..."
cp -R "data/papers_journal_entities_overview.csv" "data/OLD_papers_journal_entities_overview.csv" || :
cp -R "../named_entity_recognizer/data/papers_journal_entities_overview.csv" "data/papers_journal_entities_overview.csv"

