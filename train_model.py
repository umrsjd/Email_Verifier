import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Example of loading a larger dataset (update with actual dataset)
# df = pd.read_csv('emails.csv')  # Assume a CSV file with columns 'text' and 'label'

# Example training data
texts = ["This is a legitimate email.", "This is a phishing attempt.", "Please click this link to win a prize!", "Your account has been compromised."]
labels = [1, 0, 0, 0]

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', GradientBoostingClassifier())
])

pipeline.fit(X_train, y_train)

# Evaluate the model
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))

# Save the model
joblib.dump(pipeline, 'model.pkl')
