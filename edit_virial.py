import sys
import os
virtrain=[]
virtest=[]
if os.path.exists("./virial_train.out") and os.path.exists("./virial_test.out"):
    print("File virial train and test file exist")
    with open("./virial_train.out","r") as file:
        for line in file:
            virtrain.append(line.split())
    file.close()
    with open("./virial_test.out","r") as file:
        for line in file:
            virtest.append(line.split())
    file.close()
else:
    print("File virial train and test does not exist")
    sys.exit()
stressxx_train=[]
stressyy_train=[]
stresszz_train=[]
for i in range(len(virtrain)):
    stressxx_train.append([virtrain[i][6],virtrain[i][0]])
    stressyy_train.append([virtrain[i][7],virtrain[i][1]])
    stresszz_train.append([virtrain[i][8],virtrain[i][2]])
with open("stress_train.out","w") as file:
    for i in range(len(stressxx_train)):
        file.writelines("{:.8f} {:.8f}".format(float(stressxx_train[i][0]),float(stressxx_train[i][1])))
        file.writelines("\n")
    for i in range(len(stressyy_train)):
        file.writelines("{:.8f} {:.8f}".format(float(stressyy_train[i][0]),float(stressyy_train[i][1])))
        file.writelines("\n")
    for i in range(len(stressxx_train)):
        file.writelines("{:.8f} {:.8f}".format(float(stresszz_train[i][0]),float(stresszz_train[i][1])))
        file.writelines("\n")
file.close()
stressxx_test=[]
stressyy_test=[]
stresszz_test=[]
for i in range(len(virtest)):
    stressxx_test.append([virtest[i][6],virtest[i][0]])
    stressyy_test.append([virtest[i][7],virtest[i][1]])
    stresszz_test.append([virtest[i][8],virtest[i][2]])
with open("stress_test.out","w") as file:
    for i in range(len(stressxx_test)):
        file.writelines("{:.8f} {:.8f}".format(float(stressxx_test[i][0]),float(stressxx_test[i][1])))
        file.writelines("\n")
    for i in range(len(stressyy_test)):
        file.writelines("{:.8f} {:.8f}".format(float(stressyy_test[i][0]),float(stressyy_test[i][1])))
        file.writelines("\n")
    for i in range(len(stressxx_test)):
        file.writelines("{:.8f} {:.8f}".format(float(stresszz_test[i][0]),float(stresszz_test[i][1])))
        file.writelines("\n")
file.close()

