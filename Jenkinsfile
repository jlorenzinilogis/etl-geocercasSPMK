pipeline {
    agent any

    stages {
        stage('Preparar entorno') {
            steps {
                dir('src') {
                    // Instala dependencias si tienes requirements.txt
                    script {
                        if (fileExists('../requirements.txt')) {
                            sh 'pip install -r ../requirements.txt'
                        } else {
                            sh 'pip install pandas sqlalchemy requests openpyxl'
                        }
                    }
                }
            }
        }
        stage('Ejecutar ETL') {
            steps {
                dir('src') {
                    sh 'python main.py'
                }
            }
        }
    }
    post {
        always {
            echo 'Pipeline finalizado.'
        }
    }
}