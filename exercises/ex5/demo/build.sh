#!/bin/bash

for f in *.c; do
	name=$(echo $f | cut -d. -f1)
	cc $CFLAGS $name.c -o $name 2> /dev/null
done
