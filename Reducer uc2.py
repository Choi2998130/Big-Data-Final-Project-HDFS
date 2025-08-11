# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 17:54:44 2025

@author: DELL
"""

#!/usr/bin/env python3
import sys

cur_key = None
cur_sum = 0

for line in sys.stdin:
    line = line.rstrip('\n')
    if not line: continue
    key, val = line.split('\t', 1)
    if key != cur_key and cur_key is not None:
        section, word = cur_key.split('|', 1)
        print(f"{section}\t{word}\t{cur_sum}")
        cur_sum = 0
    cur_key = key
    try:
        cur_sum += int(val)
    except ValueError:
        pass

if cur_key is not None:
    section, word = cur_key.split('|', 1)
    print(f"{section}\t{word}\t{cur_sum}")

