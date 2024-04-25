from linkedin_api.clients.restli.client import RestliClient
import json


class LinkedinHandler:
    ACCESS_TOKEN = "AQVW3empMe6mMLhSfp4fP4CQuW3307XWSNMX6f2tyT91TjXUC0eAMBhUtbgO1I_SLRdg1HL59FWFf6d185X2u34f0Ius5-CYFbZ6bkWBXWFZ4W0_nDYpyOTqKmG9Jk38JVwKpKd-yC35-PFjOXglcPr5VMQ7E7LzD5RSUsZnShjZhyvG3RtsO5U8gbbljoa7BR_y5HvzJJTvYC5lmgkOEmYx0JOFVfGGXOOcnf10exy4tui5RIy6e5wfPoQy_ins9mta1W90i5EecPIJ5ci3VEjLWWtl5z-Amw0CLcqp2f8qLjshYyjvRb-y_l-WQrzz4BCzunze1KFrUT35C5RnVSo95XT20A"
    ME_RESOURCE = "/me"
    UGC_POSTS_RESOURCE = "/ugcPosts"
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
