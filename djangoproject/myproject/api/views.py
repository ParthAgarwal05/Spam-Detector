import re
import pickle
from django.shortcuts import render
from django.http import HttpResponse
import nltk;
nltk.download("stopwords")
nltk.download("wordnet")
import sklearn;
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
with open('api/models/vectorizer.pkl', 'rb') as vec_file:
    vectorizer = pickle.load(vec_file)

with open('api/models/model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return ' '.join(words)
    
def main(request):
    prediction = None
    if request.method == 'POST':
        mail = request.POST.get('mail', '')
        prediction = predict(mail)
    return render(request, "api/index.html", {'prediction': prediction})

def predict(mail):
    mail_processed = preprocess_text(mail)
    mail_vectorized = vectorizer.transform([mail_processed])  # Note the list input
    prediction = model.predict(mail_vectorized)
    if prediction[0] == 0:
        return "Not Spam"
    else:
        return "Spam"

