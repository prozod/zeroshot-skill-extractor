#!/bin/bash

python3 retrieve_cookie.py

li_at_cookie=$(cat ./li_at.txt)

LI_AT_COOKIE="$li_at_cookie" python3 scraper.py --query "$1" --location "$2" --limit 10
