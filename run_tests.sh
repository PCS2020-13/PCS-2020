#!/usr/bin/env bash

STEPS=250
SIMULATIONS=5
OUTPUT="output"
ROUNDABOUTS=('regular' 'turbo' 'magic')

GREEN="\033[0;32m"
NC="\033[0m"

run_roundabout() {
    echo -n "density = $2..."
    $(./main.py $1 -d $2 -i $STEPS -s $SIMULATIONS -o output -m)
    echo -e "\t${GREEN}DONE${NC}"
}

for r in "${ROUNDABOUTS[@]}"; do
    echo "========= $r =========="
    for d in $(seq 0.1 0.1 0.9); do
        run_roundabout $r $d
    done
done
