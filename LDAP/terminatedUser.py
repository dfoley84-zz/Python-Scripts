import sys
import os
import requests
import csv
from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, AUTO_BIND_NO_TLS, SUBTREE
from ldap3.core.exceptions import LDAPCursorError
import pypyodbc

#Import Function from JenkinsBuild.py
from jenkinsBuild import jenkinsNewUser

password = sys.argv[1]
list_members = []
list_members_exclude = []

dbuser = ""
dbpass = ""

#Querying Active Directory 
def get_na_group_members (group_sam_account_name, user_name, user_domain_name, user_password):
 server = Server('', port=, use_ssl=True, allowed_referral_hosts=[('', True), ('', False)])
 conn = Connection(server, user='{}\\{}'.format(user_domain_name, user_name), password=user_password, authentication=NTLM, auto_bind=True)
 conn.search(
  search_base='DC=na,DC=,DC=com',
  search_filter=f'(sAMAccountName={group_sam_account_name})',
  attributes=[
   'distinguishedName'
  ]
 )

 group_dn = conn.entries[0].distinguishedName.value
 conn.search(
  search_base=group_dn,
  search_filter='(objectClass=group)',
  search_scope='SUBTREE',
  attributes = ['member']
 )

 for entry in conn.entries:
  for member in entry.member.values:
   conn.search(
    search_base='DC=,DC=com',
    search_filter=f'(distinguishedName={member})',
    attributes=[
     'sAMAccountName',
     'employeeType'
    ]
   )
   if group_sam_account_name == '':
       list_members.append((conn.entries[0].sAMAccountName.value, conn.entries[0].employeeType.value, group_sam_account_name))
   else:
       list_members_exclude.append((conn.entries[0].sAMAccountName.value, conn.entries[0].employeeType.value, group_sam_account_name))

        
def userAccount(pool):
    # Listing out the Values within list_members
    for i in list_members:
        User = i[0]
        employeeType = i[1]

        #Listing out the Values within the Exclude List
        for a in list_members_exclude:
            excludeUser = a[0]
            
            #Checking if Users within the List_Members is not within the Exclude List
            if User not in excludeUser:
                #Checking if User is not Terminated
                if employeeType == 'terminated':
                    SQLQuery(pool,User)
                    terminatedUser = SQLQuery(pool,User)[0]
                    
                    #if the Result is True(1) or False(0) Call Jenkins to Remove .
                    if terminatedUser == 1:
                         #jenkinsRemoveUser( )
                else:

                    #Checking the Group User has Assigned vDesk
                    SQLQuery(pool,User)
                    ListUser = SQLQuery(pool,User)[0]
                    if ListUser == 1:
                        pass
                    else:
                        print(User)
                        #jenkinsNewUser( )
            else:
                #Printing out the Users that are in the Excluded List.
                print('User: {} Is Excluded from the List'.format(User))
        

def SQLQuery(pool,User):
    try:
        conn = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=;Database=;uid='+dbuser+';pwd='+ dbpass)
        cursor = conn.cursor()
        count = cursor.execute("SELECT COUNT(UserName) FROM dbo. WHERE ='{}' AND UserName='{}'".format(pool,User))
        result = count.fetchone()
    except pypyodbc.DatabaseError as err:
        raise er
    return result


def main():

    exclude =[(''),(''),('')]
    Group = [(''),(''),('')]


    for i in Group:
        pool = i[0]
        group = i[1]
        get_na_group_members()

        for a in exclude:
            pool = a[0]
            group = a[1]
            get_na_group_members()

            userAccount(pool)
            list_members.clear()
            list_members_exclude.clear()
                
if __name__ == "__main__":
    main()
