import os
from os import system
from subprocess import PIPE, run
import glob
import numpy as np
import shutil
import re
import mdynamics as md
convergence_threshold_plus=0.000001
convergence_threshold_minus=-0.000001
def run_command(com):
	result=run(com,stdout=PIPE,stderr=PIPE,universal_newlines=True,shell=True)
	return result.stdout
dirs=glob.glob("./**/slurm-[0-9]*.out",recursive=True)
ndedirs=[]
for i in range(len(dirs)):
	match=re.findall("debug",dirs[i])
	if len(match) == 0:
		ndedirs.append(dirs[i])
dir_location=[]
for i in range(len(ndedirs)):
	dir_location_text="ls {}|awk -F \"slurm\" '{{print $1}}'".format(ndedirs[i])
	dir_location.append(run_command(dir_location_text).strip().split()[0])
uniquedir=list(set(dir_location))
outcar_trajectory=[]
all_traj_num=[]
for i in range(len(uniquedir)):
	outcar_text="cat {}|grep POSITION|wc -l".format(uniquedir[i]+"OUTCAR")
	traj_num=int(run_command(outcar_text).strip().split()[0])
	all_traj_num.append(traj_num)
#	print("{} : {}".format(uniquedir[i],traj_num))
identify_which_slurm=[]
correct_slurm_dir=[]
correct_trajectory=[]
for i in range(len(uniquedir)):
	number_of_slurms=glob.glob(uniquedir[i]+"slurm-[0-9]*.out")
	for j in range(len(number_of_slurms)):
		count_slurm_traj="cat {}|grep T=|wc -l".format(number_of_slurms[j])
		slurm_traj_num=int(run_command(count_slurm_traj).strip().split()[0])
		if slurm_traj_num==all_traj_num[i]:
			correct_slurm_dir.append(number_of_slurms[j])
			correct_trajectory.append(slurm_traj_num)
with open("log.txt","w") as file:
	file.writelines("Directory \t\t\t Slurm job file to look for \t\t\t number of trajectory")
	file.writelines("\n")
	for i in range(len(uniquedir)):
		file.writelines("{}: {}: {}".format(uniquedir[i],correct_slurm_dir[i],correct_trajectory[i]))
		file.writelines("\n")
file.close()
############################ upto this point is looking up the directory, matching correct slurm out file with OUTCAR and cleaning ####################
########### picking up only those file that has greater than 10 trajectory at the least and logging it to new file ####################################
dir_above_ten_traj=[]
slurm_file_above_ten_traj=[]
traj_num_above_ten_traj=[]
for i in range(len(uniquedir)):
	if correct_trajectory[i] > 10:
		dir_above_ten_traj.append(uniquedir[i])
		slurm_file_above_ten_traj.append(correct_slurm_dir[i])
		traj_num_above_ten_traj.append(correct_trajectory[i]) 
convergence_val=[]
sl_file_above_ten_wconv=[]
ndir_above_ten_traj=[]
ntraj_num_above_ten_traj=[]
for i in range(len(slurm_file_above_ten_traj)):
	conv_check_RMM="cat {}|grep -B 1 T=|grep -o RMM".format(slurm_file_above_ten_traj[i])
	cRMM_res=run_command(conv_check_RMM).strip().split()
	if len(cRMM_res) > 0 and cRMM_res[0] == 'RMM':
		conv_check="cat {}|grep -B 1 T=|grep RMM|awk -F \":\" '{{print $2}}'|awk -F \" \" '{{print $3}}'".format(slurm_file_above_ten_traj[i])
		convergence_val.append(run_command(conv_check).strip().split())
		sl_file_above_ten_wconv.append(slurm_file_above_ten_traj[i])
		ndir_above_ten_traj.append(dir_above_ten_traj[i])
		ntraj_num_above_ten_traj.append(traj_num_above_ten_traj[i])
	conv_check_DAV="cat {}|grep -B 1 T=|grep -o DAV".format(slurm_file_above_ten_traj[i])
	cDAV_res=run_command(conv_check_DAV).strip().split()
	if len(cDAV_res) > 0 and cDAV_res[0] == 'DAV':
		conv_check="cat {}|grep -B 1 T=|grep DAV|awk -F \":\" '{{print $2}}'|awk -F \" \" '{{print $3}}'".format(slurm_file_above_ten_traj[i])
		convergence_val.append(run_command(conv_check).strip().split())
		sl_file_above_ten_wconv.append(slurm_file_above_ten_traj[i])
		ndir_above_ten_traj.append(dir_above_ten_traj[i])
		ntraj_num_above_ten_traj.append(traj_num_above_ten_traj[i])
index_below_conv=[]
for i in range(len(convergence_val)):
	each_index=[]
	for j in range(len(convergence_val[i])):
		if float(convergence_val[i][j]) < convergence_threshold_plus or float(convergence_val[i][j]) < convergence_threshold_minus:
			each_index.append(j)
	index_below_conv.append(each_index)
# To write now is
# ndir_above_ten_traj, sl_file_above_ten_wconv, ntraj_num_above_ten_traj, index_below_conv
with open("above-ten.txt","w") as file:
	file.writelines("Directory \t\t\t Slurm job file to look for \t\t\t number of trajectory \t\t\t traj. to select")
	file.writelines("\n")
	for i in range(len(ndir_above_ten_traj)):
		file.writelines("{}: {}: {}: {}".format(ndir_above_ten_traj[i],sl_file_above_ten_wconv[i],ntraj_num_above_ten_traj[i],len(index_below_conv[i])))
		file.writelines("\n")
file.close()
if os.path.exists("./MTP-XYZ"):
		shutil.rmtree("./MTP-XYZ")
os.makedirs("./MTP-XYZ",exist_ok=True)
for i in range(len(dir_above_ten_traj)):
	if len(index_below_conv[i]) > 0:
		md.write_trajectory_xyz(ndir_above_ten_traj[i]+"OUTCAR",i+1,index_below_conv[i])
