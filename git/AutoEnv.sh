#!/bin/bash

echo "hi" $1 $2
ls -l
echo $1
secs=70
SECONDS=0
while (( $SECONDS < $secs )); do
	echo "test $1"
	sleep 5
done
echo "test4"

