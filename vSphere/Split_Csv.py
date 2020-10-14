import pandas as pd
import numpy as np
from pandas import Series, DataFrame

'''
PowerCLI Script is Exporting Infomration on the networking Stack as -join','
Before Import the CSV Flat File to an SQL Database, unjoining the Vaules needs to take place 
'''

#Open the File with Pandas
try:
    report = pd.read_csv("rC:\Script\Report6.csv")
except EnvironmentError:
    print("File Not Found")
    exit(0)
else:
    pass

#Create a new DataFrame from The Network Role, and Split Vaules by ','
s = report['Network'].srt.split(',').apply(Series,1).stack()
s.index = s.index.droplevel(-1) #Remove Null Row to Line up with Columns up with vSphere_Report
s.name = 'Network' #Name the DataFrame Row as Network
del report['Network'] #Drop the Network Role already within vSphere_Report DataFrame
new_report = report.join(s) #join the two DataFrames. 

#Once Joined Export to New CSV File ready for Importing to SQL Database.
new_report.to_csv("rC:\Script\Report7.csv", index = False, sep=',', encoding='utf-8')
