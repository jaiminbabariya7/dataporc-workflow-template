# Dataproc Workflow Templates

This repository contains Dataproc workflow templates for deploying and managing Apache Hadoop and Spark jobs on Google Cloud Platform.

## Getting Started

### Prerequisites

- A Google Cloud project with Cloud Build and Dataproc APIs enabled.
- A service account with the following roles:
  - Cloud Build Editor (`roles/cloudbuild.builds.editor`)
  - Workflows Admin (`roles/workflows.admin`)

### Workflow Templates

This repository includes an example workflow template for Dataproc.

- `example-workflow-template.yaml`: A sample workflow template that demonstrates a simple WordCount job using Hadoop on Dataproc.

### Cloud Build Configuration

The repository is configured with a Cloud Build trigger to automatically import the workflow template into Dataproc whenever changes are pushed to the main branch.

#### cloudbuild.yaml

```yaml
steps:
- name: 'gcr.io/cloud-builders/git'
  args: ['clone', '--single-branch', '--depth=1', 'https://github.com/$GITHUB_USERNAME/$REPO_NAME.git', 'src']
- name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
  args: ['dataproc', 'workflow-templates', 'import', 'src/$TEMPLATE_FILE']

substitutions:
  _GITHUB_USERNAME: 'jaiminbabariya7'
  _REPO_NAME: 'dataproc-workflow-template'
  _TEMPLATE_FILE: 'example-workflow-template.yaml'

trigger:
  github:
    owner: $_GITHUB_USERNAME
    name: $_REPO_NAME
    push:
      branch: '^main$'
