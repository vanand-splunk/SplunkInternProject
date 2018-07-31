import cognitive_face as CF
import urllib3
import random
import string
from PIL import Image
import requests
from io import BytesIO
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

confidenceLevel = .2
key = 'c19155c29dc040579ea552f7e6f9414c'  # Replace with a valid Subscription Key here.
CF.Key.set(key)
base_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(base_url)

groupName = ''.join(random.choices(string.ascii_lowercase + string.digits, k=14))
CF.face_list.create(groupName)
mainFaceURL = 'https://oag.ca.gov/sites/oag.ca.gov/files/missing-person/images/orig/Cristal-Alejandra-Garcia-134951.jpg'
mainFaceID = CF.face.detect(mainFaceURL)

img_urls = [
"https://i.imgur.com/mfSKG9A.jpg",
"https://i1110.photobucket.com/albums/h447/rachaelXsb/a2805d9f-7c29-42ac-bf35-bb33e5b22a0c_zpsfd9657f2.jpg",
"https://i723.photobucket.com/albums/ww239/ChynaaBbyXoxo/Mobile Uploads/IMG_5479-imp 1_zpsq7ldcu3a.jpg",
"https://i1138.photobucket.com/albums/n521/seattles_sexy_kaley/2016-08-11-05-45-44-644_480x480.jpg",
"https://i1138.photobucket.com/albums/n521/seattles_sexy_kaley/Mobile Uploads/2feb198f-ece5-466b-b7d2-2b354e7cba7d.jpg",
"https://i1298.photobucket.com/albums/ag46/lavidabella04/Mobile Uploads/PicsArt_03-26-09.59.57_zpsnoi0nmsn.jpg",
"https://jughead.photos/sv4/IMG_6868.jpg",
"https://i.imgur.com/0L0XEFb.jpg",
]
    

i = 0
while i < len(img_urls):
    CF.face_list.add_face(img_urls[i], groupName)
    i = i + 1

similarity = CF.face.find_similars(mainFaceID[0]['faceId'],groupName, max_candidates_return=10, mode='matchFace')

j = 0

print("\nFaces that are similar with a confidence level higher than %f:" % (confidenceLevel))
while j < len(similarity):
    if (similarity[j]['confidence']) > confidenceLevel:      
        print("\nImage %d: %s\nConfidence level: %f\n" % (j, img_urls[j], similarity[j]['confidence']))
    j = j + 1