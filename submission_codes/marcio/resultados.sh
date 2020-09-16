#!/bin/bash

DIR="$(ls -d ../*/)"
I=0

for cases in $DIR
do
    case $I in
    7500) break
          ;;
    *) python resultados.py "${cases%?}"
       ;;         
    esac

    I=$I+1
done

exit 0

