#!/bin/bash
log_output="modded_candidate_list.csv"

for file in $(ls modded_ligand_logs/*.txt); do
	
	python3 log_reader.py $file ${log_output}
done