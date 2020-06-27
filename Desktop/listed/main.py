import os
from flask import Flask, request, render_template
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

COGSVCS_KEY = os.getenv('COGSVCS_KEY')
COGSVCS_CLIENTURL = os.getenv('COGSVCS_CLIENTURL')

@app.route('/', methods=['GET', 'POST'])
def main():
    return 'Boo, World!'