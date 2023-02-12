import numpy as np
import os
import sys
from ase.io import read
import re
fname=sys.argv[1]
xyzdata=read(fname)

def write_trajectory(fname):
	lattice=[]
	force=[]
	stress_str=[]
	counter=1
	with open(fname,"r") as file:
		for line in file:
			if counter==2:
				latstress=re.findall(r'"(.*?)"',line)
				lattice=np.float64(latstress[0].split())
				stress_str=np.float64(latstress[1].split())
				energy=format(float(re.findall(r'Energy=(.*?) Virial',line)[0]),'.6f')
			if counter>2:
				force.append([format(float(line.split()[4]),'.6f'),format(float(line.split()[5]),'.6f'),format(float(line.split()[6]),'.6f')])
			counter += 1
	file.close()
	stress_f=[float(stress_str[i]) for i in range(len(stress_str))]
	stress_cfg=[stress_f[0],stress_f[4],stress_f[8],stress_f[5],stress_f[2],stress_f[1]]
	stress=[format(stress_cfg[i],'.6f') for i in range(len(stress_cfg))]
	xyzdata=read(fname)
	cell=xyzdata.cell
	nions=xyzdata.get_global_number_of_atoms()
	typemtp=[xyzdata.symbols[i] for i in range(len(xyzdata.symbols))]
	typemap=list(dict.fromkeys(typemtp))
	typemapdict={}
	for index,elem in enumerate(typemap):
		typemapdict[elem]=index
	typemapdictKeys=list(typemapdict.keys())
	typemtpNum=[i for i in range(len(typemtp))]
	for i in range(len(typemtp)):
		for j in range(len(typemapdictKeys)):
			if typemtp[i]==typemapdictKeys[j]:
				typemtpNum[i]=typemapdict[typemtp[i]]
	print(typemtp)
	print(typemtpNum)
	pos=xyzdata.get_positions()
	npos=[]
	nforce=[]
	for i in range(nions):
		npos.append([format(pos[i][0],'.6f'),format(pos[i][1],'.6f'),format(pos[i][2],'.6f')])
		nforce.append([format(float(force[i][0]),'.6f'),format(float(force[i][1]),'.6f'),format(float(force[i][2]),'.6f')])
	flat_distance_array=np.unique(np.array(xyzdata.get_all_distances()).reshape((1,nions*nions))[0])
	min_distance=flat_distance_array[1]
	each_fwrite="./out.cfg"
	with open(each_fwrite,"w") as file:
		file.writelines("BEGIN_CFG")
		file.writelines("\n")
		file.writelines(" Size")
		file.writelines("\n")
		file.writelines("\t {}".format(nions))
		file.writelines("\n")
		file.writelines(" Supercell")
		file.writelines("\n")
		file.writelines("\t\t {} {} {}".format(format(cell[0][0],'.6f'),format(cell[0][1],'.6f'),format(cell[0][2],'.6f')))
		file.writelines("\n")
		file.writelines("\t\t {} {} {}".format(format(cell[1][0],'.6f'),format(cell[1][1],'.6f'),format(cell[1][2],'.6f')))
		file.writelines("\n")
		file.writelines("\t\t {} {} {}".format(format(cell[2][0],'.6f'),format(cell[2][1],'.6f'),format(cell[2][2],'.6f')))
		file.writelines("\n")
		file.writelines(" AtomData:  id type  cartes_x    cartes_y    cartes_z    fx          fy          fz")
		file.writelines("\n")
		for k in range(nions):
			index="\t\t\t"+str(k+1)
			if len(index)==5:
				ist='{0: '+'>'+"{}".format(len(index)-1)+'}'
				ind=ist.format(index)
				file.writelines("{} \t {} \t {} \t {} \t {} \t {} \t {} \t {}".format(ind,typemtpNum[k],npos[k][0],npos[k][1],npos[k][2],nforce[k][0],nforce[k][1],nforce[k][2]))
			if len(index)==4:
				ist='{0: '+'>'+"{}".format(len(index))+'}'
				ind=ist.format(index)			
				file.writelines("{} \t {} \t {} \t {} \t {} \t {} \t {} \t {}".format(ind,typemtpNum[k],npos[k][0],npos[k][1],npos[k][2],nforce[k][0],nforce[k][1],nforce[k][2]))
			file.writelines("\n")
		file.writelines(" Energy")
		file.writelines("\n")
		file.writelines("\t {}".format(energy))
		file.writelines("\n")
		file.writelines(" PlusStress:  xx          yy          zz          yz          xz          xy")
		file.writelines("\n")
		file.writelines("\t\t {} \t {} \t {} \t {} \t {} \t {}".format(stress[0],stress[1],stress[2],stress[3],stress[4],stress[5]))
		file.writelines("\n")
		file.writelines(" Feature   EFS_by   VASP")
		file.writelines("\n")
		file.writelines(" Feature   mindist  {}".format(format(min_distance,'.8f')))
		file.writelines("\n")
		file.writelines("END_CFG")
		file.writelines("\n")
		file.writelines("\n")
	file.close()
write_trajectory(fname)
# Ni-0, Zn-1, Cu-2, mg-3, Co-4, O-5