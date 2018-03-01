#/bin/bash

# BEFORE RUNNING THIS SCRIPT, MAKE SURE ALL PDF FILES AND PDF_NAME_entities.json ARE THERE!
# Retrain PDFNLT so all training CSV's are there!

# TODO
# Do XHTML enrichtment after calculating top papers, not before!
# Change all 'ocurrances' to 'occurrences'
# Balance papers that are used equally from all 10 journals before taking top!!!

# ############## #
#      SETUP     #
# ############## #

script=$(cd $(dirname $0) && pwd)

# <pdf_directory>: ../PDFNLT/pdfanalyzer/pdf/

usage() {
  echo -e "Usage: $0 [-e] <database> <facet_name> <pdf_directory> <number_top_papers>"
}

unset force
unset enrich

while getopts "e" o; do
  case "${o}" in
    e)
      enrich=1
      ;;
    *)
      usage
      exit 1
      ;;
  esac
done
shift $((OPTIND-1))

if [[ -z "$1" ]] || [[ -z "$2" ]] || [[ -z "$3" ]] || [[ -z "$4" ]]
then
  usage
  exit 1
fi

xhtmls=()
shopt -s nullglob

if [ -d "$3" -a -n "$force" ]
then
  # Whole directory, forced
  dir="$(cd $(dirname "$3") && pwd)"
  outdir="${outdir:-$dir/text}"
  pdfs=(--all)
  tsvs=(--all)
else
  if [ -f "$3" ]
  then
    # Individual files
    dir=$(cd $(dirname "$3")/.. && pwd)
    files=("$3")
  else
    # Whole directory, non-forced
    dir="$(cd $(dirname "$3") && pwd)"
    files=("$dir/$1"_pdf/*.pdf)
  fi
  outdir="${outdir:-$dir/text}"

  pdfs=()

  tsvs=()

  for i in "${files[@]}"
  do
    # If not forced, then only pick the files that are not up-to-date
    file="$(basename "$i" .xhtml)"
    file="${file%.pdf}"
    if [ -f "$dir/$1_pdf/$file.pdf" -o -n "$force" ]
    then
      pdfs+=("$dir/$1_pdf/$file.pdf")
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

if [ -e "$script/$3" ]; then
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

database=$1
facet=$2
pdf_dir=$3
number_top_papers=$4

echo "Variables:"
echo "DATABASE: $database"
echo "FACET: $facet"
echo "PDF_DIR: $pdf_dir"
echo "NUMBER_TOP_PAPERS: $number_top_papers"

# ##################### #
#      PROCESS PDFS     #
# ##################### #

echo $'Setting up statistics...\n'
mkdir -p "logging"
cp -R "logging/statistics.log" "logging/OLD_statistics.log" || :
rm "logging/statistics.log"
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

# Backup versions of occurances overviews from last execution
cp -R "data/${database}/${facet}_papers_occurances_overview.csv" "data/${database}/OLD_${facet}_papers_occurances_overview.csv" || :
cp -R "data/${database}/${facet}_top_papers_overview.csv" "data/${database}/OLD_${facet}_top_papers_overview.csv" || :

if [ -n "$enrich" ]
then
  echo "Analysing term occurances in papers and enriching XHTMLs..."

  cp -R "data/${database}/${facet}_papers_terms_overview.csv" "data/${database}/OLD_${facet}_papers_terms_overview.csv"
  rm -f "data/${database}/${facet}_papers_terms_overview.csv"
  touch "data/${database}/${facet}_papers_terms_overview.csv"
  echo "paper_id,number_terms" >> "data/${database}/${facet}_papers_terms_overview.csv"

  mkdir -p ../PDFNLT/pdfanalyzer/xhtml
  mkdir -p ../PDFNLT/pdfanalyzer/json_entities
  mkdir -p ../PDFNLT/pdfanalyzer/json_pdf_terms_pages

  for i in "${pdfs[0]}"
  do
    pdf_name="$(basename "$i" .pdf)"

    python "enrich_xhtml/enrich_xhtml_main.py" $database $facet $pdf_name 
    
    cp -R "$(pwd)/data/${database}/xhtml/${pdf_name}.xhtml" ../PDFNLT/pdfanalyzer/xhtml/
    cp -R "$(pwd)/data/${database}/json/${facet}_${pdf_name}_entities.json" ../PDFNLT/pdfanalyzer/json_entities/
    cp -R "$(pwd)/data/${database}/json/${facet}_${pdf_name}_pdf_terms_pages.json" ../PDFNLT/pdfanalyzer/json_pdf_terms_pages/
  done

  python -c 'import statistics; statistics.print_stats()'
else
  echo "Term occurances in papers and enriched XHTMLs are up-to-date"
fi

echo "Calculating top papers..."

python calculate_top_papers.py $database $facet $number_top_papers

# TODO
# [DONE] TEST FORCE AND ENRICH FLAGS
# [DONE] Generate paper_name_term_set.txt file for every pdf
# [DONE] Add every pdf #occurances to papers_terms.csv (also change above code to loop)
# [DONE] Calculate top papers for terms and entities
# [LATER] Separate sentence analysis and xhtml enrichtment
# [LATER] Rename enrich_xhtml_main!!
# [DONE] Enrich XHTML with word-id to add attribute
# [DONE] Add config file with meta-data about each word, or add all in xhtml attributes
# When pushing to PDFNLT server: Make sure to run command to clear localstorage!
# Chech with goran about textualize.rb xhtml_dir not being xhtml/ dir


# echo "Updating www/pdfnlt data..."
# ln -f -s /Users/daniel/Documents/TUDelftMasterThesis/PDFNLT/pdfanalyzer/{pdf,xhtml,json_entities,json_pdf_terms_pages} '/usr/local/var/www/pdfnlt/pdfanalyzer/'
