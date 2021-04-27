import requests
import json
import getpass
import mysql.connector
import os
import datetime

Servers = []

mydb = mysql.connector.connect(
  host=" ",
  user=" ",
  password="",
  database=""
)

for Server in Servers:
    print(Server)
    try:
        requests.packages.urllib3.disable_warnings()
        pw = os.getenv('pass')
        domain = ' '
        username =  os.getenv('user')
        url = 'https://{}'.format(Server)
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
        }
        data = {"domain": domain, "password": pw, "username": username}
        json_data = json.dumps(data)
        response = requests.post(
            f'{url}/rest/login', verify=False, headers=headers, data=json_data)
        data = response.json()
        access_token = {
            'accept': '*/*',
            'Authorization': 'Bearer ' + data['access_token']
        }

        response = requests.get(f'{url}/rest/monitor/virtual-centers', verify=False, headers=access_token)
        data = response.json()
        for server in data:
            for host in server['datastores']:
                name = host['details']['name']
                path = host['details']['path']
                capcity = host['capacity_mb']
                free = host['free_space_mb']
                status = host['status']
                typestorage = host['type']

                sql = '''  '''
                val = ( )
                mycursor.execute(sql, val)
                mydb.commit()

    except requests.exceptions.RequestException as err:
        print(err)

#Connect to SQL Database
mycursor.execute()
mydb.commit()
