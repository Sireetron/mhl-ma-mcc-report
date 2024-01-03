import requests
import json
import pandas as pd

def iot(month,year,doc,InlineImage) :


    #get History data
    url = "https://iot-bigdata.mwa.co.th/parse/classes/History"
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'Path=/'
    }
    payload = json.dumps({
        "limit" : 2000000,  
        "where": {
            "createdAt": {
                "$gt": {
                    "__type": "Date",
                    "iso": "2022-01-01"
                }
            }
        },
        "_ApplicationId": "b061191d-403b-470a-b92f-9bf9506e3369",
        "_ClientVersion": "js2.12.0",
        "_InstallationId": "0085a4c8-8d9e-47b8-89ca-f0c7f7f8d397",
        "_MasterKey": "502a8878-fa98-43d0-a565-7b72bfda4546",
        "_method": "GET"
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    df_history = pd.json_normalize(data['results'])[['device.objectId']].drop_duplicates()




    #get Device data
    pd.set_option('display.max_columns', 500)
    url = "https://iot-bigdata.mwa.co.th/parse/classes/Device"
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'Path=/'
    }
    payload = json.dumps({
        "_ApplicationId": "b061191d-403b-470a-b92f-9bf9506e3369",
        "_ClientVersion": "js2.12.0",
        "_InstallationId": "0085a4c8-8d9e-47b8-89ca-f0c7f7f8d397",
        "_MasterKey": "502a8878-fa98-43d0-a565-7b72bfda4546",
        "_method": "GET"
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    df_Device = pd.json_normalize(data['results'])[['objectId','station.objectId','name']].drop_duplicates().rename(columns={'objectId': 'device.objectId','name':'device_name'})




    #get Station data
    url = "https://iot-bigdata.mwa.co.th/parse/classes/Station"
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'Path=/'
    }
    payload = json.dumps({
        "_ApplicationId": "b061191d-403b-470a-b92f-9bf9506e3369",
        "_ClientVersion": "js2.12.0",
        "_InstallationId": "0085a4c8-8d9e-47b8-89ca-f0c7f7f8d397",
        "_MasterKey": "502a8878-fa98-43d0-a565-7b72bfda4546",
        "_method": "GET"
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    df_Station = pd.json_normalize(data['results'])[['objectId','project.objectId','name']].drop_duplicates().rename(columns={'objectId':'station.objectId','name':'station_name'})




    #get Project data
    url = "https://iot-bigdata.mwa.co.th/parse/classes/Project"
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'Path=/'
    }
    payload = json.dumps({
        "_ApplicationId": "b061191d-403b-470a-b92f-9bf9506e3369",
        "_ClientVersion": "js2.12.0",
        "_InstallationId": "0085a4c8-8d9e-47b8-89ca-f0c7f7f8d397",
        "_MasterKey": "502a8878-fa98-43d0-a565-7b72bfda4546",
        "_method": "GET"
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    df_Project = pd.json_normalize(data['results'])[['objectId','name']].drop_duplicates().rename(columns={'objectId':'project.objectId','name':'project_name'})



    #Merge All data
    iot_merge = df_history.merge(df_Device,how='left').merge(df_Device,how='left').merge(df_Station,how='left').merge(df_Project,how='left')
    #keep All data to Variable
    device = "{:,}".format(iot_merge['device.objectId'].drop_duplicates().count())
    station = "{:,}".format(iot_merge['station.objectId'].drop_duplicates().count())
    project = "{:,}".format(iot_merge['project.objectId'].drop_duplicates().count())





    #SetData to Object
    iot_merge = iot_merge.to_dict('records')
    context = {
        'device' : device,
        'station' : station,
        'project' : project,
        'iot_table' : iot_merge,
    }
    # print(context)


    return context