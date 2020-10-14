import boto3
from collections import defaultdict

ec2 = boto3.resource('ec2')
ec2info = defaultdict()

print("The Following Are the Running Instances within Region US-West-1")
for instance in ec2.instances.filter():
    if instance.state["Name"] == "running":
        for tag in instance.tags:
            if tag['Key'] == 'Name':
                print("--------------------------------------------------")
                print ("Name of Instance: " , tag['Value'], "\nInstance ID: " , instance.id, "\nInstance Type:", instance.instance_type,  "\nPublic IP:", instance.public_ip_address, "\nPrivate IP", instance.private_ip_address)
                print("---------------------------------------------------")
            else:
              print("--------------------------------------------------")
                print ("Name of Instance: None " , "\nInstance ID: " , instance.id, "\nInstance Type:", instance.instance_type,  "\nPublic IP:", instance.public_ip_address, "\nPrivate IP", instance.private_ip_address)
                print("---------------------------------------------------")
    else:
        if instance.state["Name"] != "running":
            for tag in instance.tags:
                if tag['Key'] == 'Name':
                    ec2info[instance.id] = {
                        'Type': instance.instance_type,
                        'Private IP': instance.private_ip_address,
                        'Public IP': instance.public_ip_address,
                        'Launch Time': instance.launch_time}

        
