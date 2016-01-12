#!/bin/bash

echo "generating fake dataset..."

python process.py
python process2.py
python process3.py

mkdir Fake2 
mv Original/*2.json Fake2

echo "Done"
