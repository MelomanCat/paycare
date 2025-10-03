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
                script {
                    sh "docker build --no-cache -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Use volume jenkins-data, common for both containers
                    sh """
                        docker run --rm \
                        -v jenkins-data:/var/jenkins_home \
                        -w /var/jenkins_home/workspace/${env.JOB_NAME} \
                        ${DOCKER_IMAGE} -m pytest tests/ --junitxml=report.xml
                    """
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
                script {
                    sh """
                        docker run --rm \
                        -v jenkins-data:/var/jenkins_home \
                        -w /var/jenkins_home/workspace/${env.JOB_NAME} \
                        ${DOCKER_IMAGE} etl.py ${INPUT_CSV} ${OUTPUT_CSV}
                    """
                }
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