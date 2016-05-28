#!/usr/bin/env bash

test=()
labels=(`ls 20newsgroup`)
#echo "size: ${labels}"
while [${#test[@]} < 10];
do
  echo $RANDOM
done

for i in {1..5}; do echo $(( RANDOM %= 10)); done