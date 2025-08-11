# -*- coding: utf-8 -*-
"""
Created on Sun Aug 10 16:06:02 2025

@author: DELL
"""

#!/usr/bin/env python3
# MapperUC3: emits article_id, word, 1 for each token
import sys, csv, re
token_pattern = re.compile(r"[A-Za-z0-9]+")

def tokenize(text):
    if not isinstance(text, str):
        return []
    return token_pattern.findall(text.lower())

reader = csv.DictReader(sys.stdin)
for row in reader:
    article_id = row.get("Index", "").strip()
    content = row.get("Article text", "")
    if not article_id:
        continue
    for tok in tokenize(content):
        sys.stdout.write(f"{article_id}\t{tok}\t1\n")
