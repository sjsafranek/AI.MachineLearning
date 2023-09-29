#!/bin/bash

scripts=($(find scripts/*.sh))
for script in "${scripts[@]}"; do
	echo "Executing -- $script"
	eval $script
done