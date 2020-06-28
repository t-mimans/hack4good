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
from io import BytesIO

from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from azure.cognitiveservices.vision.contentmoderator.models import ( Screen )
from msrest.authentication import CognitiveServicesCredentials

# get values from .env
load_dotenv()

# Load environment variables
SUBSCRIPTION_KEY = os.getenv('CONTENT_MODERATOR_SUBSCRIPTION_KEY')
ENDPOINT         = os.getenv('CONTENT_MODERATOR_ENDPOINT')
LOCATION         = os.getenv('CONTENT_MODERATOR_LOCATION')


def text_moderation(text_to_moderate):
    '''
    This functon will moderate the input text.
    @param text, string --> text to be moderated
    '''

    client = ContentModeratorClient( endpoint=ENDPOINT, credentials=CognitiveServicesCredentials( SUBSCRIPTION_KEY ) )
    
    # Check for profanity in the input text
    screen = client.text_moderation.screen_text(
        text_content_type = "text/plain",
        text_content = BytesIO(bytes(text_to_moderate, 'utf-8')),
        language = "eng",
        autocorrect = True,
        pii = True,
        classify = True
    )

    assert isinstance(screen, Screen)
    return screen.as_dict()


def main():
    print("Hello World! \n\n")

    text = input().strip()
    pprint(text_moderation(text))


if __name__ == "__main__":
    main()  