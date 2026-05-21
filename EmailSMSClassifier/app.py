import streamlit as st
import pickle
import nltk
import string

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Spam Classifier",
    page_icon="📩",
    layout="centered"
)

# ---------------- NLTK ----------------
nltk.download('punkt')
nltk.download('stopwords')

ps = PorterStemmer()

# ---------------- LOAD FILES ----------------
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

# ---------------- PREPROCESS ----------------
def text_transform(text):

    text = text.lower()

    text = nltk.word_tokenize(text)

    y = []

    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

# ---------------- UI ----------------
st.title("📩 Email & SMS Spam Classifier")

input_sms = st.text_area(
    "Enter your message",
    height=150
)

if st.button("Analyze Message"):

    if input_sms.strip() == "":
        st.warning("Please enter a message")

    else:

        # preprocess
        transformed_sms = text_transform(input_sms)

        # vectorize
        vector_input = tfidf.transform([transformed_sms])

        # prediction
        result = model.predict(vector_input)[0]

        # probability
        probability = model.predict_proba(vector_input)[0]

        spam_prob = round(probability[1] * 100, 2)
        ham_prob = round(probability[0] * 100, 2)

        # output
        if result == 1:
            st.error(f"🚨 Spam Message ({spam_prob}%)")
        else:
            st.success(f"✅ Ham Message ({ham_prob}%)")

        # processed text
        with st.expander("Processed Text"):
            st.write(transformed_sms)

st.caption("Built using Streamlit + NLP + Machine Learning")