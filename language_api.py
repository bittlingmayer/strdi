import os
from googleapiclient.discovery import build

service = build('translate', 'v2', developerKey=os.environ['GOOGLE_API_KEY'])

def detect(q):
    r = service.detections().list(
      q=q
    ).execute()
    return r['detections'][0][0]['language']
    
def confidence(q):
    r = service.detections().list(
      q=q
    ).execute()
    return r['detections'][0][0]['confidence']

def translate(q, source=None, target='en'):
    if source is target:
        return q
    return service.translations().list(
      source=source,
      target=target,
      q=q
    ).execute()['translations'][0]['translatedText']