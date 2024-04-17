from flask import Flask, request, jsonify, render_template
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_validate, cross_val_predict
from sklearn.metrics import auc, roc_curve, roc_auc_score, accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import pandas as pd
import numpy as np
from feature_extractor import extract_features
from pickle import load
import shap


app = Flask(__name__, template_folder='views')

params = {
    'max_depth': 3,
    'objective': 'reg:logistic',
    'eval_metric': 'error'
}

scaler = load(open('scaler.pkl', 'rb'))
xgb = xgb.XGBClassifier(**params)
xgb.load_model("./xgboost_model.json")
feature_names = pd.read_csv("dataset_B_05_2020.csv").columns.tolist()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form
    text_input = data['text']
    print(text_input)
    text_features = []
    x = extract_features(text_input, "DUMMY")
    if not x:
        return render_template('results.html', prediction=None)
    x = x[1:-1]     #remove url and status column
    text_features.append(x)
    print(text_features)
    text_features = scaler.transform(text_features)
    prediction = xgb.predict(text_features)
    print(prediction[0])

    # view SHAP of test data
    explainer = shap.TreeExplainer(xgb, feature_names=feature_names[0:-1])
    shap_values = explainer(text_features)

    # analyze SHAP of features for first test sample
    val = shap_values[0].values
    print("val:\n")
    print(val)

    # get indices of features with top 5 SHAP values
    ind = np.argpartition(val, -5)[-5:]
    ind = ind[np.argsort(val[ind])]
    print("ind:\n")
    print(ind)

    # convert indices into feature names - can be displayed, after some
    # further processing, to the user
    # Initialize an empty list to store the top feature names
    top_5_features = []

    # Loop through the indices in 'ind' and select the corresponding feature names
    for index in ind:
        top_5_features.append(feature_names[index])
    #top_5_values = val[ind]
    print(top_5_features)
    if prediction[0] == 1:
        result = "Phishing"
    else:
        result = "Legitimate"
    return render_template('results.html', prediction=result, top_features=top_5_features)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)




