# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 15:41:25 2025

@author: DELL
"""

import pandas as pd
import re
from collections import defaultdict
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords

# Download stopwords if not already present
nltk.download('stopwords')

# === Step 1: Load dataset ===
file_path = r"C:\Users\DELL\Documents\year 3 degree\FINAL SEM\big data\Final assignment dataset\CNN_Articels_clean.csv"
df = pd.read_csv(file_path, encoding='utf-8')

text_column = "Article text"

# === Step 2: Prepare stopwords list ===
stop_words = set(stopwords.words('english'))
custom_stopwords = {"said", "photos"}  # dataset-specific common words
all_stopwords = stop_words.union(custom_stopwords)

# === Step 3: Mapper simulation with stopword removal ===
def mapper(text):
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', '', text)
    words = text.split()
    return [(word, 1) for word in words if word not in all_stopwords]

# === Step 4: Reducer ===
def reducer(mapped_data):
    word_count = defaultdict(int)
    for word, count in mapped_data:
        word_count[word] += count
    return word_count

# === Step 5: Run MapReduce locally ===
all_mapped = []
for article in df[text_column].dropna():
    all_mapped.extend(mapper(article))

word_counts = reducer(all_mapped)

# === Step 6: Convert to DataFrame & sort ===
wc_df = pd.DataFrame(list(word_counts.items()), columns=["Word", "Count"])
wc_df = wc_df.sort_values(by="Count", ascending=False)

# === Step 7: Save output ===
output_path = r"C:\Users\DELL\Documents\year 3 degree\FINAL SEM\big data\Final assignment dataset\trending_topics.txt"
wc_df.to_csv(output_path, sep="\t", header=False, index=False, encoding='utf-8')

print("\nTop 20 Words (stopwords removed):\n", wc_df.head(20))

# === Step 8: Horizontal bar chart ===
top_20 = wc_df.head(20)
plt.figure(figsize=(10, 6))
plt.barh(top_20["Word"], top_20["Count"], color="darkblue")
plt.xlabel("Frequency")
plt.ylabel("Words")
plt.title("Top 20 Meaningful Words from MapReduce Output")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()



