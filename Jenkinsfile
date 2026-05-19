pipeline {
    agent any

    environment {
        IMAGE_NAME = "fitness-tracker"
        CONTAINER_NAME = "fitness-tracker-container"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME% .'
            }
        }

        stage('Stop Old Container') {
            steps {
                bat '''
                docker stop %CONTAINER_NAME% || exit 0
                docker rm %CONTAINER_NAME% || exit 0
                '''
            }
        }

        stage('Run Docker Container') {
            steps {
                bat 'docker run -d -p 5001:5000 --name %CONTAINER_NAME% %IMAGE_NAME%'
            }
        }
    }

    post {
        success {
            echo 'Deployment Successful!'
        }

        failure {
            echo 'Pipeline Failed!'
        }
    }
}