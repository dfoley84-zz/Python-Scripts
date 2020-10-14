import pypyodbc   
import csv

'''
Function: 
        Simple Script to Make a Connection to an SQL Database,
        This will First Remove the Old Data that resides within the Table, 
        Then repopulate the Table with new Data. Within the CSV File
'''

#Connect to SQL Database
conn = pypyodbc.connect('Driver={SQL Server};Server=;Database=;uid=;pwd=')


#Remove SQL DataFrom Table
cursor = conn.cursor()
cursor.execute('TRUNCATE TABLE dbo.Report5')
cursor.close()

#Open CSV File Import into SQL Database
with open("report5.csv") as f:
    reader = csv.reader(f)
    columns = next(reader) 
    query = 'insert into Report5({0}) values ({1})'
    query = query.format(','.join(columns), ','.join('?' * len(columns)))
    cursor = conn.cursor()
    for data in reader:
        cursor.execute(query, data)
    cursor.commit()
    cursor.close()
    conn.close()
f.close()
