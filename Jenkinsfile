pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "etl-image:latest"
        INPUT_CSV = "input.csv"
        OUTPUT_CSV = "output.csv"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                // Build image
                sh "docker build --no-cache -t ${DOCKER_IMAGE} ."
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    docker.image('etl-image:latest').inside {
                        sh 'pytest tests/ --junitxml=report.xml'
                    }
                }
            }
            post {
                always {
                    junit 'report.xml'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                // Run ETL script
                sh "docker run --rm -v \$(pwd)/${INPUT_CSV}:/app/${INPUT_CSV} -v \$(pwd)/${OUTPUT_CSV}:/app/${OUTPUT_CSV} ${DOCKER_IMAGE} etl.py ${INPUT_CSV} ${OUTPUT_CSV}"
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