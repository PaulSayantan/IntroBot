# here scrape the github account and get the user info
# and check with the provided fullname
# true to accept false to refuse

#Python Script to extract Profile Info from GitHub

import requests
import re
import json

def extract_data(DataNeeded, DataFromGithub, ):
    Data = {}
    for (k, v) in DataFromGithub.items():

            if k in DataNeeded:
                Data[k] = v
    
    return Data


def save_json(filename , json_data):
    with open('{}.json'.format(filename), 'w') as fp:
        json.dump(json_data, fp , indent= True)


def get_user_stats(Username, data):
    Username = Username
    UserURL = 'https://api.github.com/users/{}'.format(Username)

    # this is data from github, we dont need all of it
    UserDataFromGithub = requests.get(UserURL).json()
    DataNeeded = [
        'name',
        #'type',
        'bio',
        'company',
        #'blog',
        'location',
        #'public_repos',
        #'followers'
    ]
    userData = extract_data(DataNeeded, UserDataFromGithub)
    return userData.get(data)


# check with the provided fullname
# true to accept false to refuse
def checkAccount(fname, url) -> bool:
    regex = r'(\w+)$'
    match = re.search(regex, url)
    uname = match.group(1)
    rname = get_user_stats(uname, 'name')
    return fname == rname
    