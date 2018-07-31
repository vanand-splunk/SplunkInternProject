import requests
import json
import time
import urllib3
import config
import sys
from multiprocessing.dummy import Pool as ThreadPool
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#CONSTANTS
filename = config.filename
url = config.url
token = config.token
authHeader = {'Authorization': 'Splunk %s' % (token)}
numThreads = 7
counter = 0

def sendEvent(event):

    global counter
    
    try:
        epochTime = convertToEpoch(event['result']['_time'])

        #sending metadata + event data
        jsonDict = {"index": event['result']['index'], "sourcetype": event['result']['sourcetype'],
        "source": event['result']['source'], "time": epochTime, "event": event['result']['_raw']}       

    except:
        print ("Error found, script stopped. Before error, we sent %d events to Splunk." % counter)
        sys.exit()

    else:
        #call request to send event to HEC
        r = requests.post(url, headers=authHeader, json=jsonDict, verify=False)

        #if event is not successfully sent through HEC
        if r.text != '{"text":"Success","code":0}':
            print(r.text)
            print ("Error found, script stopped. Before error, we sent %d events to Splunk." % counter)
            sys.exit()
    
    #keep track of how many events are being sent to Splunk
    counter +=1


#converting timestamp to Epoch
def convertToEpoch(jsonTime):

    epochTime = time.mktime(time.strptime(jsonTime, '%Y-%m-%dT%H:%M:%S.%f%z'))
    return epochTime


def main():
    
    #initalize linked array
    data = []

    #read json file and load in events into array
    try: 
        with open(filename) as json_file:
            for line in json_file:
                data.append(json.loads(line))
    
    except:
        print ("Error found, script stopped. Before error, we sent %d events to Splunk." % counter)
        sys.exit()

    #set number of threads
    pool = ThreadPool(numThreads)

    #python multithreading - pool.map(my_function, my_array) 
    results = pool.map(sendEvent, data)

    print("Done! %d events sent to Splunk successfully." % counter)
    pool.close()
    pool.join()

main()