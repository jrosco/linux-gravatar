#!/bin/sh

sudo python setup.py clean --all
cat data/files.txt | sudo xargs rm -rf
