#!/bin/bash

SITES=( "https://github.com/vega/vega-datasets.git" "https://github.com/vega/vega-lite.git" )

for site in "${SITES[@]}"
do
    git clone --depth=1 $site
done

