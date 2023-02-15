import numpy as np
import sys
import glob
import re

def extract_fit(fnvasp,fnmtp):
	data_vasp=[]
	data_mtp=[]
	begin_index=[]
	end_index=[]
	beg_tag="BEGIN_CFG"
	end_tag="END_CFG"
	count=0
	with open(fnvasp,"r") as file:
		for line in file:
			beg_found=re.findall(beg_tag,line)
			if len(beg_found) > 0:
				begin_index.append(count)
			end_found=re.findall(end_tag,line)
			if len(end_found) > 0:
				end_index.append(count)
			data_vasp.append(line.strip())
			count += 1
	file.close()
	with open(fnmtp,"r") as file:
		for line in file:
			data_mtp.append(line.strip())
	file.close()
	each_config_vasp=[]
	each_config_mtp=[]
	for i in range(len(begin_index)):
		temp_config_vasp=data_vasp[begin_index[i]:end_index[i]+1]
		each_config_vasp.append(temp_config_vasp)
		temp_config_mtp=data_mtp[begin_index[i]:end_index[i]+1]
		each_config_mtp.append(temp_config_mtp)
	energy_all_vasp=[]
	force_all_vasp=[]
	stress_all_vasp=[]
	energy_all_mtp=[]
	force_all_mtp=[]
	stress_all_mtp=[]
	for i in range(len(each_config_vasp)):
		nions=int(each_config_vasp[i][2])
		energyV=each_config_vasp[i][8+nions+1]
		energyM=each_config_mtp[i][8+nions+1]
		energy_all_vasp.append(energyV)
		energy_all_mtp.append(energyM)
		force_tempV=each_config_vasp[i][8:nions+8]
		force_tempM=each_config_mtp[i][8:nions+8]
		onlyForceV=[]
		onlyForceM=[]
		for j in range(len(force_tempV)):
			temp_V=force_tempV[j].split()[5:8]
			temp_M=force_tempM[j].split()[5:8]
			onlyForceV.append(temp_V)
			onlyForceM.append(temp_M)
		force_all_vasp.append(onlyForceV)
		force_all_mtp.append(onlyForceM)
		stress_tempV=each_config_vasp[i][8+nions+3].split()
		stress_tempM=each_config_mtp[i][8+nions+3].split()
		stress_all_vasp.append(stress_tempV)
		stress_all_mtp.append(stress_tempM)
	return energy_all_vasp,energy_all_mtp,force_all_vasp,force_all_mtp,stress_all_vasp,stress_all_mtp

fnvasp=sys.argv[1]
fnmtp=sys.argv[2]
energy_all_vasp,energy_all_mtp,force_all_vasp,force_all_mtp,stress_all_vasp,stress_all_mtp=extract_fit(fnvasp,fnmtp)
with open("output_energy.txt","w") as file:
	file.writelines("MTP energy (eV), VASP energy(eV)")
	file.writelines("\n")
	for i in range(len(energy_all_vasp)):
		file.writelines("{} {}".format(energy_all_mtp[i],energy_all_vasp[i]))
		file.writelines("\n")
file.close()
with open("output_force.txt","w") as file:
	file.writelines("MTP force (eV/A) (x, y, z), VASP force (eV/A) (x, y, z)")
	file.writelines("\n")
	for i in range(len(force_all_vasp)):
		for j in range(len(force_all_vasp[i])):
			fvx=force_all_vasp[i][j][0]
			fvy=force_all_vasp[i][j][1]
			fvz=force_all_vasp[i][j][2]
			fmx=force_all_mtp[i][j][0]
			fmy=force_all_mtp[i][j][1]
			fmz=force_all_mtp[i][j][2]
			file.writelines("{} {} {} {} {} {}".format(fmx,fmy,fmz,fvx,fvy,fvz))
			file.writelines("\n")
file.close()
with open("output_stress.txt","w") as file:
	file.writelines("MTP stress (eV), VASP stress (eV)")
	file.writelines("\n")
	for i in range(len(stress_all_vasp)):
		for j in range(len(stress_all_vasp[i])):
			file.writelines("{} {}".format(stress_all_mtp[i][j],stress_all_vasp[i][j]))
			file.writelines("\n")
file.close()
