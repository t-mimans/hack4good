import os
from flask import Flask, request, render_template
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from text_analytics import TextAnalytics
from contentmoderation import text_moderation
import urllib.request 
import urllib.error
import json 

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
        #grab the input text
        text = request.form['text_input']
        text_chunks = [text[i:i+1020] for i in range(0, len(text), 1024)]
        
        # some additional variables
        highlighted = text
        hate_score = 0
        hate_words = []

        sentiment_message, entity_message, keyphrase_message = TextAnalytics(COGSVCS_CLIENTURL, COGSVCS_KEY, text_chunks)    
        
        for chunk in text_chunks:
            toxic_words = text_moderation(COGSVCS_CLIENTURL, COGSVCS_KEY, chunk)
            
            if "terms" in toxic_words:
                for term in toxic_words['terms']:
                    if term['term'] not in hate_words:
                        highlighted = highlighted.replace(term['term'], "<mark>" + term['term'] + "</mark>")
                        hate_words.append(term['term'])

            hate_score += get_hate_score(chunk)

        #return all of the messages in a sample output
        return render_template('report.html', text_highlighted=highlighted, positive=sentiment_message[0], neutral=sentiment_message[1], negative=sentiment_message[2], entities=entity_message, keyphrases=keyphrase_message, hate=str(hate_score*100), hatefulwords=hate_words)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

def get_hate_score(text):
    data =  {
        "Inputs": {
            "input1":
                {
                    "ColumnNames": ["id", "label", "tweet"],
                    "Values": [ [ "0", "0", text],]
                    },        },
                "GlobalParameters": {}
    }

    body = str.encode(json.dumps(data))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/75e2e65c01754c3f8d498e08a7c73e3b/services/48ce6baf8ee64b1e9ce0ab44d1a66da4/execute?api-version=2.0&details=true'
    api_key = 'PWLiMLplJTtcrX3S7v6X6kXNLB1uUSOhNHTHMfdMivroAl/S8y95n+tdD1w7EFjMRwqJxVxi8VJPFEC/W6Q3kQ=='
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    
    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        result_str = str(result)
        result_str = result_str[result_str.index("Values"):]
        result_str = result_str[15:-8]

        if result_str.count("-") > 0:
            return 0
        else: 
            return float(result_str)
    
    except urllib.error.HTTPError as error:
        return 0
        print("The request failed with status code: " + str(error.code))
        print(error.info())
        print(json.loads(error.read())) 
