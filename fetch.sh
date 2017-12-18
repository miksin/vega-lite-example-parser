#!/bin/sh

# Clean files
rm -Rf data
rm -Rf specs
rm -Rf vega-datasets
rm -Rf vega-lite

git clone --depth=1 https://github.com/vega/vega-datasets.git
git clone --depth=1 https://github.com/vega/vega-lite.git

mv vega-datasets/data .
mv vega-lite/examples/specs .

rm -Rf vega-datasets
rm -Rf vega-lite
