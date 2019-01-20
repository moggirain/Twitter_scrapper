#!/bin/zsh

python Main.py -s 2015-01-01 -e 2019-01-01 -m 1000000 --outdir out/$1 --batchsize 1000 --randsleep 100 $1
