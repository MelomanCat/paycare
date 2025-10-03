pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "etl-image:latest"
        INPUT_CSV = "input.csv"
        OUTPUT_CSV = "output.xml"
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
                    // Запускаем тесты и сохраняем report.xml через volume
                    sh """
                        docker run --rm \
                        -v \$(pwd):/output \
                        -w /app \
                        --entrypoint /bin/sh \
                        ${DOCKER_IMAGE} -c 'python3 -m pytest tests/ --junitxml=/output/report.xml -v'
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
                        -w /var/jenkins_home/workspace/\${JOB_NAME} \
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