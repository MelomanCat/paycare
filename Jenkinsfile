pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "etl-image:latest"
        INPUT_CSV = "input.csv"
        OUTPUT_CSV = "output.csv"
    }

    stages {
        stage('Check Workspace') {
            steps {
                script {
                    // Смотрим, что есть в workspace Jenkins
                    sh 'pwd'
                    sh 'ls -la'
                    sh 'ls -la tests/ || echo "tests/ not found in workspace"'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build --no-cache -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Check Docker Image') {
            steps {
                script {
                    // Проверяем, что находится ВНУТРИ образа
                    sh """
                        docker run --rm \
                        --entrypoint /bin/sh \
                        ${DOCKER_IMAGE} -c 'pwd && ls -la && ls -la tests/ || echo "tests/ not found in image"'
                    """
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Запускаем тесты на файлах ИЗ образа (не из volume)
                    sh """
                        docker run --rm \
                        --entrypoint /bin/sh \
                        ${DOCKER_IMAGE} -c 'cd /app && python3 -m pytest tests/ --junitxml=/app/report.xml -v'
                    """
                    
                    // Копируем report.xml из контейнера в workspace
                    sh """
                        CONTAINER_ID=\$(docker create ${DOCKER_IMAGE})
                        docker cp \$CONTAINER_ID:/app/report.xml ./report.xml || echo "Failed to copy report"
                        docker rm \$CONTAINER_ID
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