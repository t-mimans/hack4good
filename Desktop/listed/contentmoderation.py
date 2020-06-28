#
#   Module Name:
#             contentmoderation.py
#   Description:    
# 
#   Author: Mike Kamwana ( Github: @MikeMula)
#
#
#   Notes:
#

import os
from pprint import pprint
from dotenv import load_dotenv

from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from azure.cognitiveservices.vision.contentmoderator.models import ( Screen )
from msrest.authentication import CognitiveServicesCredentials

# get values from .env
load_dotenv()

# Load environment variables
SUBSCRIPTION_KEY = os.getenv('CONTENT_MODERATOR_SUBSCRIPTION_KEY')
ENDPOINT         = os.getenv('CONTENT_MODERATOR_ENDPOINT')
LOCATION         = os.getenv('CONTENT_MODERATOR_LOCATION')

def text_moderation(filename):
    '''
    This functon will moderate the input text.
    @param text_to_screen, string --> text to be moderated
    '''

    client = ContentModeratorClient( endpoint=ENDPOINT, credentials=CognitiveServicesCredentials(SUBSCRIPTION_KEY) )

    with open(filename, "rb") as text_fd:
        
        # Check for profanity in the input text
        screen = client.text_moderation.screen_text(
            text_content_type = "text/plain",
            text_content = text_fd,
            language = "eng",
            autocorrect = True,
            pii = True
        )

        assert isinstance(screen, Screen)
        pprint(screen.as_dict())






def main():
    print("Hello World! \n\n")

    text = input().strip()
    text_moderation(text)

if __name__ == "__main__":
    main()  