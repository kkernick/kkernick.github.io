#!/bin/bash

# Unsurprisingly, ShinyLive doesn't support symlinks. Therefore, just copy them
for project in "expression" "geocoordinate" "geomap" "image" "pairwise"; do
	cp "./shared/shared.py" "./${project}/src/shared.py"
done