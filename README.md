# Dataproc Workflow Templates

This repository contains Dataproc workflow templates for deploying and managing Apache Hadoop job on Google Cloud Platform.

## Getting Started

### Prerequisites

- A Google Cloud project with Cloud Build and Dataproc APIs enabled.
- A service account with the following roles:
  - Cloud Build Editor (`roles/cloudbuild.builds.editor`)
  - Workflows Admin (`roles/workflows.admin`)

### Workflow Templates

This repository includes an workflow template for Dataproc.

- `example-workflow-template.yaml`: A cloudbuild workflow template that will run a WordCount job using Hadoop on Dataproc.
- `wordcount.py`: Contains logic for Wordcount script in Python.

### Cloud Build Configuration

The repository is configured with a PubSub ad Cloud Build trigger to automatically import the workflow template into Dataproc whenever PubSub publishes the message.
