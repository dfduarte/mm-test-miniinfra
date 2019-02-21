#!/bin/bash

while true; do
   echo "Pooling..."
   cd /worker
   python ./main.py
done