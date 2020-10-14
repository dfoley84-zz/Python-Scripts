from pyVim.connect import SmartConnect
from pyVmomi import vim
import ssl
import os
import sys

vCenter_Server = str(sys.argv[1])
vCenter_user = str(sys.argv[2])
vCenter_pass = str(sys.argv[3])

s=ssl.SSLContext(ssl.PROTOCOL_TLSv1)
s.verify_mode=ssl.CERT_NONE
si= SmartConnect(host=vCenter_Server, user=vCenter_user, pwd=vCenter_pass,sslContext=s)
content=si.content

# Method that populates objects of type vimtype
def get_all_objs(content, vimtype):
        obj = {}
        container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
        for managed_object_ref in container.view:
                obj.update({managed_object_ref: managed_object_ref.name})
        return obj 

#Calling above method
Getcluster = get_all_objs(content, [vim.ClusterComputeResource])

for i in Getcluster:
    ClusterName = cluster.name
    #Calling Ansible Script()
