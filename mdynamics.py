import numpy as np
import sys
import glob
#import ase
import re
import shutil
import os
#from ase import Atoms

class mtpoutcar:
    def __init__(self,filename,indrm):
        self.filename=filename
        self.indrm=indrm
    def get_sysinfo_energy(self):
        energy_text=[]
        nions=[]
        ionspertype=[]
        ionname=[]
        stress=[]
        with open(self.filename,"r") as file:
            for line in file:
                enfind=re.findall("free  energy   TOTEN  =",line)
                numions=re.findall("NIONS",line)
                ionptype=re.findall("ions per type =",line)
                ionnamepattern='(?<=VRHFIN =)(.*)(?=:)'
                ion_name=re.findall(ionnamepattern,line)
                stress_find=re.findall("Total",line)
                if len(numions)>0:
                    ionpattern='(?<=NIONS)(.*)'
                    grab_nions=re.findall(ionpattern,line)
                    onlynumIpattern='(?<==)(.*)'
                    onlynumI=re.findall(onlynumIpattern,grab_nions[0])
                    nions.append(int(onlynumI[0].strip()))
                if len(ionptype)>0:
                    ionptpattern='(?<=ions per type =)(.*)'
                    grab_iptype=re.findall(ionptpattern,line)
                    iontypes=grab_iptype[0].strip()
                    ionspertype.append(np.int64(iontypes.split()))
                if len(ion_name)>0:
                    ionname.append(ion_name[0])
                if len(stress_find)>0:
                    stresspattern='(?<=Total)(.*)'
                    stressval=re.findall(stresspattern,line)
                    stresstensor=stressval[0].strip().split()
                    if len(stresstensor)==6:
                        stress.append(np.float64(stresstensor))
                if len(enfind)>0:
                    pattern='(?<=-)(.*)(?=[0-9])'
                    grab_energy=re.findall(pattern,line)
                    patternp='(?<=)(.*)(?=[0-9])'
                    grab_energyp=re.findall(patternp,line)
                    if len(grab_energyp)>0:
                        energy_text.append(float(grab_energyp[0].split("=")[1].strip()))
                    if len(grab_energy)>0:
                        energy_text.append(float("-"+grab_energy[0]))
        file.close()
        nenergy_text=[]
        for i in range(len(self.indrm)):
        	nenergy_text.append(energy_text[self.indrm[i]])
        energy_sys={'ions':nions[0],'ions_name':ionname,'ions_per_type':ionspertype[0],'stress':stress,'energy':nenergy_text}
        return energy_sys
    def get_lattice_vectors(self):
        latindex=[]
        counter=1
        lattice_search="direct lattice vectors"        
        with open(self.filename,"r") as file:
            for line in file:
                all_lattice=re.findall(lattice_search,line)
                if len(all_lattice)>0:
                    latindex.append(counter)
                counter += 1
        file.close()
        all_direct=[]
        all_reciprocal=[]
        for i in range(len(latindex)):
            each_direc=[]
            each_reciproc=[]
            with open(self.filename,"r") as file:
                for index,line in enumerate(file):
                    if index+1>latindex[i] and index+1 <= latindex[i]+3:
                        each_direc.append(line.strip().split()[0])
                        each_direc.append(line.strip().split()[1])
                        each_direc.append(line.strip().split()[2])
                        each_reciproc.append(line.strip().split()[3])
                        each_reciproc.append(line.strip().split()[4])
                        each_reciproc.append(line.strip().split()[5])
                all_direct.append(np.reshape(np.float64(each_direc),(3,3)))
                all_reciprocal.append(np.reshape(np.float64(each_reciproc),(3,3)))
            file.close()
        nrall_direct=[]
        nrall_reciprocal=[]
        for i in range(len(self.indrm)):
        	nrall_direct.append(all_direct[self.indrm[i]])
        	nrall_reciprocal.append(all_reciprocal[self.indrm[i]])
        latticeVectors={'direct':nrall_direct,'reciprocal':nrall_reciprocal}
        return latticeVectors
    def get_pos_forces(self,ionsNum):
        posforce_text='POSITION                                       TOTAL-FORCE \(eV\/Angst\)'
        posforce_index=[]
        counter=1
        with open(self.filename,"r") as file:
            for line in file:
                all_pos_force=re.findall(posforce_text,line)
                if len(all_pos_force)>0:
                    posforce_index.append(counter)
                counter += 1
        file.close()
        all_pforce=[]
        for i in range(len(posforce_index)):
            each_pforce=[]
            with open(self.filename,"r") as file:
                for index,line in enumerate(file):
                    if index+1>posforce_index[i]+1 and index+1 <= posforce_index[i]+1+ionsNum:
                        each_pforce.append(np.float64(line.strip().split()))
            all_pforce.append(np.matrix(each_pforce))
            file.close()
        nrall_pforce=[]
        for i in range(len(self.indrm)):
        	nrall_pforce.append(all_pforce[self.indrm[i]])
        posforcedict={"position-force":all_pforce} 
        return posforcedict

