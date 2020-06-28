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

def text_moderation(url, key, text_to_moderate):
    '''
    This functon will moderate the input text.
    @param text, string --> text to be moderated
    '''

    client = ContentModeratorClient( url, CognitiveServicesCredentials( key ) )
    
    # Check for profanity in the input text
    screen = client.text_moderation.screen_text(
        text_content_type = "text/plain",
        text_content = BytesIO(bytes(text_to_moderate, 'utf-8')),
        language = "eng",
        autocorrect = True,
        classify = True
    )

    # Category1 refers to potential presence of language that may be considered sexually explicit or adult in certain situations.
    # Category2 refers to potential presence of language that may be considered sexually suggestive or mature in certain situations.
    # Category3 refers to potential presence of language that may be considered offensive in certain situations.
    # Score is between 0 and 1. The higher the score, the higher the model is predicting that the category may be applicable. This feature relies on a statistical model rather than manually coded outcomes. We recommend testing with your own content to determine how each category aligns to your requirements.

    assert isinstance(screen, Screen)
    return screen.as_dict()