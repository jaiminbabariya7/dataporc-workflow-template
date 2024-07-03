#!/usr/bin/env python3
import sys

def mapper():
    for line in sys.stdin:
        line = line.strip()
        words = line.split()
        for word in words:
            print(f'{word}\t1')

def reducer():
    current_word = None
    current_count = 0
    word = None

    for line in sys.stdin:
        line = line.strip()
        word, count = line.split('\t', 1)
        try:
            count = int(count)
        except ValueError:
            continue

        if current_word == word:
            current_count += count
        else:
            if current_word:
                print(f'{current_word}\t{current_count}')
            current_count = count
            current_word = word

    if current_word == word:
        print(f'{current_word}\t{current_count}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python wordcount.py [mapper|reducer]")
        sys.exit(1)

    if sys.argv[1] == 'mapper':
        mapper()
    elif sys.argv[1] == 'reducer':
        reducer()
    else:
        print("Invalid argument. Use 'mapper' or 'reducer'.")
        sys.exit(1)
