import os
from flask import Flask, request, render_template
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from text_analytics import TextAnalytics

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
        text_chunks = [text[i:i+1024] for i in range(0, len(text), 1024)]

        #run text analytics on the input
        text_analytics_message = TextAnalytics(COGSVCS_CLIENTURL, COGSVCS_KEY, text_chunks)    

        #return all of the messages in a sample output
        return render_template('sample_output.html', message=text_analytics_message)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

