# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 17:54:20 2025

@author: DELL
"""

#!/usr/bin/env python3
import sys, csv, re

reader = csv.DictReader(sys.stdin)
nonword = re.compile(r"[^\w']+")         # keep words/apostrophes
is_time = re.compile(r"^\d{1,2}:\d{2}:\d{2}$")

STOPWORDS = set("""
a an the and or but if then of on in to for from by with at as is are was were be been being
""".split())

for row in reader:
    section = (row.get('section') or '').strip().lower()
    text = (row.get('text') or '')
    # normalize
    text = nonword.sub(' ', text.lower())
    for w in text.split():
        if w in STOPWORDS: continue
        if w.isdigit(): continue
        if is_time.match(w): continue          # <-- kills HH:MM:SS “words”
        if len(w) < 3: continue
        key = f"{section}|{w}"
        print(f"{key}\t1")

