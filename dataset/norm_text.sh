#!/usr/bin/env bash
#this function will convert text to lowercase and will disconnect punctuation and special symbols from words
function normalize_text {
  awk '{print tolower($0);}' < $1 | sed -e 's/\./ \. /g' -e 's/<br \/>/ /g' -e 's/"/ " /g' \
  -e 's/,/ , /g' -e 's/(/ ( /g' -e 's/)/ ) /g' -e 's/\!/ \! /g' -e 's/\?/ \? /g' \
  -e 's/\;/ \; /g' -e 's/\:/ \: /g' > $1-norm
}

rm -r data/
mkdir data
for j in `ls 20newsgroup`; do
  mkdir data/$j
  for i in `ls 20newsgroup/$j`; do cat 20newsgroup/$j/$i >> temp; awk 'BEGIN{print;}' >> temp; done
  normalize_text temp
  mv temp-norm data/$j/norm
  rm temp
done
