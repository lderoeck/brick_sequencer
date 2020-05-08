#/usr/bin/env bash
IFS=$'\n'
set -f
echo $PWD
source ./.venv/bin/activate;
cd src/;
j=1
for i in $(cat < "../$1"); do
	git checkout "$i"
	git checkout master ../Accuracy.py
	mkdir -p ../accuracyResults;
	touch ../accuracyResults/Result.txt;
	python ../Accuracy.py;
	printf -v k "%02d" $j
	mv ../accuracyResults/Result.txt "../result-$k-$i.txt";
	let j=j+1
done;
deactivate;

