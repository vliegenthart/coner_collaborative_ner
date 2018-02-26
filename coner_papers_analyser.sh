#/bin/bash

# BEFORE RUNNING THIS SCRIPT, MAKE SURE ALL PDF FILES AND PDF_NAME_entities.json ARE THERE!
# Retrain PDFNLT so all training CSV's are there!

# ############## #
#      SETUP     #
# ############## #

script=$(cd $(dirname $0) && pwd)

usage() {
  echo -e "Usage: $0 [-f] ../PDFNLT/pdfanalyzer/pdf <facet_name> <number_top_papers>"
  # echo -e "   or  $0 [-f] ../PDFNLT/pdfanalyzer/pdf/<pdf_file> <facet_name>"
}

unset force

while getopts "fo:vi" o; do
  case "${o}" in
    f)
      force=1
      ;;
    *)
      usage
      exit 1
      ;;
  esac
done
shift $((OPTIND-1))

if [[ -z "$1" ]] || [[ -z "$2" ]] || [[ -z "$3" ]]
then
  usage
  exit 1
fi

xhtmls=()
shopt -s nullglob

if [ -d "$1" -a -n "$force" ]
then
  # Whole directory, forced
  dir="$(cd $(dirname "$1") && pwd)"
  outdir="${outdir:-$dir/text}"
  pdfs=(--all)
  tsvs=(--all)
else
  if [ -f "$1" ]
  then
    # Individual files
    dir=$(cd $(dirname "$1")/.. && pwd)
    files=("$1")
  else
    # Whole directory, non-forced
    dir="$(cd $(dirname "$1") && pwd)"
    files=("$dir"/pdf/*.pdf)
  fi
  outdir="${outdir:-$dir/text}"

  pdfs=()

  tsvs=()

  for i in "${files[@]}"
  do
    # If not forced, then only pick the files that are not up-to-date
    file="$(basename "$i" .xhtml)"
    file="${file%.pdf}"
    if [ -f "$dir/pdf/$file.pdf" -o -n "$force" ]
    then
      pdfs+=("$dir/pdf/$file.pdf")
      tsvs+=("$file.csv")
      xhtmls+=("$dir/xhtml/$file.xhtml")
    fi
  done
fi

if [ ${#pdfs[@]} -eq 0 ]
then
  # Everything is up-to-date, nothing to do
  echo "No papers to analyse!"
  exit
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

if [ -e "$script/$1" ]; then
  echo "✓ PDF directory found"
else
  echo -e "PDF directory file not found"
  exit -1
fi

# Load RVM into a shell session *as a function*
# Loading RVM *as a function* is mandatory
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

pdf_dir=$1
facet=$2
number_papers=$3


# ##################### #
#      PROCESS PDFS     #
# ##################### #

echo $'Setting up statistics...\n'
rm -Rf "logging/statistics.log"
mkdir -p "logging"
touch "logging/statistics.log"

echo "------------------------------------"
echo "-     XHTML PIPELINE EXECUTION     -"
echo "------------------------------------"

# Copy pdf to PDFNLT and NER
echo "Copying PDF files from PDFNLT to NER and data/pdf/..."
mkdir -p ../named_entity_recognizer/pdf
mkdir -p "$(pwd)/data/pdf/"
cp -R $pdf_dir ../named_entity_recognizer/pdf/
cp -R $pdf_dir "$(pwd)/data/pdf/"

# Remove xhtml file from PDFNLT/xhtml
# rm -Rf "../PDFNLT/pdfanalyzer/xhtml/$pdf_name.xhtml"

# ###################### #
#      PROCESS TERMS     #
# ###################### #

echo "Creating training files for PDFs..."

for i in "${pdfs[@]}"
do
  pdf_name="$(basename "$i" .pdf)"
  touch -a "../PDFNLT/pdfanalyzer/train/$pdf_name.csv"
done

echo "Running PDFNLT postprocessing for $pdf_dir..."

# To DEBUG: bash -x prints all statements executed
# bash -x "$script/../PDFNLT/postprocess/postprocess.sh" "$pdf_dir"

rvm use jruby-9.1.13.0@pdfnlt

sh "../PDFNLT/postprocess/postprocess.sh" "$pdf_dir"

# TO DEBUG RUN SINGLE PAPER FOR NEXT EXECUTION
# rm "../PDFNLT/pdfanalyzer/train/TUD-LTE.csv"

# ########################################### #
#      CALCULATE TOP PAPERS & ENRICH XHTML    #
# ########################################### #

echo "Calculating top papers..."

# for i in "${pdfs[0]}"
# do
#   pdf_name="$(basename "$i" .pdf)"
#   python "enrich_xhtml/enrich_xhtml_main.py" $pdf_name $facet $number_papers
# done


mv -f "data/papers_terms_overview.csv" "data/papers_terms_overview_old.csv"
touch "data/papers_terms_overview.csv"
echo "paper_name,number_entities" >> data/papers_terms_overview.csv

pdf_name="$(basename "${pdfs[0]}" .pdf)"
python "enrich_xhtml/enrich_xhtml_main.py" $pdf_name $facet $number_papers


# TODO
# Generate paper_name_term_set.txt file for every pdf
# Add every pdf #occurances to papers_terms.csv
# Calculate top papers for terms and entities
# Separate sentence analysis and xhtml enrichtment
# Rename enrich_xhtml_main!!






# python enrich_xhtml/enrich_xhtml_main.py "$pdf_name" "$facet"

# echo "Copying enriched XHTML and JSON files to PDFNLT/pdfanalyzer..."

# mkdir -p ../PDFNLT/pdfanalyzer/xhtml
# cp -R "$script/data/xhtml/${pdf_name}.xhtml" ../PDFNLT/pdfanalyzer/xhtml/
# mkdir -p ../PDFNLT/pdfanalyzer/json_entities
# cp -R "$script/data/json/${pdf_name}_entities.json" ../PDFNLT/pdfanalyzer/json_entities/
# mkdir -p ../PDFNLT/pdfanalyzer/json_pdf_terms_pages
# cp -R "$script/data/json/${pdf_name}_pdf_terms_pages.json" ../PDFNLT/pdfanalyzer/json_pdf_terms_pages/

# echo "Updating www/pdfnlt data..."
# ln -f -s /Users/daniel/Documents/TUDelftMasterThesis/PDFNLT/pdfanalyzer/{pdf,xhtml,json_entities,json_pdf_terms_pages} '/usr/local/var/www/pdfnlt/pdfanalyzer/'

# # [DONE] Enrich XHTML with word-id to add attribute
# # [DONE] Add config file with meta-data about each word, or add all in xhtml attributes
# # When pushing to PDFNLT server: Make sure to run command to clear localstorage!
# # Chech with goran about textualize.rb xhtml_dir not being xhtml/ dir

# python -c 'import statistics; statistics.print_stats()'

# # echo "Extracting Named Entites..."
# # echo "Updating database annotation entry..."







