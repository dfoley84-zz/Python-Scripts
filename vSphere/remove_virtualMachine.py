'''
Script is Used to Remove Virtual Machine which have been Selected to be Removed after 7 Days has passed.
'''

import csv 
import sys
import os
from datetime import datetime, timedelta

#Getting System Time
Todays_Date = datetime.now()
String_Date = str(Todays_Date)
Today_object = datetime.strptime(String_Date,'%Y-%m-%d %H:%M:%S.%f')


#Open CSV File and Add Contents to a List
with open('virtualmachines.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    data = list(reader)
f.close()
#os.remove('outfile.csv')

newname = 'virtualmachines' + String_Date + '.csv'
os.rename('virtualmachines.csv', newname)

if len(data) > 0:
#Loop over the Data List 
    for i in data:
        #Get the Index Item which holds the Date Variable 
        Old_Date = i[3]
        #Using timedelta to Compare System Date agaisnt Date within the List
        datetime_object = datetime.strptime(Old_Date, '%Y-%m-%d %H:%M:%S.%f')
        result = abs(Today_object - datetime_object).days

    #Using an IF Statement if the Date within List is Above Seven Days Run the Ansible Script to Remove the Machine
        if result > 7:
            re  = (i)
            s = ",".join(re)

            print("Deleting The Following Machine: {}".format(i[2]))
            
            os.system('ansible-playbook Delete_Virtual_Machine.yaml --extra-vars "vcenter_hostname={} vcenter_user= Vcenter_password= cluster_name={} VM_Name={}"'.format(i[0],i[1],i[2]))

            print("Finished Removing: {}".format(i[2]))

            print("Running Python Script to Remove A Record")
            os.system('python RemoveARecord.py {} {} {} {}'.format(i[1],i[2],i[3],i[4]))
            
            print("Python Job Finished:")

            #Keeping Track of Items thaat are Removed from vSphere.
            with open("RemovedMachines.csv", "a") as f:
                f.write("The Following Machine: {} Was Removed From vCenter: {} On the Following Date: {}\n".format(i[2],i[0],Todays_Date))
            f.close()

        else:
            #Any Items that are not Above the Seven Day mark Write back to New CSV File.
            re = (i)
            #Remvoving the Brackets and '' from Items within List & Write to CSV File 
            s = ",".join(re)
            with open("virtualmachines.csv", "a") as fp:
                fp.write("{}\n".format(s))
            fp.close()
else:
    print("No Infomation was Processed: Data List is Null")
