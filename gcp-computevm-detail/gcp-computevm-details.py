import sys
import json
import re
import os
from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build


#Function to capture all the zones in the project
#and send them back to main fn as an array : name
def list_zones(service,project):
    i=0
    #print("Fn to capture all the zones\n")
    name = []
    res_zone = service.zones().list(project=project).execute()
    #print json.dumps(res_zone['items'],indent=3)
    no_of_zones = len(res_zone['items'])
    print ("Number of zones present in the project : "+ str(no_of_zones))
    while i < no_of_zones:
        name.append(res_zone['items'][i]['name'])
        i=i+1
    return name
    #print name


def list_instances(service,project,zone):

    k = 0
    no_of_zones = len(zone)
    #for all zones ,check no of instances present
    while k < no_of_zones:
        i = 0
        result = service.instances().list(project=project, zone=zone[k]).execute()
        # If a zone has instances then list out all the detials
        try :
            no_of_instances = len(result['items'])
            #print json.dumps(result['items'],indent= 3)
            print "\n"+"Number of instances found :"+str(no_of_instances)+"\n"
            print "STATUS"+"\t"+"INSTANCE NAME"+"\t"+"MACHINE TYPE"+"\t"+"NO OF DISKS ATTACHED"+"\t"+"DISK NAME"+"\t"+"BOOT DISK ?"
            print "--------------------------------------------------------------------------"
            while i < no_of_instances:
                j = 0
                mc_type = re.split('([^/]*)$',str(result['items'][i]['machineType']))
                no_of_disks = len(result['items'][i]['disks'])
                while j < no_of_disks:

                    print (str(result['items'][i]['status'])+'\t'+str(result['items'][i]['name'])+'\t'+mc_type[1]+"\t"+str(len(result['items'][i]['disks']))+'\t'+str(result['items'][i]['disks'][j]['deviceName'])+"\t"+str(result['items'][i]['disks'][j]['boot']))
                    j = j+1
                i = i + 1
            k=k+1
        #if a zone doesn't have any instances (a key error is thrown), then move on to next instance
        except KeyError:
            k=k+1




def disk_details(service,project,zone):
    i = 0
    k=0
    no_of_zones = len(zone)
    print "\n"+"DISK DETAILS"+"\n"
    #for all zones ,check no of instances present
    while k < no_of_zones:
        i = 0
        disk_res = service.disks().list(project=project, zone=zone[k]).execute()
        #if zone has disks mounted on it
        try :
            no_of_disks = len(disk_res['items'])
            print "\n"+"DISK NAME"+"\t"+"DISK TYPE"+"\t"+"DISK SIZE"+"\t"+"DISK STATUS"+"\n"
            print "----------------------------------------------------------------------"
            while i <  no_of_disks:
                type = re.split('([^/]*)$',str(disk_res['items'][i]['type']))
                #print type[1]
                print(str(disk_res['items'][i]['name'])+"\t"+type[1]+"\t"+str(disk_res['items'][i]['sizeGb'])+" GB"+"\t"+str(disk_res['items'][i]['status']))
                i = i+1
            k=k+1
        except KeyError:
            k=k+1




def main():
    print("\n")
    zone_arr = []

    #Enter the service account file in json format path details
    json_path = raw_input('Enter the file location path with json file name :')
    #Enter the project id path details
    project = raw_input('Enter the project-id :')

    #Validate the credentials given in the json file and export in the environment
    try :
            os.system("export GOOGLE_APPLICATION_CREDENTIALS="+str(json_path))
            credentials = GoogleCredentials.get_application_default()
    except Error as e:
        print(e)

   # Use compute API with the credentials
    try :
        service = build('compute', 'v1', credentials=credentials)
    except Error as e:
        print(e)

    #Capture all the zones available in  project
    zone_arr = list_zones(service,str(project))
    #print zone_arr

    #Pass all the zones to list the compute instances in the project
    list_instances(service,str(project),zone_arr)

    #List all the disks attached to instances in use in Project
    disk_details(service,str(project),zone_arr)

if __name__ == '__main__':
    main()


