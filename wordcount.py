#!/usr/bin/env python3
import sys

def word_count_mapper():
    word_counts = {}
    for line in sys.stdin:
        line = line.strip()
        words = line.split()
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
    return word_counts

def word_count_reducer(word_counts):
    for word, count in word_counts.items():
        print(f'{word}\t{count}')

if __name__ == "__main__":
    word_counts = word_count_mapper()
    word_count_reducer(word_counts)
