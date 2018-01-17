/** Desired capabilities */
def capabilities = [
  browserName: 'Chrome',
  platform: 'Windows 10'
]

pipeline {
  agent {
    dockerfile true
  }
  libraries {
    lib('fxtest@1.10')
  }
  options {
    ansiColor('xterm')
    timestamps()
    timeout(time: 30, unit: 'MINUTES')
  }
  environment {
    PYTEST_PROCESSES = "${PYTEST_PROCESSES ?: "auto"}"
    PYTEST_ADDOPTS =
      "-n=${PYTEST_PROCESSES} " +
      "--tb=short " +
      "--color=yes " +
      "--driver=SauceLabs " +
      "--variables=capabilities.json"
    PULSE = credentials('PULSE')
    SAUCELABS = credentials('SAUCELABS')
  }
  stages {
    stage('Lint') {
      steps {
        sh "flake8"
      }
    }
    stage('Test') {
      steps {
        writeCapabilities(capabilities, 'capabilities.json')
        sh "pytest --junit-xml=results/junit.xml " +
          "--html=results/index.html --self-contained-html " +
          "--log-raw=results/raw.txt " +
          "--log-tbpl=results/tbpl.txt"
      }
      post {
        always {
          stash includes: 'results/*', name: 'results'
          archiveArtifacts 'results/*'
          junit 'results/*.xml'
          submitToActiveData('results/raw.txt')
          submitToTreeherder('stubattribution-tests', 'e2e', 'End-to-end integration tests', 'results/*', 'results/tbpl.txt')
        }
      }
    }
  }
  post {
    always
      unstash 'results'
      publishHTML(target: [
        allowMissing: false,
        alwaysLinkToLastBuild: true,
        keepAll: true,
        reportDir: 'results',
        reportFiles: "index.html",
        reportName: 'HTML Report'])
    }
    changed {
      ircNotification()
    }
    failure {
      emailext(
        attachLog: true,
        attachmentsPattern: 'results/index.html',
        body: '$BUILD_URL\n\n$FAILED_TESTS',
        replyTo: '$DEFAULT_REPLYTO',
        subject: '$DEFAULT_SUBJECT',
        to: '$DEFAULT_RECIPIENTS')
    }
  }
}
