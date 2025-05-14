import pickle
import json
import random
from nltk.tokenize import wordpunct_tokenize


with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("intent.json") as file:
    intents = json.load(file)


def predict_intent(text):
    vec = vectorizer.transform([text])
    prediction = model.predict(vec)[0]
    return prediction

def get_response(text):
    intent = predict_intent(text)
    for i in intents['intents']:
        if i['tag'] == intent:
            return random.choice(i['responses'])
    return "Sorry, I didn't understand that."


if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        print("Bot:", get_response(user_input))
