import json
import random
import pickle
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

nltk.download('punkt')


# Load intents
with open("intent.json") as file:
    intents = json.load(file)

X = []
y = []

for intent in intents['intents']:
    for pattern in intent['patterns']:
        X.append(pattern)
        y.append(intent['tag'])

# Tokenize and vectorize
from nltk.tokenize import wordpunct_tokenize
vectorizer = CountVectorizer(tokenizer=wordpunct_tokenize)

X_vec = vectorizer.fit_transform(X)

# Train classifier
clf = MultinomialNB()
clf.fit(X_vec, y)

# Save model and vectorizer
with open("model.pkl", "wb") as f:
    pickle.dump(clf, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open("classes.pkl", "wb") as f:
    pickle.dump(list(set(y)), f)

print("✅ Model trained and saved using Scikit-learn!")
