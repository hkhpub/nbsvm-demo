#!/usr/bin/env bash
#this function will convert text to lowercase and will disconnect punctuation and special symbols from words
function normalize_text {
  awk '{print tolower($0);}' < $1 | sed -e 's/\./ \. /g' -e 's/<br \/>/ /g' -e 's/"/ " /g' \
  -e 's/,/ , /g' -e 's/(/ ( /g' -e 's/)/ ) /g' -e 's/\!/ \! /g' -e 's/\?/ \? /g' \
  -e 's/\;/ \; /g' -e 's/\:/ \: /g' > $1-norm
}

rm -r data2/
mkdir data2
for j in `ls devset`; do
  mkdir data2/$j
  for i in `ls devset/$j`; do cat devset/$j/$i >> temp; awk 'BEGIN{print;}' >> temp; done
  `tr '\n\n' ' ' < temp` >> temp
  normalize_text temp
  mv temp-norm data2/$j/norm
  rm temp
done
