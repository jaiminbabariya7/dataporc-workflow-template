#!/usr/bin/env python3
import sys
from google.cloud import storage

def read_input_from_gcs(bucket_name, input_file_path):
    """Reads input from a file stored in GCS."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(input_file_path)
    return blob.download_as_text()

def write_output_to_gcs(bucket_name, output_file_path, output_data):
    """Writes output to a file in GCS."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(output_file_path)
    blob.upload_from_string(output_data)

def word_count_mapper(input_data):
    """Performs word count mapping."""
    word_counts = {}
    for line in input_data.splitlines():
        line = line.strip()
        words = line.split()
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
    return word_counts

def word_count_reducer(word_counts):
    """Performs word count reducing."""
    output_data = []
    for word, count in word_counts.items():
        output_data.append(f'{word}\t{count}')
    return '\n'.join(output_data)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: wordcount.py <bucket_name> <input_file_path> <output_file_path>")
        sys.exit(1)

    bucket_name = sys.argv[1]
    input_file_path = sys.argv[2]
    output_file_path = sys.argv[3]

    # Read input data from GCS
    input_data = read_input_from_gcs(bucket_name, input_file_path)

    # Perform word count mapping
    word_counts = word_count_mapper(input_data)

    # Perform word count reducing
    output_data = word_count_reducer(word_counts)

    # Write output data to GCS
    write_output_to_gcs(bucket_name, output_file_path, output_data)
