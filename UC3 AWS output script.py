# -*- coding: utf-8 -*-
"""
Created on Sun Aug 10 16:16:10 2025

@author: DELL
"""

# === UC3 Word Clouds: Per-Article TTR & Avg TTR by Section ===
# Works in Spyder. Requires: pandas, matplotlib, wordcloud
# Install if needed: pip install wordcloud

import os
import math
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# ----------------------------
# 1) File paths (your provided)
# ----------------------------
path_agg = r"C:\Users\DELL\Documents\year 3 degree\FINAL SEM\big data\Final assignment dataset\UC3 output\agg_by_section.csv"
path_ttr = r"C:\Users\DELL\Documents\year 3 degree\FINAL SEM\big data\Final assignment dataset\UC3 output\per_article_ttr.csv"

out_dir = os.path.dirname(path_agg)
out_wc_agg = os.path.join(out_dir, "wc_agg_by_section.png")
out_wc_art = os.path.join(out_dir, "wc_per_article_ttr.png")

# -------------------------------------------------------
# 2) Helper: make word cloud from a {label: weight} dict
# -------------------------------------------------------
def make_wordcloud(freq_dict, title, outfile=None, width=1600, height=900):
    # Scale up weights so tiny decimals (e.g., 0.4 TTR) are visible
    # WordCloud uses relative frequencies; multiplying just improves contrast.
    scale_factor = 100.0
    scaled = {k: max(0, float(v) * scale_factor) for k, v in freq_dict.items() if isinstance(v, (int, float))}

    # Build & plot
    wc = WordCloud(
        width=width,
        height=height,
        background_color="white",
        prefer_horizontal=0.9,
        collocations=False,  # keep words as they are (no merging)
        normalize_plurals=False
    ).generate_from_frequencies(scaled)

    plt.figure(figsize=(width/100, height/100))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(title, fontsize=18, pad=12)
    plt.tight_layout()

    if outfile:
        wc.to_file(outfile)
        print(f"Saved: {outfile}")
    plt.show()

# -------------------------------------------
# 3) PER-ARTICLE TTR word cloud (Article->TTR)
#    Expected columns: 'article_id' (or 'title') and 'ttr'
# -------------------------------------------
df_art = pd.read_csv(path_ttr)

# Try to guess sensible columns if names differ
# Adjust these two lines if your column names are different.
label_col_art_candidates = [c for c in df_art.columns if c.lower() in ("article_id", "article", "title", "doc", "document")]
value_col_art_candidates = [c for c in df_art.columns if "ttr" in c.lower() or "ratio" in c.lower()]

label_col_art = label_col_art_candidates[0] if label_col_art_candidates else df_art.columns[0]
value_col_art = value_col_art_candidates[0] if value_col_art_candidates else df_art.select_dtypes(include="number").columns[-1]

# Clean & build dict
df_art2 = df_art[[label_col_art, value_col_art]].dropna()
# Optional: limit to top N by TTR for clarity
df_art2 = df_art2.sort_values(by=value_col_art, ascending=False).head(150)

freq_art = dict(zip(df_art2[label_col_art].astype(str), df_art2[value_col_art].astype(float)))

make_wordcloud(freq_art, "Vocabulary Richness (TTR) by Article", outfile=out_wc_art)

# -------------------------------------------
# 4) AGG BY SECTION word cloud (Section->Avg_TTR)
#    Expected columns: 'section' and 'avg_ttr'
# -------------------------------------------
df_agg = pd.read_csv(path_agg)

label_col_sec_candidates = [c for c in df_agg.columns if "section" in c.lower()]
value_col_sec_candidates = [c for c in df_agg.columns if ("avg" in c.lower() and "ttr" in c.lower()) or "ttr" in c.lower()]

label_col_sec = label_col_sec_candidates[0] if label_col_sec_candidates else df_agg.columns[0]
value_col_sec = value_col_sec_candidates[0] if value_col_sec_candidates else df_agg.select_dtypes(include="number").columns[-1]

df_agg2 = df_agg[[label_col_sec, value_col_sec]].dropna()
freq_sec = dict(zip(df_agg2[label_col_sec].astype(str), df_agg2[value_col_sec].astype(float)))

make_wordcloud(freq_sec, "Average Vocabulary Richness (TTR) by Section", outfile=out_wc_agg)

# ----------------------
# 5) Quick sanity prints
# ----------------------
print("\nDetected columns:")
print(f"- Per-article: label='{label_col_art}', value='{value_col_art}'")
print(f"- By-section:  label='{label_col_sec}', value='{value_col_sec}'")
print("Done.")
