#!/usr/bin/env bash

# Makes sure decimal numbers have a dot instead of a comma
LC_NUMERIC=C
STEPS=$1
SIMULATIONS=$2
ASSHOLE=$3
OUTPUT="./output"
ROUNDABOUTS=('regular' 'turbo' 'magic')

GREEN="\033[0;32m"
NC="\033[0m"

run_roundabout() {
    echo -n "density = $2..."
    $(./main.py $1 -d $2 -i $STEPS -s $SIMULATIONS -o output -m -A $ASSHOLE)
    echo -e "\t${GREEN}DONE${NC}"
}

main() {
    if [ ! -d "$OUTPUT" ]; then
        echo "creating output directory..."
        mkdir "$OUTPUT"
    fi

    echo "running roundaboutsim with $STEPS time steps and $SIMULATIONS simulations per density..."

    for r in "${ROUNDABOUTS[@]}"; do
        echo "========= $r =========="
        for d in $(seq 0.05 0.05 0.95); do
            run_roundabout $r $d
        done
    done
}

if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters. Please specify the number of time steps, the number of simulations and te asshole factor."
else
    main
fi
