#/bin/bash

# BEFORE RUNNING THIS SCRIPT, MAKE SURE ALL PDF FILES AND PDF_NAME_entities.json ARE THERE!

# TODO
# - EXTRACT ALLLLLLL THE DATA DANIEL! ALSO FOR EACH FACET AND ALL PDFS
# - Maybe just crawl entire publications collection and save it locally???
# - Add supports and parameter passing for FACETS
# - Fix facet for enrichment XHTML

# ############## #
#      SETUP     #
# ############## #

script=$(cd $(dirname $0) && pwd)

usage() {
  echo -e "Usage: $0 <database> <facet> <sample_number_papers> <fetch_database_papers>"
}

if [[ -z "$1" ]] || [[ -z "$2" ]] || [[ -z "$3" ]]

then
  usage
  exit 1
fi

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

database=$1
facet=$2
sample_number_papers=$3

echo "Variables:"
echo "DATABASE: $database"
echo "FACET: $facet"
echo "SAMPLE_NUMBER_PAPERS: $sample_number_papers"
echo "FETCH_DATABASE_PAPERS: $4"

# ################################ #
#      EXTRACT PDFS & ENTITIES     #
# ################################ #

string_lines="--------------------------------------------------------------------"

echo $string_lines
echo "-     TSE-NER: EXTRACT $sample_number_papers PDFS & ENTITIES & PAPER INFORMATION     -"
echo $string_lines

# Create overview of all papers with journal and number extracted entities
if [ ! -f "../named_entity_recognizer/data/${database}/${facet}_papers_journal_entities_overview.csv" ]; then
  python "../named_entity_recognizer/create_papers_journal_entities_overview.py" $database $facet
fi

echo "Copying papers_journal_entities overview to data/${database}/ directory..."
cp -R "data/${database}/${facet}_papers_journal_entities_overview.csv" "data/${database}/OLD_${facet}_papers_journal_entities_overview.csv" || :
cp -R "../named_entity_recognizer/data/${database}/${facet}_papers_journal_entities_overview.csv" "data/${database}/${facet}_papers_journal_entities_overview.csv"


# Fetch, write and copy papers information from TSE-NER server; publication attributes, pdf file, entities and full text
if [ ! -z $4 ]; then
  python "../named_entity_recognizer/download_paper_objects.py" $database $facet $sample_number_papers 
fi

echo "Copying papers information from ${database} server; publication attributes, pdf file, entities and full text..."
cp -R "data/${database}/${facet}_papers_information_overview.csv" "data/${database}/OLD_${facet}_papers_information_overview.csv" || :
cp -R "../named_entity_recognizer/data/${database}/" "data/${database}/"
cp -R "../named_entity_recognizer/data/${database}/pdf/" "../PDFNLT/pdfanalyzer/${database}_pdf/"

# 
# cp -R "data/${database}/${facet}_papers_journal_entities_overview.csv" "data/${database}/OLD_${facet}_papers_journal_entities_overview.csv" || :
# cp -R "../named_entity_recognizer/data/${database}/${facet}_papers_journal_entities_overview.csv" "data/${database}/${facet}_papers_journal_entities_overview.csv"





