# Deployment Guide: Docker, Jenkins & AWS ECR

## Prerequisites

1. **AWS Account Setup**
   - Create ECR repository: `image-ocr-converter`
   - Create IAM user with ECR push permissions
   - Generate AWS Access Key ID and Secret Access Key

2. **Jenkins Setup**
   - Jenkins server running (version 2.350+)
   - Docker plugin installed
   - AWS Credentials plugin installed
   - Pipeline plugin installed

3. **Local Tools**
   - Docker installed
   - Docker Compose installed
   - AWS CLI configured

## Step 1: Configure Jenkins Credentials

1. Navigate to Jenkins Dashboard
2. Go to Manage Jenkins → Manage Credentials
3. Add AWS Credentials:
   - Kind: AWS Credentials
   - ID: `aws-ecr-credentials`
   - Access Key ID: `<your-access-key>`
   - Secret Access Key: `<your-secret-key>`

4. Add GitHub Credentials (if needed):
   - Kind: Username with password
   - ID: `github-credentials`

## Step 2: Create Jenkins Pipeline Job

1. Create new "Pipeline" job
2. Configure repository URL: `https://github.com/ApsalBehath26/image-ocr-converter.git`
3. Set branch to `*/main`
4. Set Pipeline script from SCM:
   - SCM: Git
   - Repository URL: `https://github.com/ApsalBehath26/image-ocr-converter.git`
   - Script Path: `Jenkinsfile`

## Step 3: Configure Environment Variables

In Jenkins job configuration, add:

```
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=<your-account-id>
ECR_REGISTRY=<account-id>.dkr.ecr.us-east-1.amazonaws.com
IMAGE_NAME=image-ocr-converter
IMAGE_TAG=latest
```

## Step 4: Push to AWS ECR

The Jenkinsfile automatically:
1. Builds Docker image
2. Authenticates with ECR
3. Tags image with ECR registry
4. Pushes image to ECR

Manual push (if needed):

```bash
# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag image
docker tag image-ocr-converter:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/image-ocr-converter:latest

# Push to ECR
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/image-ocr-converter:latest
```

## Step 5: Verify Deployment

```bash
# List ECR images
aws ecr describe-images --repository-name image-ocr-converter --region us-east-1

# Pull and run image locally
docker pull <account-id>.dkr.ecr.us-east-1.amazonaws.com/image-ocr-converter:latest
docker run -p 5000:5000 <account-id>.dkr.ecr.us-east-1.amazonaws.com/image-ocr-converter:latest
```

## Troubleshooting

### Jenkins Build Fails
- Check Jenkins logs: `docker logs jenkins`
- Verify Docker socket is mounted
- Ensure AWS credentials are correct

### ECR Push Fails
- Verify IAM user has `ecr:*` permissions
- Check AWS credentials in Jenkins
- Ensure ECR repository exists

### Docker Build Issues
- Clear Docker cache: `docker system prune -a`
- Check internet connectivity
- Verify Dockerfile syntax

## CI/CD Pipeline Flow

```
Git Push → Jenkins Trigger → Build Docker Image → Run Tests 
→ Tag Image → Login to ECR → Push to ECR → Deployment Ready
```
