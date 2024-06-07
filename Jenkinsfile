pipeline {
    agent any
    environment {
        DOCKER_CREDENTIAL_ID = 'docker_credentials'
        DOCKER_HUB_USERNAME = 'kovengers' // 여기에 Docker Hub 사용자 이름을 입력하세요.
        IMAGE_NAME = 'fast-api' // 여기에 사용할 이미지 이름을 입력하세요.
        VERSION = "${env.BUILD_NUMBER}" // Jenkins 빌드 번호를 버전으로 사용합니다.
    }
    stages {
        stage('Pull Git Submodules') {
            steps {
                sh 'git submodule update --init --recursive'
            }
        }
        stage('Build Docker images') {
            steps {
                script {
                    docker.build("${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${VERSION}") // 이미지 빌드 및 버전 태그
                    docker.build("${DOCKER_HUB_USERNAME}/${IMAGE_NAME}", "-t ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:latest -t ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${VERSION} .")
                }
            }
        }
        stage('Push Docker images') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', "${DOCKER_CREDENTIAL_ID}") {
                        // 'latest' 태그 푸시
                        docker.image("${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:latest").push()
                        // 버전 태그 푸시
                        docker.image("${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${VERSION}").push()
                        
                        echo "Push ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${VERSION}"
                    }
                }
            }
        }
        stage('Docker image cleanup') {
            steps {
                script {
                    sh 'docker rmi ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${VERSION}'
                    sh 'docker rmi registry.hub.docker.com/${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${VERSION}'
                }
            }
        }
        stage('Update Kubernetes YAML') {
            steps {
                script {
                    dir('Submodules'){
                        sshagent(['k8s_git']) {
                            sh 'mkdir -p ~/.ssh'
                            sh 'if [ ! -f ~/.ssh/known_hosts ]; then ssh-keyscan github.com >> ~/.ssh/known_hosts; fi'
                            sh 'rm -rf kubernetes-yaml' // Add this line
                            sh 'git clone git@github.com:KEA-Kovengers/kubernetes-yaml.git'
                        }
                        dir('kubernetes-yaml') {
                            dir('backend/fastapi-service'){
                                sh "sed -i 's|${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:.*|${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${VERSION}|' fastapi-service.yaml"
                                sh 'git add fastapi-service.yaml'
                            }
                            
                            sh 'git config user.email "keakovengers@gmail.com"'
                            sh 'git config user.name "kovengers"'
                            sh 'git add -A'
                            sh 'git status'
                            sh 'git diff --cached --exit-code || git commit -m "Update service image tag"'
                            sshagent(['k8s_git']) {
                                sh 'git push origin kakao-cloud'
                            }
                        }
                    }
                }
            }
        }
    }
}
