from flask import Flask, request, jsonify, render_template
from email_validator import validate_email, EmailNotValidError
import spacy
import joblib

app = Flask(__name__)

# Load your model and NLP pipeline
model = joblib.load('model.pkl')
nlp = spacy.load('en_core_web_sm')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    try:
        data = request.get_json()
        text = data.get('text')

        if not text:
            return jsonify({"result": False, "message": "No text provided."}), 400

        # Check email validity
        is_email = False
        try:
            validate_email(text)
            is_email = True
        except EmailNotValidError:
            is_email = False

        # NLP processing
        doc = nlp(text)
        suspicious_keywords = ["urgent", "verify", "password", "account", "click here","link","URL","url"]
        found_keywords = [token.text.lower() for token in doc if token.text.lower() in suspicious_keywords]

        # Model prediction
        cleaned_text = ' '.join([token.text for token in doc])
        prediction = model.predict([cleaned_text])
        is_suspicious = prediction[0] == 1

        if is_suspicious or found_keywords:
            return jsonify({"result": False, "message": "The email/text is suspicious."})
        else:
            return jsonify({"result": True, "message": "The email/text appears to be legitimate."})

    except Exception as e:
        return jsonify({"result": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
