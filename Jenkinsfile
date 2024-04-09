pipeline {
    agent any
    environment {
        DOCKER_CREDENTIAL_ID = 'docker_credentials'
        DOCKER_HUB_USERNAME = 'kovengers' // 여기에 Docker Hub 사용자 이름을 입력하세요.
        IMAGE_NAME = 'fast-api' // 여기에 사용할 이미지 이름을 입력하세요.
        VERSION = "${env.BUILD_NUMBER}" // Jenkins 빌드 번호를 버전으로 사용합니다.
    }
    stages {
        // stage('Build FastAPI app') {
        //     steps {
        //         sh 'pip install -r requirements.txt' // 필요한 패키지 설치
        //     }
        // }
        stage('Build Docker images') {
            steps {
                script {
                    docker.build("${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${VERSION}") // 이미지 빌드 및 버전 태그
                }
            }
        }
        stage('Push Docker images') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', "${DOCKER_CREDENTIAL_ID}") {
                        docker.image("${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${VERSION}").push() // Docker Hub에 푸시
                    }
                }
            }
        }
    }
}
