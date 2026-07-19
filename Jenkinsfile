pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        AWS_ACCOUNT_ID = credentials('aws-account-id')
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        IMAGE_NAME = 'image-ocr-converter'
        IMAGE_TAG = "${BUILD_NUMBER}"
        DOCKER_IMAGE = "${ECR_REGISTRY}/${IMAGE_NAME}"
    }

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo '=== Checking out code from repository ==='
                    checkout scm
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    echo '=== Building Docker image ==='
                    sh "docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} -t ${DOCKER_IMAGE}:latest ."
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo '=== Running tests ==='
                    sh "docker run --rm ${DOCKER_IMAGE}:${IMAGE_TAG} pytest tests/ -v --tb=short"
                }
            }
        }

        stage('Security Scan') {
            steps {
                script {
                    echo '=== Scanning for vulnerabilities ==='
                    // Optional: Use Trivy or similar
                    sh "docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image ${DOCKER_IMAGE}:${IMAGE_TAG} || true"
                }
            }
        }

        stage('Login to ECR') {
            steps {
                script {
                    echo '=== Authenticating with AWS ECR ==='
                    withAWS(credentials: 'aws-ecr-credentials', region: "${AWS_REGION}") {
                        sh '''
                            aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                        '''
                    }
                }
            }
        }

        stage('Push to ECR') {
            steps {
                script {
                    echo '=== Pushing image to AWS ECR ==='
                    sh '''
                        docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    echo '=== Cleaning up local Docker images ==='
                    sh "docker rmi ${DOCKER_IMAGE}:${IMAGE_TAG} || true"
                }
            }
        }
    }

    post {
        always {
            echo '=== Pipeline execution completed ==='
            cleanWs()
        }
        success {
            echo '✓ Build successful! Image pushed to ECR'
        }
        failure {
            echo '✗ Build failed. Check logs for details.'
        }
    }
}
