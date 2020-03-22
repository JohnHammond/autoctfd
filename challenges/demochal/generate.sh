#!/bin/bash

FLAG="thisisaflag"
echo $FLAG > flag.txt

qrencode -o afile.png "$FLAG"