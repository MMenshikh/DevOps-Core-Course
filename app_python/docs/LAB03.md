# LAB03 --- CI/CD Pipeline with GitHub Actions

## CI/CD Practices Applied

### Automated Builds

Docker image is automatically built on push and pull requests using
GitHub Actions.

### Secure Secrets Management

Sensitive data stored in GitHub Repository Secrets instead of hardcoding
credentials.

### Container Security Scanning

Snyk integrated into pipeline to scan Docker image for vulnerabilities.

### Continuous Delivery

Docker image automatically pushed to DockerHub after successful pipeline
execution.

------------------------------------------------------------------------

## Pipeline Information & Decisions

CI Platform: GitHub Actions\
Container Registry: DockerHub\
Security Scanner: Snyk

Triggers: - push to main - pull requests

Pipeline Stages: 1. Repository checkout 2. Docker image build 3.
Security scan with Snyk 4. DockerHub login 5. Image push to registry

------------------------------------------------------------------------

## Workflow Execution Process

### Automatic Trigger

Pipeline runs when:

-   code is pushed
-   pull request is created

### Build Stage

Docker image built using:

docker build -t devops-info-service .

### Security Scan

Snyk scans Docker image for known vulnerabilities before publishing.

### Push Stage

Image pushed to:

maksimmenshikh/devops-info-service

------------------------------------------------------------------------

## Technical Analysis

Automated CI reduces manual deployment steps and human error.

Secrets stored in GitHub prevent credential exposure in repository code.

Security scanning ensures vulnerabilities are detected early in
development.

Automated publishing guarantees consistent container versions.

------------------------------------------------------------------------

## Challenges & Solutions

### Missing Secrets

Pipeline failed due to missing repository secrets.\
Solved by adding DOCKERHUB_TOKEN, DOCKERHUB_USERNAME and SNYK_TOKEN.

### Docker Authentication Failure

Fixed by generating DockerHub access token and configuring
docker/login-action.

### Failed Security Scan

Resolved by rebuilding image and ensuring dependencies were up to date.
