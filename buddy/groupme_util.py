from django.conf import settings
import requests, json

from .models import User, Course, StudyGroup, StudyRequest

# GROUPME_ACCESS_TOKEN = settings.GROUPME_ACCESS_TOKEN

def creategroupme(title):
    groupme_name = "Study Group for - {}".format(title)
    groupme_params = '{"name": "'+str(groupme_name)+'", "share":"true"}'
    posturl = "https://api.groupme.com/v3/groups?token={}".format(GROUPME_ACCESS_TOKEN)
    groupme_response = requests.post(posturl,
                                    groupme_params).json()

    groupme_id = groupme_response['response']['group_id']
    groupme_shareurl = groupme_response['response']['share_url']

    return(groupme_name, groupme_id, groupme_shareurl)