pipeline {
    agent any

    environment {
        IMAGE_NAME = "fitness-tracker"
        CONTAINER_NAME = "fitness-container"
    }

    stages {

        stage('Clone Repository') {
            steps {
                git 'https://github.com/2023cssrujankumarkd-eng/Fitness-tracker.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh '''
                docker stop $CONTAINER_NAME || true
                docker rm $CONTAINER_NAME || true
                '''
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker run -d -p 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME'
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