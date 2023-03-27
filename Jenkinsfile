#!groovy
import org.jenkinsci.plugins.workflow.libs.Library

@Library(['jenkins-global-libraries', 'jenkins-build-config']) _

String applicationName = "manchester-transport-dashboard"
String applicationVersion = "0.1.${env.BUILD_NUMBER}"
pipeline {
    agent { label 'linux' }
    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 10, unit: 'MINUTES')
        timestamps()
    }
    environment {
        kubectl = tool name: 'kubectl'
        helm = tool name: 'helm'
    }
    stages{
        stage('Build Docker Image') {
            steps {
                sh "chmod +x ./build.sh"
                sh "./build.sh $applicationVersion"
            }
        }
        stage('Checkout Helm Chart') {
            steps {
                dir('chart') {
                    sparseCheckout(
                        gitRepoUrl: 'https://git.services.aquilaheywood.co.uk/scm/helm/streamlit-development.git',
                        branch: "master"
                    )
                }
            }
        }

        stage('Deploy Container') {
            steps {
                dir('chart') {
                        sh "${helm}/helm --kube-context cluster02 upgrade ${applicationName} . --install --set image.tag=${applicationVersion} --values values.yaml --set ingress.hosts[0].host=${applicationName}.services.aquilaheywood.co.uk --set ingress.tls[0].hosts[0]=${applicationName}.services.aquilaheywood.co.uk --set image.repository=nexus-altdev.services.aquilaheywood.co.uk/${applicationName}"
                }
            }
        }
        stage('Verify Deployment') {
            options {
                timeout(time: 120, unit: 'SECONDS')
            }
            steps {
                sh "${kubectl}/bin/kubectl --context cluster02 rollout status deployment ${applicationName}-streamlit"
                echo 'Development Statistics deployment was successful!'
            }
        }
    }
}