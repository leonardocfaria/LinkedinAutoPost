import json
import webbrowser
from urllib.parse import parse_qs, urlparse

import requests

from linkedinautopost.constants.constants import (LINKEDIN_API_URL,
                                                  LINKEDIN_POST_URL)
from linkedinautopost.utils.config import config


class LinkedIn:
    __auth_code = ""
    __access_token = ""
    __headers = ""
    __user_info = ""

    def __init__(self):
        self.get_auth_code()
        self.get_access_token()
        self.get_headers()
        self.get_user_info()

    def parse_redirect_uri(self, redirect_response):
        """
        Parse redirect response into components.
        Extract the authorized token from the redirect uri.
        """

        url = urlparse(redirect_response)
        url = parse_qs(url.query)
        return url["code"][0]

    def save_token(self, filename, data):
        """
        Write token to credentials file.
        """
        data = json.dumps(data, indent=4)
        with open(filename, "w") as f:
            f.write(data)

    def get_auth_code(self):
        # Make a HTTP request to the server
        # Once authorized, will redirect to redirect_uri

        params = {
            "response_type": "code",
            "client_id": config.credentials["client_id"],
            "redirect_uri": config.credentials["redirect_uri"],
            "scope": "w_member_social openid email profile",
        }

        response = requests.get(f"{LINKEDIN_API_URL}/authorization", params=params)

        webbrowser.open(response.url)

        auth_code = input("Past code: ")
        self.__auth_code = auth_code

    def get_access_token(self):
        params = {
            "grant_type": "authorization_code",
            "code": f"{self.__auth_code}",
            "client_id": config.credentials["client_id"],
            "client_id": config.credentials["client_secret"],
            "redirect_uri": config.credentials["redirect_uri"],
        }

        response = requests.post(
            f"{LINKEDIN_API_URL}/accessToken",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            params=params,
        )
        token = response.json()
        self.__access_token = token["access_token"]

    def get_headers(self):
        self.__headers = {
            "Authorization": f"Bearer {self.__access_token}",
            "cache-control": "no-cache",
            "X-Restli-Protocol-Version": "2.0.0",
        }

    def get_user_info(self):
        response = requests.get(f"{LINKEDIN_POST_URL}/userinfo", headers=self.__headers)
        user_info = response.json()
        self.__user_info = user_info

    def post(self, message):
        post_data = {
            "author": f"urn:li:person:{self.__user_info['sub']}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": message},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "CONNECTIONS"},
        }

        response = requests.post(
            f"{LINKEDIN_POST_URL}/ugcPosts", headers=self.__headers, json=post_data
        )
        print(response.json())
