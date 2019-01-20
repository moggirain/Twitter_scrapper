while IFS="" read -r p || [ -n "$p" ]
do
  ./run.sh "$p"
done < $1
