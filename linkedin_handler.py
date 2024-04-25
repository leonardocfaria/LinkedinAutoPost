from linkedin_api.clients.restli.client import RestliClient
import json


class LinkedinHandler:
    ACCESS_TOKEN = <Token>
    ME_RESOURCE = "/me"
    POSTS_RESOURCE = "/posts"
    API_VERSION = "202302"

    def __init__(self):
        self.restli_client = RestliClient()
        self.restli_client.session.hooks["response"].append(lambda r: r.raise_for_status())

    def post(self, text):
        me_ID = self.restli_client.get(resource_path=self.ME_RESOURCE, access_token=self.ACCESS_TOKEN)
        print(f"Successfully fetched profile: {json.dumps(me_ID.entity)}")
        posts_create_response = self.restli_client.create(
            resource_path=self.POSTS_RESOURCE,
            entity={
              "author": f"urn:li:person:{me_ID.entity['id']}",
              "visibility": "PUBLIC",

              "commentary": text,
              "distribution": {
                   "feedDistribution": "MAIN_FEED",
                   "targetEntities": [],
                   "thirdPartyDistributionChannels": [],
              },
            },
           #version_string=API_VERSION,
            access_token=self.ACCESS_TOKEN,
        )
        print(f"Successfully created post using /posts: {posts_create_response.entity_id}")
