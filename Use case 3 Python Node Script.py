# -*- coding: utf-8 -*-
"""
Created on Sun Aug 10 16:30:26 2025

@author: DELL
"""

import pandas as pd
import re
from collections import Counter
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# === 1. File Path ===
file_path = r"C:\Users\DELL\Documents\year 3 degree\FINAL SEM\big data\Final assignment dataset\CNN_Articles_clean.csv"
output_wordcloud = r"C:\Users\DELL\Documents\year 3 degree\FINAL SEM\big data\Final assignment dataset\UC3_keywords_wordcloud.png"

# === 2. Load dataset ===
df = pd.read_csv(file_path)
text_col = 'content' if 'content' in df.columns else df.columns[-1]

# === 3. Stopwords & tokenisation ===
custom_stopwords = set(STOPWORDS)
# Add extra irrelevant words if needed
custom_stopwords.update([
    'said', 'will', 'can', 'new', 'year', 'two', 'one', 'us', 'time',
    'also', 'first', 'last', 'make', 'may', 'many', 'much', 'since',
    'say', 'says', 'get', 'got', 'back', 'like'
])

def normalize_and_tokenize(text):
    if pd.isnull(text):
        return []
    text = text.lower()
    tokens = re.findall(r'[a-z]+', text)
    tokens = [t for t in tokens if len(t) > 2 and t not in custom_stopwords]
    return tokens

# === 4. Count word frequencies ===
all_tokens = []
for txt in df[text_col]:
    all_tokens.extend(normalize_and_tokenize(txt))

word_counts = Counter(all_tokens)

# === 5. Create Word Cloud ===
wc = WordCloud(width=1600, height=900, background_color='white', collocations=False)
wc.generate_from_frequencies(word_counts)

plt.figure(figsize=(14, 8))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title('Vocabulary Richness Keywords (UC3)', fontsize=18)
plt.tight_layout()
plt.show()

# Save
wc.to_file(output_wordcloud)
print(f"Word cloud saved to: {output_wordcloud}")


