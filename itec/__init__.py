from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'afb106f085decea3730314f4b5c92d6c'
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

from itec import routes