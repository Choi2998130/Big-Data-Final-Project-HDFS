# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 18:59:06 2025

@author: DELL
"""

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import re

# Download NLTK data if needed
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Load file safely: 
file_path = r"C:\Users\DELL\Documents\year 3 degree\FINAL SEM\big data\Final assignment dataset\uc2_results_top_by_alphabet.txt"

# Read CSV without header, and assign column names explicitly
df = pd.read_csv(file_path, sep="\t", header=None, names=['word', 'count'])

# Remove rows where count is not numeric (e.g., header rows)
df = df[pd.to_numeric(df['count'], errors='coerce').notnull()]

# Convert 'count' to numeric type explicitly
df['count'] = df['count'].astype(float)

# Proceed with rest of your preprocessing
df['word'] = df['word'].str.lower()
df['word'] = df['word'].apply(lambda x: re.sub(r'[^a-z]', '', x))
df = df[df['word'] != '']

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_word(w):
    if w in stop_words or len(w) < 3:
        return ''
    return lemmatizer.lemmatize(w)

df['processed_word'] = df['word'].apply(preprocess_word)
df = df[df['processed_word'] != '']

word_freq = df.groupby('processed_word')['count'].sum().to_dict()

wc = WordCloud(width=1600, height=800, background_color='white', colormap='plasma',
               max_words=200, min_font_size=10, max_font_size=200).generate_from_frequencies(word_freq)

plt.figure(figsize=(14,7))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title("Combined Word Cloud - Use Case 2 (Keyword Bias / Framing)", fontsize=18, fontweight='bold')
plt.tight_layout()
plt.show()


