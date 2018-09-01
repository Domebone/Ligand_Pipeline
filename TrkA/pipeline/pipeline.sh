#!/bin/bash
mkdir pdbqt
mkdir pdb
python3 CSV_parser.py uncurated_list.csv && python3 ligand_converter.py

echo "Converting to pdbqt"

for ligand in $(ls pdb/*pdb); do
	
	ligandname=`echo "$ligand" | cut -d'.' -f1| cut -d'/' -f2`
	obabel $ligand -O pdbqt/$ligandname.pdbqt
	echo "Converted to pdbqt"
done

echo Ligand Prep Complete!

mkdir configs
mkdir output
mkdir logs

echo Creating Configuration File...
constant_suffix="_conf.txt"
for ligand in $(ls pdbqt/*pdbqt); do
	#echo $ligand
	ligandname=`echo "$ligand"|cut -d'/' -f2`
	
	bash ./conf_maker.sh $ligandname pdbqt configs output logs
	

	config_path="configs/${ligandname}_conf.txt"
	#config_path="$config_path$constant_suffix"
	
	echo Docking ${ligandname}...
	vina --config $config_path

done

#!/bin/bash
echo "">candidate_list.csv
echo "Computing Best Ligands..."
log_output="candidate_list.csv"
for file in $(ls logs/*.txt); do
	
	python3 log_reader.py $file $log_output
done

python3 evaluator.py candidate_list.csv 
echo "Primary eval complete"

mkdir modded_pdb
mkdir modded_pdbqt

python3 mol/improv-rando.py ../candidate_list.csv

for ligand in $(ls modded_pdb/*pdb); do
	
	ligandname=`echo "$ligand" | cut -d'.' -f1| cut -d'/' -f2`
	obabel $ligand -O modded_pdbqt/$ligandname.pdbqt
	echo "Converted to pdbqt"
done

mkdir modded_ligand_configs
mkdir modded_ligand_logs
mkdir modded_ligand_outputs

echo Creating New Configuration Files...
constant_suffix="_conf.txt"


for ligand in $(ls modded_pdbqt/*pdbqt); do
	#echo $ligand
	ligandname=`echo "$ligand"|cut -d'/' -f2`
	
	bash ./conf_maker.sh $ligandname modded_pdbqt modded_ligand_configs modded_ligand_outputs modded_ligand_logs
	

	config_path="modded_ligand_configs/${ligandname}_conf.txt"
	#config_path="$config_path$constant_suffix"
	
	echo Docking ${ligandname}...
	vina --config $config_path

done

log_output= "modded_candidate_list.csv"

for file in $(ls modded_ligand_logs/*.txt); do
	
	python3 log_reader.py $file $log_output
done

python3 post_modding_eval.py log_output	#this is the end of the pipeline