  
from pyVim.connect import SmartConnect
from pyVmomi import vim
import ssl
import os

s=ssl.SSLContext(ssl.PROTOCOL_TLSv1)
s.verify_mode=ssl.CERT_NONE
si= SmartConnect(host="", user="", pwd="",sslContext=s)
content=si.content

# Method that populates objects of type vimtype
def get_all_objs(content, vimtype):
        obj = {}
        container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
        for managed_object_ref in container.view:
                obj.update({managed_object_ref: managed_object_ref.name})
        return obj 

#Calling above method
getVM=get_all_objs(content, [vim.VirtualMachine])

for vm in getVM:
        print(vm.name)
