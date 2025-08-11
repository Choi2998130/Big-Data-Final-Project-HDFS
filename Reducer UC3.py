# -*- coding: utf-8 -*-
"""
Created on Sun Aug 10 16:06:19 2025

@author: DELL
"""

#!/usr/bin/env python3
# ReducerUC3: aggregates by article_id to compute total, unique, TTR
import sys

current_article = None
total_count = 0
unique_words = set()

def flush(article_id, total, unique_words):
    if article_id is None:
        return
    uniq = len(unique_words)
    ttr = (uniq / total) if total else 0.0
    sys.stdout.write(f"{article_id}\t{uniq}\t{total}\t{ttr:.6f}\n")

for line in sys.stdin:
    parts = line.strip().split("\t")
    if len(parts) < 3:
        continue
    article_id, word, count_str = parts[0], parts[1], parts[2]
    if current_article is None:
        current_article = article_id
    if article_id != current_article:
        flush(current_article, total_count, unique_words)
        current_article = article_id
        total_count = 0
        unique_words = set()
    try:
        c = int(count_str)
    except:
        c = 1
    total_count += c
    unique_words.add(word)

flush(current_article, total_count, unique_words)
