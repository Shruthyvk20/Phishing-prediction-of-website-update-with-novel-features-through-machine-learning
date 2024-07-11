import pandas as pd
from flask import render_template, Flask, request
import pickle

app = Flask(__name__, template_folder='templates')

# Load the pickled model
phish_model = pickle.load(open('model.pkl', 'rb'))

# Load the CSV file
df1 = pd.read_csv('phish_predict.csv')
df2 = pd.read_csv('final_dataset.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict.html')
def formpg():
    return render_template('predict.html')

@app.route('/submit', methods=['POST'])
def predict():
    url = request.form['url']
    # Get the features for the URL from the model
    features_names = ['URL_length', 'privacy_policy', 'contact_information', 'feedback_score',
       'load_time', 'broken_links', 'new_tech', 'time_elapsed',
       'content_similarity', 'update_frequency', 'number_of_changes','update_size', 'certificate_authority', 'SSL_encrption_strength',
       'self_signed_certificate', 'digital_signature_validity',
       'san_matches_domain', 'trusted_seal', 'certification_bey_validity',
       'certification_not_expired', 'certification_revocation_status']
    row = df1.loc[df1['URL'] == url]
    if not row.empty:
        index = row.index[0]
        # Get the features for that URL from the model
        features = df2.iloc[index][features_names].values
        # Predict using the model
        model_predict = phish_model.predict([features])
        if model_predict == 0:
           return render_template('submit.html', prediction_text='This is predicted as a legitimate website')
        else:
           return render_template('submit.html', prediction_text='This is predicted as a phishing website')
    else:
       return render_template('submit.html')

if __name__ == "__main__":
    app.run(debug=True)
