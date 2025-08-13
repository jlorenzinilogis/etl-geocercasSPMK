pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://your-repo-url.git'
            }
        }

        stage('Setup') {
            steps {
                script {
                    // Set up Python environment
                    sh 'python -m venv venv'
                    sh '. venv/bin/activate'
                    sh 'pip install -r requirements.txt'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Run tests
                    sh '. venv/bin/activate && pytest'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Deployment steps
                    sh 'echo "Deploying application..."'
                    // Add your deployment commands here
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh 'rm -rf venv'
        }
    }
}