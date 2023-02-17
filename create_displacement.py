import numpy as np
import sys
import glob
import sys
from os import system
import shutil
import os
elements={'H': '1.007', 'He': '4.002', 'Li': '6.941', 'Be': '9.012', 'B': '10.811', 
'C': '12.011', 'N': '14.007', 'O': '15.999', 'F': '18.998', 'Ne': '20.18', 'Na': '22.99',
 'Mg': '24.305', 'Al': '26.982', 'Si': '28.086', 'P': '30.974', 'S': '32.065', 'Cl': '35.453', 
 'Ar': '39.948', 'K': '39.098', 'Ca': '40.078', 'Sc': '44.956', 'Ti': '47.867', 'V': '50.942', 
 'Cr': '51.996', 'Mn': '54.938', 'Fe': '55.845', 'Co': '58.933', 'Ni': '58.693', 'Cu': '63.546',
  'Zn': '65.38', 'Ga': '69.723', 'Ge': '72.64', 'As': '74.922', 'Se': '78.96', 'Br': '79.904',
   'Kr': '83.798', 'Rb': '85.468', 'Sr': '87.62', 'Y': '88.906', 'Zr': '91.224', 'Nb': '92.906',
    'Mo': '95.96', 'Tc': '98', 'Ru': '101.07', 'Rh': '102.906', 'Pd': '106.42', 'Ag': '107.868', 
    'Cd': '112.411', 'In': '114.818', 'Sn': '118.71', 'Sb': '121.76', 'Te': '127.6', 'I': '126.904',
     'Xe': '131.293', 'Cs': '132.905', 'Ba': '137.327', 'La': '138.905', 'Ce': '140.116', 'Pr': '140.908',
      'Nd': '144.242', 'Pm': '145', 'Sm': '150.36', 'Eu': '151.964', 'Gd': '157.25', 'Tb': '158.925', 'Dy': '162.5',
       'Ho': '164.93', 'Er': '167.259', 'Tm': '168.934', 'Yb': '173.054', 'Lu': '174.967', 'Hf': '178.49', 'Ta': '180.948',
        'W': '183.84', 'Re': '186.207', 'Os': '190.23', 'Ir': '192.217', 'Pt': '195.084', 'Au': '196.967', 
        'Hg': '200.59', 'Tl': '204.383', 'Pb': '207.2', 'Bi': '208.98', 'Po': '210', 'At': '210', 
        'Rn': '222', 'Fr': '223', 'Ra': '226', 'Ac': '227', 'Th': '232.038', 'Pa': '231.036',
         'U': '238.029', 'Np': '237', 'Pu': '244', 'Am': '243', 'Cm': '247', 'Bk': '247', 
         'Cf': '251', 'Es': '252', 'Fm': '257', 'Md': '258', 'No': '259', 'Lr': '262',
          'Rf': '261', 'Db': '262', 'Sg': '266', 'Bh': '264', 'Hs': '267', 'Mt': '268',
           'Ds ': '271', 'Rg ': '272', 'Cn ': '285', 'Nh': '284', 'Fl': '289', 'Mc': '288', 'Lv': '292', 'Ts': '295', 'Og': '294'}
try:
	fname=sys.argv[1]
	if fname[-1]=="/":
		fname=fname
	else:
		fname=fname+"/"
except:
	print("Input directory name")
	sys.exit()
alldirs=glob.glob(fname+"**/"+"POSCAR*",recursive=True)
elem_order=[]
for i in range(len(alldirs)):
	with open(alldirs[i],"r") as file:
		counter=0
		for line in file:
			if counter == 5:
				elem_order.append(line.split())
			counter += 1
	file.close()
potcar_dir="~/Potpaw_PBE/"
pot_dir_path=[]
for i in range(len(elem_order)):
	each_dir=[]
	for j in range(len(elem_order[i])):
		each_dir.append(potcar_dir+elem_order[i][j]+"/POTCAR")
	pot_dir_path.append(each_dir)
if os.path.exists("./EachDisplacement"):
	shutil.rmtree("./EachDisplacement")
os.mkdir("./EachDisplacement")
for i in range(len(pot_dir_path)):
	dirname="./EachDisplacement/"+"{}".format(i+1)
	os.makedirs(dirname,exist_ok=True)
	potcarname=dirname+"/POTCAR"
	fcat="cat {} {} {} > {}".format(pot_dir_path[i][0],pot_dir_path[i][1],pot_dir_path[i][2],potcarname)
	system(fcat)
	poscarData=[]
	with open(alldirs[i],"r") as file:
		for line in file:
			poscarData.append(line.strip().split())
	file.close()
	scalefactor=poscarData[2][0]
	ntype=len(poscarData[5])
	atoms=poscarData[5]
	natoms=poscarData[6]
	coordinates=poscarData[8:]
	cellinpf=dirname+"/cell.inp"
	with open(cellinpf,"w") as file:
		file.writelines("1 1 1 90 90 90")
		file.writelines("\n")
		file.writelines("1 0 0 0 1 0 0 0 1")
		file.writelines("\n")
		file.writelines(scalefactor)
		file.writelines("\n")
		file.writelines(str(ntype))
		file.writelines("\n")
		file.writelines("{} {} {}".format(natoms[0],natoms[1],natoms[2]))
		file.writelines("\n")
		file.writelines("{} {} {}".format(elements[atoms[0]],elements[atoms[1]],elements[atoms[2]]))
		file.writelines("\n")
		for i in range(len(coordinates)):
			file.writelines("{} {} {} {}".format(coordinates[i][0],coordinates[i][1],coordinates[i][2],coordinates[i][3]))
			file.writelines("\n")
	file.close()
	with open(dirname+"/supercell.inp","w") as file:
		supercellsize=1
		file.writelines("{} 0 0".format(supercellsize))
		file.writelines("\n")
		file.writelines("0 {} 0".format(supercellsize))
		file.writelines("\n")
		file.writelines("0 0 {}".format(supercellsize))
	file.close()
	with open(dirname+"/snaps.inp","w") as file:
		freq=400
		temperature=300
		primcell=1
		nsnap=11
		file.writelines(str(freq))
		file.writelines("\n")
		file.writelines(str(temperature))
		file.writelines("\n")
		file.writelines("{} {}".format(primcell,nsnap))
	file.close()