import json
import os.path
import pandas as pd
import requests
from time import sleep
headers = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
           }


def pre_process_data():
    df=pd.read_csv('linkedin_profiles.csv')
    cc=df.Url.str.split('/').str[-2]
    usernames_list=cc.tolist()
    return usernames_list


def get_data(user_list):
    with requests.session() as s:
        s.cookies['li_at'] = "AQEDATXLzLwB-KVSAAABgXWvGKgAAAGBmbucqFYAu1ypt9oo_q6dkDkXdbInmMYHSrxh5l1vY2TR7AM5znPUZWw5MlgvsSVpQX5xgxM3R3cz35wRw6SO_8MiL0dyseecce_SHZrirjqapbC1SL8PgkMD"
        s.cookies["JSESSIONID"] = "ajax:5910709753241549801"
        s.headers = headers
        s.headers["csrf-token"] = s.cookies["JSESSIONID"].strip('"')
    print('Total Profiles= '+str(len(user_list)))
    for user in user_list:
        indd=user_list.index(user)
        print('Extracting profile no. '+str(indd+1))
        link='https://www.linkedin.com/voyager/api/identity/profiles/'+str(user)
        response = s.get(link)
        response_dict = response.json()

        isFile = os.path.isdir('output_data')
        if isFile==False:
            os.mkdir('output_data')
        with open('output_data/'+str(user)+'.json', 'w') as fp:
            json.dump(response_dict, fp)
        sleep(10)

users_list=pre_process_data()
get_data(users_list)