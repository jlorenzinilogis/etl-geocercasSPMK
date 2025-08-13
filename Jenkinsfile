pipeline {
    agent any

    stages {
        stage('Preparar entorno') {
            steps {
                dir('src') {
                    script {
                        // Crea entorno virtual si no existe
                        sh '''
                        python3 -m venv ../venv
                        . ../venv/bin/activate
                        pip install --upgrade pip
                        pip install -r ../requirements.txt
                        '''
                    }
                }
            }
        }
        stage('Ejecutar ETL') {
            steps {
                dir('src') {
                    sh '''
                    . ../venv/bin/activate
                    python main.py
                    '''
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