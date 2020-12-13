#!/bin/sh

cd ../
sudo python setup.py clean --all
cat data/files.txt | sudo xargs rm -rf
