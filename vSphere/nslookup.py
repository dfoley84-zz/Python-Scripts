'''
Script used to perform NSLOOKUP on a List of IP Address and inserted to a Database
'''

import socket
import os
import csv
import ipaddress
import pypyodbc


username = ""
password = ""

#Listing Out
conn = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=;Database=;uid='+username+';pwd='+ password)


v = []
vc = []

#Merging the Subnets to One List
SubnetRange = 

for i in SubnetRange:
    vCenter = i[0]
    subnet = i[1]
    iprange = i[2]
 

    for ip in ipaddress.IPv4Network(unicode(iprange)):
        ipsubnet = str(ip)
        print(ipsubnet)
        nslookup = ipsubnet, socket.getfqdn(ipsubnet)

        if nslookup[1].__contains__("<domain>.com"):
            print(nslookup[0], nslookup[1])
            cursor = conn.cursor()
            cursor.execute(''' INSERT INTO dbo.horizoniplist (subnet, ip_address, hostname, vCenter, status,allocate,available)
                            VALUES ('{}', '{}', '{}', '{}', 'allocate','1','0') '''.format(iprange, nslookup[0], nslookup[1],vCenter))
            cursor.commit()
        else:
            cursor = conn.cursor()
            cursor.execute(''' INSERT INTO dbo.horizoniplist (subnet, ip_address, hostname, vCenter, status,allocate,available)
                            VALUES ('{}', '{}', '{}', '{}', 'available','0','1') '''.format(iprange, nslookup[0], nslookup[1],vCenter ))
            cursor.commit()
