#!/bin/bash

pdftoppm scan.pdf scan -png

python3 -m pip install deda

for img in scan-*.png
do
    awk "BEGIN{printf \"%c\", $(deda_parse_print "$img" | sed -nE 's/.*serial: -([0-9]+)-/\1/p')}"
done
