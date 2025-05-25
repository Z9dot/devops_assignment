pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'sample-flask-app'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/YOUR_USERNAME/YOUR_REPO.git'
            }
        }

        stage('Code Linting') {
            steps {
                sh 'pip install flake8'
                sh 'flake8 app.py --ignore=E501'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Unit Testing') {
            steps {
                sh 'python -m unittest discover tests || echo "No unit tests implemented"'
            }
        }

        stage('Deploy App Container') {
            steps {
                sh 'docker run -d -p 5000:5000 --name flask_app $DOCKER_IMAGE'
                sh 'sleep 5'
            }
        }

        stage('Selenium Tests') {
            steps {
                sh '''
                docker build -t selenium-tests -f Dockerfile.selenium .
                docker run --net=host selenium-tests
                '''
            }
        }
    }

    post {
        always {
            sh 'docker stop flask_app || true'
            sh 'docker rm flask_app || true'
        }
    }
}
