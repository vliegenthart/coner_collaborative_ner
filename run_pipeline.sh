#/bin/bash

# ############## #
#      SETUP     #
# ############## #

if [[ -z "$1" ]] || [[ -z "$2" ]]
then
  echo -e "Usage: $0 [-f] <../PDFNLT/pdfanalyzer/pdf/pdf_name> <facet_name>"
  exit -1
fi

script=$(cd $(dirname $0) && pwd)

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
  echo "✓ PDF"
else
  echo -e "PDF file not found"
  exit -1
fi

echo ""

pdf_file=$1
pdf_name="$(basename "$pdf_file" .pdf)"

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
echo "Copying PDF file to PDFNLT and NER..."
cp -R $pdf_file ../named_entity_recognizer/pdf/

# Remove xhtml file from PDFNLT/xhtml
# rm -Rf "../PDFNLT/pdfanalyzer/xhtml/$pdf_name.xhtml"

# ###################### #
#      PROCESS TERMS     #
# ###################### #

echo "Running PDFNLT postprocessing for $pdf_file..."

# To DEBUG: bash -x prints all statements executed
# bash -x "$script/../PDFNLT/postprocess/postprocess.sh" "$pdf_file"

sh "$script/../PDFNLT/postprocess/postprocess.sh" "$pdf_file"

python enrich_xhtml/enrich_xhtml_main.py "$pdf_name" "$2"

echo "Copying enriched XHTML and JSON files to PDFNLT/pdfanalyzer..."

mkdir -p ../PDFNLT/pdfanalyzer/xhtml
cp -R "$script/data/xhtml/${pdf_name}.xhtml" ../PDFNLT/pdfanalyzer/xhtml/
mkdir -p ../PDFNLT/pdfanalyzer/json_entities
cp -R "$script/data/json/${pdf_name}_entities.json" ../PDFNLT/pdfanalyzer/json_entities/
mkdir -p ../PDFNLT/pdfanalyzer/json_pdf_terms_pages
cp -R "$script/data/json/${pdf_name}_pdf_terms_pages.json" ../PDFNLT/pdfanalyzer/json_pdf_terms_pages/

echo "Updating www/pdfnlt data..."
ln -f -s /Users/daniel/Documents/TUDelftMasterThesis/PDFNLT/pdfanalyzer/{pdf,xhtml,json_entities,json_pdf_terms_pages} '/usr/local/var/www/pdfnlt/pdfanalyzer/'

# [DONE] Enrich XHTML with word-id to add attribute
# [DONE] Add config file with meta-data about each word, or add all in xhtml attributes
# When pushing to PDFNLT server: Make sure to run command to clear localstorage!

python -c 'import statistics; statistics.print_stats()'

# echo "Extracting Named Entites..."
# echo "Updating database annotation entry..."