def write_trajectory(fname,ind):
	data=mtpoutcar(fname)
	sysinfo=data.get_sysinfo_energy()
	nions=sysinfo['ions']
	ionsname=sysinfo['ions_name']
	ionspertype=sysinfo['ions_per_type']
	typemtp=[]
	index=[i for i in range(len(ionsname))]
	for i in range(len(ionspertype)):
	    for j in range(ionspertype[i]):
	        typemtp.append(index[i])
	stress=sysinfo['stress']
	energy=sysinfo['energy']
	lattice=data.get_lattice_vectors()
	direct_lattice=lattice['direct']
	position_energy=data.get_pos_forces(nions)
	posenergy=position_energy['position-force']
	shuf_trajec=[i for i in range(len(energy))]
	np.random.shuffle(shuf_trajec)
	# Write in Atom object for each configuration/trajectory and
	# get minimal distance using ASE
	min_dist=[]
#	for i in range(len(energy)):
#		newcfg=Atoms(cell=direct_lattice[i],positions=posenergy[i][:,0:3],pbc=[1,1,1])
#		flat_distance_array=np.unique(np.array(newcfg.get_all_distances()).reshape((1,nions*nions))[0])
#		min_distance=flat_distance_array[1]
#		min_dist.append(min_distance)
	for i in range(len(energy)):
		each_fwrite="./MTP-CFG/"+"data-"+"{}-{}".format(ind,i+1)+".cfg"
		with open(each_fwrite,"w") as file:
			file.writelines("BEGIN_CFG")
			file.writelines("\n")
			file.writelines(" Size")
			file.writelines("\n")
			file.writelines("\t {}".format(nions))
			file.writelines("\n")
			file.writelines(" Supercell")
			file.writelines("\n")
			for j in range(3):
				file.writelines("\t\t {:.6f}\t {:.6f}\t {:.6f}".format(direct_lattice[shuf_trajec[i]][j][0],direct_lattice[shuf_trajec[i]][j][1],direct_lattice[shuf_trajec[i]][j][2]))
				file.writelines("\n")
			file.writelines(" AtomData:  id type       cartes_x      cartes_y      cartes_z           fx          fy          fz")
			file.writelines("\n")
			for k in range(nions):
				nid='{0: <4}'.format(str(k+1))
				attype='{0: <4}'.format(str(typemtp[k]))
				file.writelines("\t\t\t {} \t {} \t {:.8f} \t {:.8f} \t {:.8f} \t {:.8f} \t {:.8f} \t {:.8f}".format(nid,attype,posenergy[shuf_trajec[i]][k,0],posenergy[shuf_trajec[i]][k,1],\
				posenergy[shuf_trajec[i]][k,2],posenergy[shuf_trajec[i]][k,3],posenergy[shuf_trajec[i]][k,4],posenergy[shuf_trajec[i]][k,5]))
				file.writelines("\n")
			file.writelines(" Energy")
			file.writelines("\n")
			file.writelines("\t {}".format(energy[shuf_trajec[i]]))
			file.writelines("\n")
			file.writelines(" PlusStress:  xx          yy          zz          yz          xz          xy")
			file.writelines("\n")
			file.writelines("\t\t {:.8f} \t {:.8f} \t {:.8f} \t {:.8f} \t {:.8f} \t {:.8f}".format(stress[shuf_trajec[i]][0],stress[shuf_trajec[i]][1],stress[shuf_trajec[i]][2],stress[shuf_trajec[i]][3],stress[shuf_trajec[i]][4],stress[shuf_trajec[i]][5]))
			file.writelines("\n")
			file.writelines(" Feature   EFS_by   VASP")
			file.writelines("\n")
