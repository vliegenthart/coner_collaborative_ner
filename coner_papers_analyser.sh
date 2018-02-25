#/bin/bash

# BEFORE RUNNING THIS SCRIPT, MAKE SURE ALL PDF FILES AND PDF_NAME_entities.json ARE THERE!

# ############## #
#      SETUP     #
# ############## #

script=$(cd $(dirname $0) && pwd)

usage() {
  echo -e "Usage: $0 [-f] ../PDFNLT/pdfanalyzer/pdf <facet_name>"
  echo -e "   or  $0 [-f] ../PDFNLT/pdfanalyzer/pdf/<pdf_file> <facet_name>"
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

if [[ -z "$1" ]] || [[ -z "$2" ]]
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

echo ""

pdf_dir=$1


# #################### #
#      PROCESS PDF     #
# #################### #


echo "Setting up statistics...\n"
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

echo "Running PDFNLT postprocessing for $pdf_dir..."

# python create_training_files.py ""



# touch -a "../PDFNLT/pdfanalyzer/train/$pdf_name.csv"

# # To DEBUG: bash -x prints all statements executed
# bash -x "$script/../PDFNLT/postprocess/postprocess.sh" "$pdf_dir"

# sh "$script/../PDFNLT/postprocess/postprocess.sh" "$pdf_dir"

# python enrich_xhtml/enrich_xhtml_main.py "$pdf_name" "$2"

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







# #/bin/bash

# ############## #
#      SETUP     #
# ############## #

# if [[ -z "$1" ]] || [[ -z "$2" ]]
# then
#   echo -e "Usage: $0 [-f] <../PDFNLT/pdfanalyzer/pdf> <facet_name>"
#   exit -1
# fi

# script=$(cd $(dirname $0) && pwd)






