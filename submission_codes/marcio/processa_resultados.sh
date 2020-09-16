#!/bin/bash

casos="$(ls ../)"

for caso in $casos; do
    python resultados.py "../$caso"
done
