#/bin/bash

# ############## #
#      SETUP     #
# ############## #

if [[ -z "$1" ]]
then
  echo -e "Usage: $0 [-f] <pdf/pdf_file>"
  exit -1
fi

script=$(cd $(dirname $0) && pwd)


# ##################### #
#      DEPENDENCIES     #
# ##################### #

echo "Checking Dependencies..."
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

pdf_file=$1
pdf_name="$(basename "$pdf_file" .pdf)"

# echo $filename
# pdf_name = ${$1%.*}
# print pdf_name

# #################### #
#      PROCESS PDF     #
# #################### #

echo "Processing PDF..."

# Remove copy pdf to PDFNLT and NER
cp -R $pdf_file ../PDFNLT/pdf/
cp -R $pdf_file ../named_entity_recognizer/pdf/

# Remove xhtml file from PDFNLT/xhtml
rm -Rf "$script/../PDFNLT/xhtml/$pdf_name.xhtml"

# ###################### #
#      PROCESS TERMS     #
# ###################### #

sh "$script/../PDFNLT/postprocess/postprocess.sh" "$pdf_file"

# Run Postprocess with PDF file
# Read Terms
# combine terms
# Copy XHTML and text
# COMBINE


# bash "$script/../PDFNLT/postprocess/postprocess.sh"




# echo "Extracting Named Entites..."
# echo "Annotating XHTML with VES..."
# echo "Updating database annotation entry..."




