import numpy as np
import os
import re
train_data=[]
test_data=[]
with open("./train.xyz","r") as file:
	for line in file:
		train_data.append(line.strip())
file.close()
with open("./test.xyz","r") as file:
	for line in file:
		test_data.append(line.strip())
file.close()
virial_change_train=[]
virial_change_test=[]
for i in range(len(train_data)):
	if train_data[i][0:7]=="Lattice":
		virial_change_train.append(train_data[i])
for i in range(len(test_data)):
	if test_data[i][0:7]=="Lattice":
		virial_change_test.append(test_data[i])
vir_zero_train=[]
vir_zero_test=[]
for i in range(len(virial_change_train)):
	pattern="(?<=\")(.*?)(?=\")"
	vir_each=re.findall(pattern,virial_change_train[i])[2].split()
	virlist=vir_each
	vxx=virlist[0]; vxy=virlist[1]; vxz=virlist[2]
	vyx=virlist[3]; vyy=virlist[4]; vyz=virlist[5]
	vzx=virlist[6]; vzy=virlist[7]; vzz=virlist[8]
	vasym_off='0.0000'
	virlist_asym_off=[vxx,vasym_off,vasym_off,vasym_off,vyy,vasym_off,vasym_off,vasym_off,vzz]
	pre_tag="\""
	off_zero_vir=" ".join(virlist_asym_off)
	post_tag="\" Properties"
	off_virial=pre_tag+off_zero_vir+post_tag
	virial_off_present=virial_change_train[i].split("=")
	virial_off_nop=[virial_off_present[0],virial_off_present[1],virial_off_present[2],off_virial,virial_off_present[4]]
	vir_zero_train.append("=".join(virial_off_nop))
for i in range(len(virial_change_test)):
	pattern="(?<=\")(.*?)(?=\")"
	vir_each=re.findall(pattern,virial_change_test[i])[2].split()
	virlist=vir_each
	vxx=virlist[0]; vxy=virlist[1]; vxz=virlist[2]
	vyx=virlist[3]; vyy=virlist[4]; vyz=virlist[5]
	vzx=virlist[6]; vzy=virlist[7]; vzz=virlist[8]
	vasym_off='0.0000'
	virlist_asym_off=[vxx,vasym_off,vasym_off,vasym_off,vyy,vasym_off,vasym_off,vasym_off,vzz]
	pre_tag="\""
	off_zero_vir=" ".join(virlist_asym_off)
	post_tag="\" Properties"
	off_virial=pre_tag+off_zero_vir+post_tag
	virial_off_present=virial_change_test[i].split("=")
	virial_off_nop=[virial_off_present[0],virial_off_present[1],virial_off_present[2],off_virial,virial_off_present[4]]
	vir_zero_test.append("=".join(virial_off_nop))
counter_train=0
counter_test=0
with open("new_train.xyz","w") as file:
	for i in range(len(train_data)):
		if train_data[i][0:7] != "Lattice":
			file.writelines(train_data[i])
			file.writelines("\n")
		if train_data[i][0:7]=="Lattice":
			file.writelines(vir_zero_train[counter_train])
			file.writelines("\n")
			counter_train += 1;
with open("new_test.xyz","w") as file:
	for i in range(len(test_data)):
		if test_data[i][0:7] != "Lattice":
			file.writelines(test_data[i])
			file.writelines("\n")
		if test_data[i][0:7]=="Lattice":
			file.writelines(vir_zero_test[counter_test])
			file.writelines("\n")
			counter_test += 1;
