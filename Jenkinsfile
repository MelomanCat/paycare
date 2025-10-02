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
                sh """
                docker build -f Dockerfile -t etl-test .
                docker run --rm etl-test pytest tests/ --junitxml=report.xml
                """
            }
            post {
                always {
                    junit 'report.xml'
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