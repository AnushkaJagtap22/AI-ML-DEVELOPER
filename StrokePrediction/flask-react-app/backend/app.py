from flask import Flask, request, jsonify
import pandas as pd
from joblib import load
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "stroke_model.joblib"
)

model = load(MODEL_PATH)

print("Model loaded successfully!")