#!/bin/bash

if [ ! -d "tenderx_venv" ]; then
    echo "Virtual environment not found. Creating and installing dependencies..."
    
    python3 -m venv tenderx_venv

    source ./tenderx_venv/bin/activate

    pip install -r ./tenderx/requriements.txt
else
    echo "Virtual environment found. Activating..."
    source ./tenderx_venv/bin/activate
fi

echo "Running TenderX..."
streamlit run tenderx/tender.py