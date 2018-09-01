#!/bin/bash



#the file needs to take the reptor name so at the step

#where there is going to be binding estimation we need

#to create this file



#identify the receptor ID -> will be a constant for the whole run of course



RECEPTOR_ID=receptor/1wwa.pdbqt

#eg output: receptor= protein.pdbqt



#identify the ligand ID -> will have to vary for every run



LIGAND_ID=$2/$1


#eg output: ligand= SO.pdbqt



#we will decide the universal coordinates

center_x='-36'

center_y='76.07'

center_z='20.47'



size_x='38'

size_y='44'

size_z='44'





#generate the conf.txt



{



echo receptor= ${RECEPTOR_ID}

echo ligand= ${LIGAND_ID}

echo ''

echo ''

echo ''

echo center_x= ${center_x}

echo ''

echo center_y= ${center_y}

echo ''

echo center_z= ${center_z}

echo ''

echo ''

echo ''

echo size_x= ${size_x}

echo ''

echo size_y= ${size_y}

echo ''

echo size_z= ${size_z}

echo ''

echo ''

echo ''

echo out= ${4}/${1}

echo ''

echo ''

echo log= ${5}/${1}.txt

echo ''

echo ''

echo exhaustiveness= 8

echo energy_range= 4

#default is = 8

#With the default (or any given) setting of exhaustiveness, the time spent on the search is already varied heuristically depending on the number of atoms, flexibility, etc. Normally, it does not make sense to spend extra time searching to reduce the probability of not finding the global minimum of the scoring function beyond what is significantly lower than the probability that the minimum is far from the native conformation. However, if you feel that the automatic trade-off made between exhaustiveness and time is inadequate, you can increase the exhaustiveness level. This should increase the time linearly and decrease the probability of not finding the minimum exponentially.

} >${3}/${1}_conf.txt

