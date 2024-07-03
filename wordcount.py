#!/usr/bin/env python3
import sys
from google.cloud import storage

def read_from_gcs(input_path):
    """Read data from GCS."""
    storage_client = storage.Client()
    bucket_name, blob_name = input_path.split('/', 3)[-1].split('/', 1)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    content = blob.download_as_string().decode('utf-8')
    return content

def word_count_mapper(content):
    """Perform word count."""
    word_counts = {}
    for line in content.splitlines():
        words = line.strip().split()
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
    return word_counts

def write_to_gcs(output_path, word_counts):
    """Write results to GCS."""
    storage_client = storage.Client()
    bucket_name, blob_name = output_path.split('/', 3)[-1].split('/', 1)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    output_data = '\n'.join([f'{word}\t{count}' for word, count in word_counts.items()])
    blob.upload_from_string(output_data)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python wordcount.py <input_gcs_path> <output_gcs_path>")
        sys.exit(1)

    input_gcs_path = sys.argv[1]
    output_gcs_path = sys.argv[2]

    # Read data from GCS
    input_data = read_from_gcs(input_gcs_path)

    # Perform word count
    word_counts = word_count_mapper(input_data)

    # Write results to GCS
    write_to_gcs(output_gcs_path, word_counts)
