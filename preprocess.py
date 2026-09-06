import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("wordnet")

# Create lemmatizer
lemmatizer = WordNetLemmatizer()

# Load the intents dataset
with open("intents.json", "r") as file:
    data = json.load(file)

print("NLP Preprocessing Started...\n")

# Process each intent and pattern
for intent in data["intents"]:
    print(f"Intent: {intent['tag']}")

    for pattern in intent["patterns"]:

        # Convert sentence into words
        words = word_tokenize(pattern)

        # Convert words to lowercase and base form
        processed_words = [
            lemmatizer.lemmatize(word.lower())
            for word in words
            if word.isalnum()
        ]

        print(f"Original: {pattern}")
        print(f"Processed: {processed_words}\n")