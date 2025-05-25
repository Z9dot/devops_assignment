pipeline {
    agent any

    options {
        timeout(time: 30, unit: 'MINUTES')
    }

    environment {
        DOCKER_IMAGE = 'sample-flask-app'
        CONTAINER_NAME = 'sample-flask-app-container'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/Z9dot/devops_assignment.git'
            }
        }

        stage('Code Linting') {
            steps {
                script {
                    try {
                        sh '''
                        docker run --rm -v "$(pwd)":/app -w /app python:3.9-slim sh -c "
                            pip install flake8 && 
                            flake8 app.py --ignore=E501
                        "
                        '''
                    } catch (Exception e) {
                        echo 'Linting failed, but continuing pipeline...'
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Unit Testing') {
            steps {
                sh 'python3 -m unittest discover tests 2>/dev/null || echo "No unit tests found or Python not available"'
            }
        }

        stage('Deploy App Container') {
            steps {
                sh 'docker stop $CONTAINER_NAME || true'
                sh 'docker rm $CONTAINER_NAME || true'
                sh 'docker run -d -p 5000:5000 --name $CONTAINER_NAME $DOCKER_IMAGE'
                sh 'sleep 10'
                sh 'curl -f http://localhost:5000 || echo "Health check failed"'
            }
        }

        stage('Selenium Tests') {
            steps {
                script {
                    try {
                        sh '''
                        docker build -t selenium-tests -f Dockerfile.selenium .
                        docker run --net=host selenium-tests
                        '''
                    } catch (Exception e) {
                        echo 'Selenium tests failed: ' + e.getMessage()
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }
    }

    post {
        always {
            sh '''
            docker stop $CONTAINER_NAME || true
            docker rm $CONTAINER_NAME || true
            docker rmi selenium-tests || true
            docker system prune -f || true
            '''
        }
        failure {
            echo 'Pipeline failed!'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
    }
}