#			file.writelines(" Feature   mindist  {:.8f}".format(min_dist[shuf_trajec[i]]))
#			file.writelines("\n")
			file.writelines("END_CFG")
			file.writelines("\n")
			file.writelines("\n")
		file.close()

def write_trajectory_xyz(fname,ind,ind2rem):
	data=mtpoutcar(fname,ind2rem)
	sysinfo=data.get_sysinfo_energy()
	nions=sysinfo['ions']
	ionsname=sysinfo['ions_name']
	ionspertype=sysinfo['ions_per_type']
	typemtp=[]
	index=[i for i in range(len(ionsname))]
	for i in range(len(ionspertype)):
	    for j in range(ionspertype[i]):
	        typemtp.append(ionsname[i])
	stress=sysinfo['stress']
	energy=sysinfo['energy']
	lattice=data.get_lattice_vectors()
	direct_lattice=lattice['direct']
	position_energy=data.get_pos_forces(nions)
	posenergy=position_energy['position-force']
	shuf_trajec=[i for i in range(len(energy))]
	np.random.shuffle(shuf_trajec)
	for i in range(len(energy)):
		each_fwrite="./MTP-XYZ/"+"data-"+"{}-{}".format(ind,i+1)+".xyz"
		with open(each_fwrite,"w") as file:
			file.writelines("{}".format(nions))
			file.writelines("\n")
			lattice_str="Lattice=\"{:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f}\"".format(direct_lattice[shuf_trajec[i]][0][0],\
				direct_lattice[shuf_trajec[i]][0][1],direct_lattice[shuf_trajec[i]][0][2],direct_lattice[shuf_trajec[i]][1][0],\
				direct_lattice[shuf_trajec[i]][1][1],direct_lattice[shuf_trajec[i]][1][2],direct_lattice[shuf_trajec[i]][2][0],
				direct_lattice[shuf_trajec[i]][2][1],direct_lattice[shuf_trajec[i]][2][2])
			energy_str="Energy={}".format(energy[shuf_trajec[i]])
			stress_str="Virial=\"{:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f} {:.6f}\"".format(stress[shuf_trajec[i]][0],stress[shuf_trajec[i]][5],\
				stress[shuf_trajec[i]][4],stress[shuf_trajec[i]][5],stress[shuf_trajec[i]][1],stress[shuf_trajec[i]][3],stress[shuf_trajec[i]][4],stress[shuf_trajec[i]][3],\
				stress[shuf_trajec[i]][2])
			other_str="Properties=species:S:1:pos:R:3:force:R:3"
			header_one=lattice_str+" "+energy_str+" "+stress_str+" "+other_str
			file.writelines(header_one)
			file.writelines("\n")
			for k in range(nions):
				file.writelines("{} \t {:.8f} \t {:.8f} \t {:.8f} \t {:.8f} \t {:.8f} \t {:.8f}".format(typemtp[k],posenergy[shuf_trajec[i]][k,0],posenergy[shuf_trajec[i]][k,1],\
				posenergy[shuf_trajec[i]][k,2],posenergy[shuf_trajec[i]][k,3],posenergy[shuf_trajec[i]][k,4],posenergy[shuf_trajec[i]][k,5]))
				file.writelines("\n")
		file.close()
