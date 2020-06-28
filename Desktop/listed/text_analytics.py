import os
from flask import Flask, request, render_template
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def TextAnalytics(url, key, text_chunks):
    #perform analytics on the input text
    client = TextAnalyticsClient(url, AzureKeyCredential(key))

    keyphrase_message = []
    entity_message = []
    sentiment_message = []

    positive_score = 0
    neutral_score  = 0
    negative_score = 0

    for text in text_chunks:
        text = [text]
        #grab the sentiment response
        sentiment_response = client.analyze_sentiment(documents = text)[0]

        positive_score    += sentiment_response.confidence_scores.positive
        neutral_score     += sentiment_response.confidence_scores.neutral
        negative_score    += sentiment_response.confidence_scores.negative

        keyphrase_response = client.extract_key_phrases(documents = text)[0]
        for phrase in keyphrase_response.key_phrases:
            keyphrase_message.append("* {0} \n".format(phrase))

        #grab the keyphrases
        entities_response = client.recognize_entities(documents = text)[0]
        for entity in entities_response.entities:
            entity_message.append("* {0} [{1}]\n".format(entity.text, entity.category))

    sentiment_message = [str(positive_score*100)+"%", str(neutral_score*100)+"%", str(negative_score*100)+"%"]
    
    return sentiment_message, entity_message, keyphrase_message