#!/bin/bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
[theme]\n\
primaryColor = '#1f77b4'\n\
backgroundColor = '#ffffff'\n\
secondaryBackgroundColor = '#f0f2f6'\n\
textColor = '#262730'\n\
" > ~/.streamlit/config.toml
