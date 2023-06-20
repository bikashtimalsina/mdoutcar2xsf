import os
import glob
import re
import sys
import shutil
from collections import Counter

""" Takes the train.cfg or test.cfg file from MTP as input.
    The train.cfg or test.cfg file should be provided as first
    Argument. """

fname=sys.argv[1]
file=open(fname)
filedata=''.join(file.readlines())
pattern_config="(?<=BEGIN_CFG)(.*?)(?=END_CFG)"
configs=re.findall(pattern_config,filedata,flags=re.S)
latt_pattern="(?<=Supercell)(.*?)(?=AtomData)"
lattice_raw=re.findall(latt_pattern,filedata,flags=re.S)
lattice=[lattice_raw[i].strip().split() for i in range(len(lattice_raw))]
energy_pattern="(?<=Energy)(.*?)(?=PlusStress)"
energy_raw=re.findall(energy_pattern,filedata,flags=re.S)
energy=[energy_raw[i].strip() for i in range(len(energy_raw))]
stress_pattern="(?<=xy)(.*?)(?=Feature)"
stress_raw=re.findall(stress_pattern,filedata,flags=re.S)
stress=[stress_raw[i].strip() for i in range(len(stress_raw))]
coords_pattern="(?<=fz)(.*?)(?=Energy)"
coords_raw=re.findall(coords_pattern,filedata,flags=re.S)
poscoord=[]
atomtype=[]
elematomtype=[]
for i in range(len(coords_raw)):
    coords=coords_raw[i].split("\n")
    eachpcos=[]
    indexnum=[]
    for j in range(1,len(coords)-1):
        eachpcos.append(coords[j].strip().split()[2:])
        indexnum.append(coords[j].strip().split()[1])
    total_type=dict(Counter(indexnum))
    if len(total_type) == 2:
        sym_indexnum=[]
        for j in range(len(indexnum)):
            if indexnum[j] == "0":
                sym_indexnum.append("Zr")
            if indexnum[j]== "1":
                sym_indexnum.append("B")
    if len(total_type) == 3:
        sym_indexnum=[]
        for j in range(len(indexnum)):
            if indexnum[j] == "0":
                sym_indexnum.append("Zr")
            if indexnum[j] == "1":
                sym_indexnum.append("Hf")
            if indexnum[j] == "2":
                sym_indexnum.append("B")
    elematomtype.append(sym_indexnum)
    atomtype.append(indexnum)
    poscoord.append(eachpcos)
if os.path.exists("./configs"):
    shutil.rmtree("./configs")
os.makedirs("./configs",exist_ok=True)
for i in range(len(poscoord)):
    filew="./configs/"+"out-{}".format(i+1)+".xyz"
    eachelemcount=dict(Counter(elematomtype[i]))
    if len(eachelemcount) == 3:
        if eachelemcount['Zr'] == eachelemcount['Hf']:
            with open(filew,"w") as file:
                file.writelines(str(len(poscoord[i])))
                file.writelines("\n")
                lattice_str="Lattice=\""+" ".join(lattice[i])+"\" "
                energy_str="Energy="+energy[i]+" "
                stress_str="Virial=\""+stress[i]+"\" "
                other_str="Properties=species:S:1:pos:R:3:force:R:3"
                allstring=lattice_str+energy_str+stress_str+other_str
                file.writelines(allstring)
                file.writelines("\n")
                for j in range(len(poscoord[i])):
                    file.writelines(elematomtype[i][j]+" "+" ".join(poscoord[i][j]))
                    file.writelines("\n") 
