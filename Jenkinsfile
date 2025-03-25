pipeline {
    agent any // need to be kubernetes agent

    environment {
        // Define your virtual environment and Python version
        VENV = 'venv'
        PYTHON_VERSION = 'python3.8'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the repository
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    // Set up a virtual environment
                    sh 'python3 -m venv $VENV'
                    sh '. $VENV/bin/activate'
                    sh 'pip install --upgrade pip'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Install project dependencies
                    sh '. $VENV/bin/activate && pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run tests, replace 'pytest' with the test tool you're using
                    sh '. $VENV/bin/activate && pytest'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Deploy to your environment (this is an example using Heroku)
                    sh '. $VENV/bin/activate && git push heroku main'
                }
            }
        }
    }

    post {
        always {
            // Clean up (delete the virtual environment)
            sh 'rm -rf $VENV'
        }
        success {
            // Notify success (you could integrate email notifications or Slack messages)
            echo "Build and deploy succeeded!"
        }
        failure {
            // Notify failure
            echo "Build failed. Please check the logs."
        }
    }
}