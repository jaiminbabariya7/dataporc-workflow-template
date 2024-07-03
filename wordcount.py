#!/usr/bin/env python3
import sys
from google.cloud import storage
from google.cloud.exceptions import NotFound

def read_from_gcs(bucket_name, file_name):
    """Read content from a file in GCS."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        content = blob.download_as_string().decode('utf-8')
        return content.splitlines()
    except NotFound as e:
        print(f"File '{file_name}' not found in bucket '{bucket_name}'. Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading from GCS bucket '{bucket_name}' file '{file_name}': {e}")
        sys.exit(1)

def write_to_gcs(bucket_name, file_name, content):
    """Write content to a file in GCS."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(content)

def mapper(lines):
    """Mapper function for word count."""
    word_count = {}
    for line in lines:
        line = line.strip()
        words = line.split()
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
    
    # Prepare output in tab-separated format
    output_lines = [f'{word}\t{count}' for word, count in word_count.items()]
    return '\n'.join(output_lines)

def reducer(lines):
    """Reducer function for word count (summing up counts)."""
    word_count = {}
    for line in lines:
        word, count = line.split('\t')
        if word in word_count:
            word_count[word] += int(count)
        else:
            word_count[word] = int(count)
    
    # Prepare output in tab-separated format
    output_lines = [f'{word}\t{count}' for word, count in word_count.items()]
    return '\n'.join(output_lines)

if __name__ == "__main__":

    bucket_name = 'workflow_buckt'
    input_file = 'input_data/input.txt'
    output_file = 'output_data/output.txt'

    # Read input from GCS
    lines = read_from_gcs(bucket_name, input_file)

    # Process using both mapper and reducer
    mapper_output = mapper(lines)
    reducer_output = reducer(mapper_output.splitlines())

    # Write output to GCS
    write_to_gcs(bucket_name, output_file, reducer_output)
