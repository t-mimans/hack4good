import os
from flask import Flask, request, render_template
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

app = Flask(__name__)
load_dotenv()

COGSVCS_KEY = os.getenv('COGSVCS_KEY')
COGSVCS_CLIENTURL = os.getenv('COGSVCS_CLIENTURL')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # User is requesting main page
        return render_template('index.html')

    elif request.method == 'POST':
        #perform analytics on the input text
        client = TextAnalyticsClient(COGSVCS_CLIENTURL, AzureKeyCredential(COGSVCS_KEY))

        #grab the input text
        text = request.form['text_input']
        text = [text]

        #grab the sentiment response
        sentiment_response = client.analyze_sentiment(documents = text)[0]
        message = []
        message.append("YOUR TEXT: " + text[0])
        message.append("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
            sentiment_response.confidence_scores.positive,
            sentiment_response.confidence_scores.neutral,
            sentiment_response.confidence_scores.negative,
        ))

        #grab the keyphrases
        message.append("Keyphrases: ")
        keyphrase_response = client.extract_key_phrases(documents = text)[0]
        for phrase in keyphrase_response.key_phrases:
            message.append("* {0} \n".format(phrase))

        #grab the keyphrases
        message.append("Entities: ")
        entities_response = client.recognize_entities(documents = text)[0]
        for entity in entities_response.entities:
            message.append("* {0} [{1}]\n".format(entity.text, entity.category))
        
        #return all of the messages in a sample output
        return render_template('sample_output.html', message=message)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

