#!/usr/bin/env bash
echo "======================================================"
echo "             Rule-Based Chatbot (PyBot)"
echo "======================================================"
echo ""

# Fast dependency check
python3 -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[Checking and installing Python dependencies...]"
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies."
        exit 1
    fi
fi

echo ""
echo "[Launching application in dedicated window...]"
python3 launch.py
