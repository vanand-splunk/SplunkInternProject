import requests
import json
import time

def sendEvents(filename, url, token):

    data = []
    r = []
    counter = 0
    authHeader = {'Authorization': 'Splunk %s' % (token)}

    with open(filename) as jsonFile:
        for event in jsonFile:
            #import pdb; pdb.set_trace()
            try:
                
                #loading in json events
                data = json.loads(event) 
                epochTime = convertToEpoch(data['result']['_time'])

                #sending metadata + event data
                jsonDict = {"index": data['result']['index'], "sourcetype": data['result']['sourcetype'],
                "source": data['result']['source'], "time": epochTime, "event": data['result']['_raw']}
            

            except:
                print ("Error found, script stopped. Before error, we sent %d events to Splunk." % counter)

            else:
                r = requests.post(url, headers=authHeader, json=jsonDict, verify=False)

                #if event is not successfully sent through HEC
                if r.text != '{"text":"Success","code":0}':
                    print(r.text)
                    print ("Error found, script stopped. Before error, we sent %d events to Splunk." % counter)
                    break

                print(r.text)
            
            #keep track of how many events are being sent to Splunk
            counter = counter + 1


#converting timestamp to Epoch
def convertToEpoch(jsonTime):

    epochTime = time.mktime(time.strptime(jsonTime, '%Y-%m-%dT%H:%M:%S.%f%z'))
    return epochTime

def main():

    inputFile = input("Name of File: ")
    inputURL = input("URL: ")
    inputToken = input("Token: ")
    sendEvents(inputFile, inputURL, inputToken)

main()
#load in file
#my_function = takes 1 json file sends to HEC
#30000 linked array, where each element = json file <- my_array
