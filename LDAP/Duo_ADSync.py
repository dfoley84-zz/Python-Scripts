'''
Duo Syncs every by default every 24hours. 
Script will force a Sync every hour.
'''

import sys
import os
import time
import duo_client
from time import sleep
import datetime

from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, AUTO_BIND_NO_TLS, SUBTREE
from ldap3.core.exceptions import LDAPCursorError
now = datetime.datetime.now()

server_name = ''
domain_name = ''
user_name = ''
password = ''

i_key = ""
s_key = ""
api_host = "api-.duosecurity.com"
Directory_key = ""


# Array of Users
Duo_users = [] # Array / List for Users that are within Duo
duo_ad_group_2fa = [] # Array / List for users that are part of 2FA-Hosting
NotSyncedUsers = [] # Array / List of User that aren't Sync to Duo
newlist = [] # Lower Str.


Active_Directory = [
'2FA-DUO,OU=Enterprise Groups,OU=Groups,OU=,OU=Global Hosting,DC=rmcloud,DC=int',
',OU=Roles,OU=100620,OU=Projects,OU=10342,OU=Tenants,OU=10001,OU=Tenants,OU=SSA,OU=SSO,OU=Global Hosting,DC=,DC=int',
',OU=Roles,OU=10367,OU=Tenants,OU=10001,OU=Tenants,OU=SSA,OU=SSO,OU=Global Hosting,DC=,DC=int',
',OU=Roles,OU=10367,OU=Tenants,OU=10001,OU=Tenants,OU=SSA,OU=SSO,OU=Global Hosting,DC=,DC=int',
',OU=Roles,OU=10316,OU=Tenants,OU=10001,OU=Tenants,OU=SSA,OU=SSO,OU=Global Hosting,DC=,DC=int',
'Remote Ondemand - DUO,OU=Custom Tenants,OU=SSA,OU=SSO,OU=Global Hosting,DC=,DC=int'
 ]

i = 0

admin_api = duo_client.Admin(
    ikey = i_key,
    skey = s_key,
    host = api_host,)


# Get Users from DUO
users = admin_api.get_users()
for user in users:
	Duo_users.append(user["username"]) 

while i < len(Active_Directory):
	
    Active_DirectoryGroup = (Active_Directory[i])
    format_string = '{:40}'
    print(format_string.format('samaccountname'))
    server = Server(server_name, get_info=ALL)
    conn = Connection(server, user='{}\\{}'.format(domain_name, user_name), password=password, authentication=NTLM,auto_bind=True)
    conn.search('dc={},dc=int'.format(domain_name),'(&(objectCategory=user)(memberOf:1.2.840.113556.1.4.1941:=CN={}))'.format(Active_DirectoryGroup),
    search_scope=SUBTREE,
    attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])
	
    for a in sorted(conn.entries):
        duo_ad_group_2fa.append(a.samaccountname)
	
    i += 1

for g in duo_ad_group_2fa:
	for items in g:
		newlist.append(items.lower())
		
for b in newlist:
	if b not in Duo_users:
		NotSyncedUsers.append(i)

f = open("DuoSync.txt", "a+")
for s in NotSyncedUsers:
	os.system("python -m duo_client.client --ikey {} --skey {} --host {} --method POST --path /admin/v1/users/directorysync/{}/syncuser username={}".format(i_key, s_key, api_host, Directory_key, s))
	f.write('The Following User: {}  was Added to Duo on: {}\n'.format(s, str(now)))
f.close()
