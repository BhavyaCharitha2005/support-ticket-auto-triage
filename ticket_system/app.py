from flask import Flask, request, jsonify
import pickle
import re
import numpy as np

app = Flask(__name__)

# Load the trained model and vectorizer
def load_model():
    with open('ticket_classifier_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('tfidf_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    return model, vectorizer

model, vectorizer = load_model()

# Text cleaning function
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = ' '.join(text.split())
    return text

@app.route('/')
def home():
    return "Customer Support Ticket Auto-Triage API - Use POST /classify"

@app.route('/classify', methods=['POST'])
def classify_ticket():
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        subject = data.get('subject', '')
        description = data.get('description', '')
        
        if not subject or not description:
            return jsonify({'error': 'Please provide both subject and description'}), 400
        
        # Combine and clean
        full_text = subject + ' ' + description
        cleaned_text = clean_text(full_text)
        
        # Transform and predict
        text_vector = vectorizer.transform([cleaned_text])
        prediction = model.predict(text_vector)[0]
        confidence = float(model.predict_proba(text_vector)[0].max())
        
        response = {
            'ticket_category': prediction,
            'confidence': confidence,
            'status': 'success'
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

if __name__ == '__main__':
    print("Starting API server...")
    app.run(debug=True)
