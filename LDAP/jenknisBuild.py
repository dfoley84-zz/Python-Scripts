import requests

def jenkinsNewUser(userName, horizonserver, nodepool):
  email = userName+'@.com'
  email2 = userName+'@.com'
  machine_name = ''

  Jenkins_url = ""  
  jenkins_user = ""
  jenkins_pwd = ""
  jenkins_job_name = ""
  buildWithParameters = True
  jenkins_params = {
            'token': '',
            '' : ,
            '' : ,
            '' : ,
            '' : ,
            'email' : email }
  try:
      auth= (jenkins_user, jenkins_pwd)
      crumb_data= requests.get("{}/crumbIssuer/api/json".format(Jenkins_url),verify=False,auth=auth,headers={'content-type': 'application/json'})
      if str(crumb_data.status_code) == "200":
          if buildWithParameters:
              data = requests.get("{}/job/{}/buildWithParameters".format(Jenkins_url,jenkins_job_name),verify=False,auth=auth,params=jenkins_params,headers={'content-type': 'application/json','Jenkins-Crumb':crumb_data.json()['crumb']})
          else:
             data = requests.get("{}/job/{}/build".format(Jenkins_url,jenkins_job_name),verify=False,auth=auth,params=jenkins_params,headers={'content-type': 'application/json','Jenkins-Crumb':crumb_data.json()['crumb']})
          if str(data.status_code) == "201":
              print("Building vDesk for User: {}".format(userName))
          else:
              print("Error")
      else:
          print("Couldn't fetch Jenkins-Crumb")
          raise

  except Exception as e:
      print ("Failed triggering the Jenkins job")
      print ("Error: " + str(e))
