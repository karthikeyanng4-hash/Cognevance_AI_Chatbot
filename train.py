import json
import pickle
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# Load intents

with open("intents.json", "r", encoding="utf-8") as file:

    data = json.load(file)


patterns = []

tags = []


for intent in data["intents"]:

    for pattern in intent["patterns"]:

        patterns.append(pattern.lower())

        tags.append(intent["tag"])


print("Training data loaded successfully!")

print(f"Total training patterns: {len(patterns)}")

print(f"Total intents: {len(set(tags))}")


# Vectorizer

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(patterns)


# Model

model = LogisticRegression(
    max_iter=2000
)

model.fit(X, tags)


# Save

with open("chatbot_model.pkl", "wb") as file:

    pickle.dump(model, file)


with open("vectorizer.pkl", "wb") as file:

    pickle.dump(vectorizer, file)


print("\n🤖 Training completed successfully!")

print("Model saved: chatbot_model.pkl")

print("Vectorizer saved: vectorizer.pkl")