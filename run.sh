#!/bin/bash

if command -v python3 &> /dev/null; then
    python_cmd="python3"
else
    python_cmd="python"
fi

cd modules/payload/
$python_cmd -i contractpload.py

if [ $? -eq 0 ]; then
    cd ../..  # Move back to the root directory
    $python_cmd -i modules/flashloan.py
fi