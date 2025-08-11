# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 19:08:14 2025

@author: DELL
"""

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import re

# Download required nltk data once
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Load CSV file
file_path = r"C:\Users\DELL\Documents\year 3 degree\FINAL SEM\big data\Final assignment dataset\CNN_Articles_clean.csv"
df = pd.read_csv(file_path)

# Column with article text
text_col = 'Article text'

# Prepare NLP tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = str(text).lower()                             # lowercase
    text = re.sub(r'[^a-z\s]', '', text)                 # remove non-alpha chars
    tokens = text.split()                                # split into words
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words and len(t) > 2]  # filter and lemmatize
    return tokens

# Combine all words from all articles
all_words = []
for text in df[text_col]:
    all_words.extend(preprocess_text(text))

# Count word frequencies
word_freq = {}
for word in all_words:
    word_freq[word] = word_freq.get(word, 0) + 1

# Generate and plot word cloud
wc = WordCloud(width=1600, height=800, background_color='white',
               colormap='plasma', max_words=200).generate_from_frequencies(word_freq)

plt.figure(figsize=(14,7))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title("Combined Word Cloud - Use Case 2 (All Sections)", fontsize=18, fontweight='bold')
plt.show()


 