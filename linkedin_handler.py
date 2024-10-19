import requests
import os
import json
import webbrowser

from dotenv import load_dotenv

#load file into env object
load_dotenv('access_token.env')
#access_token = os.getenv('ACCESS_TOKEN')


api_url = 'https://www.linkedin.com/oauth/v2' 




class LinkedinHandler:

    __auth_code = ''
    __access_token = ''
    __headers= ''
    __user_info = ''

    def __init__(self):
        self.get_auth_code()
        self.get_access_token()
        self.get_headers()
        self.get_user_info()

    def read_credentials(self,file):
        #API credentials are stored in a safe place

        with open(file) as f:
            credentials = json.load(f)
        return credentials
    
    def parse_redirect_uri(self, redirect_response):
        '''
        Parse redirect response into components.
        Extract the authorized token from the redirect uri.
        '''
        from urllib.parse import urlparse, parse_qs

        url = urlparse(redirect_response)
        url = parse_qs(url.query)
        return url['code'][0]
    
    def save_token(self, filename,data):
        '''
        Write token to credentials file.
        '''
        data = json.dumps(data, indent = 4) 
        with open(filename, 'w') as f: 
            f.write(data)

    def get_auth_code(self):
        #Make a HTTP request to the server
        #Once authorized, will redirect to redirect_uri

        credentials = self.read_credentials('credentials.json')
        client_id, client_secret = credentials['client_id'], credentials['client_secret']
        redirect_uri = credentials['redirect_uri']
        
        params = {
            'response_type': 'code',
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'scope': 'w_member_social openid email profile'
        }

        response = requests.get(f'{api_url}/authorization', params=params)

        webbrowser.open(response.url)

        auth_code = input("Past code: ")
        self.__auth_code = auth_code


    def get_access_token(self):

        credentials = self.read_credentials('credentials.json')
        client_id, client_secret = credentials['client_id'], credentials['client_secret']
        redirect_uri = credentials['redirect_uri']

        headers= {'Content-Type': 'application/x-www-form-urlencoded'}

        params = {
            'grant_type': 'authorization_code',
            'code': f'{self.__auth_code}',
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri
        }

        response = requests.post(f'{api_url}/accessToken', headers=headers, params=params)
        token = response.json()
        self.__access_token = token['access_token']

        


    def get_headers(self):
        #Make headers to attach to the API call

        headers = {
            'Authorization': f'Bearer {self.__access_token}',
            'cache-control': 'no-cache',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        self.__headers = headers
        

    def get_user_info(self):
        response = requests.get('https://api.linkedin.com/v2/userinfo', headers = self.__headers)
        user_info = response.json()
        self.__user_info = user_info
        

         

    def post(self, message):

        post_data = {
            'author': f'urn:li:person:{self.__user_info['sub']}',
            'lifecycleState': 'PUBLISHED',
            'specificContent': {
                'com.linkedin.ugc.ShareContent': {
                    'shareCommentary': {
                        'text': message
                    },
                    'shareMediaCategory': 'NONE'
                }
            },
            'visibility': {
                'com.linkedin.ugc.MemberNetworkVisibility': 'CONNECTIONS'
            }
        }

        response = requests.post('https://api.linkedin.com/v2/ugcPosts', headers=self.__headers, json=post_data)
        print(response.json())
        
    
    