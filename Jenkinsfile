pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "my-etl-image:latest"
        INPUT_CSV = "input.csv"
        OUTPUT_CSV = "output.csv"
    }

    stages {
        

        stage('Run Tests') {
            steps {
                sh 'pytest tests/ --junitxml=report.xml'
            }
            post {
                always {
                    junit 'report.xml'  // publish results
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }

        stage('Run Docker Container') {
            steps {
                sh "docker run --rm -v \$(pwd)/${INPUT_CSV}:/app/${INPUT_CSV} -v \$(pwd)/${OUTPUT_CSV}:/app/${OUTPUT_CSV} ${DOCKER_IMAGE}"
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
            
        }
        failure {
            echo 'Pipeline failed!'
            
        }
    }
}