from flask import Flask, request, jsonify, render_template
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_validate, cross_val_predict
from sklearn.metrics import auc, roc_curve, roc_auc_score, accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import pandas as pd
import numpy as np
from feature_extractor import extract_features


app = Flask(__name__, template_folder='views')

params = {
    'max_depth': 3,
    'objective': 'reg:logistic',
    'eval_metric': 'error'
}

scaler = StandardScaler()
xgb = xgb.XGBClassifier(**params)
xgb.load_model("./xgboost_model.json")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form
    text_input = data['text']
    print(text_input)
    text_features = []
    text_features.append(extract_features(text_input, "Legitimate"))
    print(text_features)
    text_features[0] = text_features[0][1:-1]
    text_features = scaler.fit_transform(text_features)
    prediction = xgb.predict(text_features)
    print(prediction[0])
    #return jsonify({'prediction': int(prediction[1])})
    if prediction[0] == 1:
        result = "Phishing"
    else:
        result = "Legitimate"
    return render_template('results.html', prediction=result)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)




