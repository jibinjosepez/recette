#!/bin/bash

# Script to download recipes scrapped from the website www.marimiton.org
# Data will be stored  under path provided as variable or under  ../data


location="${1:-../data}"
wget --directory-prefix=/tmp/recipe  https://d1sf7nqdl8wqk.cloudfront.net/recipes.json.gz &&  gzip -dc /tmp/recipe/recipes.json.gz > $location/recipes.json && rm -r /tmp/recipe

