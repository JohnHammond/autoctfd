#!/bin/bash

FLAG="anotherflag"
echo $FLAG > flag.txt

echo $FLAG | rot13 > prompt.txt
