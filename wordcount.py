#!/usr/bin/env python3
import sys
from google.cloud import storage

def read_from_gcs(input_path):
    """Reads data from a GCS file."""
    storage_client = storage.Client()
    bucket_name, blob_name = input_path.split('/', 3)[-1].split('/', 1)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    content = blob.download_as_string().decode('utf-8')
    return content

def word_count_mapper(content):
    """Performs word count."""
    word_counts = {}
    for line in content.splitlines():
        words = line.strip().split()
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
    return word_counts

def write_to_gcs(output_path, word_counts):
    """Writes results to a GCS file."""
    storage_client = storage.Client()
    bucket_name, blob_name = output_path.split('/', 3)[-1].split('/', 1)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    output_data = '\n'.join(f'{word}\t{count}' for word, count in word_counts.items())
    blob.upload_from_string(output_data)

if __name__ == "__main__":
    # Specify your input and output paths
    input_path = 'gs://workflow_buckt/input_data/input.txt'
    output_path = 'gs://workflow_buckt/output_data/output.txt'

    # Read input data from GCS
    input_data = read_from_gcs(input_path)

    # Map function (word count)
    word_counts = word_count_mapper(input_data)

    # Write output data to GCS
    write_to_gcs(output_path, word_counts)
