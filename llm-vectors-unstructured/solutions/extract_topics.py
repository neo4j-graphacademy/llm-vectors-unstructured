from textblob import TextBlob

phrase = "You can extract topics from phrases using TextBlob"

topics = TextBlob(phrase).noun_phrases

print(topics)