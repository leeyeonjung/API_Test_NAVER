pipeline {
    agent { label 'web_windows' }

    environment {
        NAVER_ACCESS_TOKEN  = credentials('api_access_token')
        NAVER_REFRESH_TOKEN = credentials('api_refresh_token')
    }

    stages {

        /* -------------------------------------------------
         * 1. Token Validity Check
         * ------------------------------------------------- */
        stage('Check Token Validity') {
            steps {
                script {
                    def result = bat(
                        script: '''
                            cd C:\\Automation\\API_Test_Naver
                            python src\\utils\\check_token.py
                        ''',
                        returnStdout: true
                    ).trim()

                    if (result.contains("VALID")) {
                        echo "🟢 Access Token is VALID"
                        env.TOKEN_EXPIRED = "false"
                    } else {
                        echo "🔴 Access Token is INVALID → Refresh required"
                        env.TOKEN_EXPIRED = "true"
                    }
                }
            }
        }

        /* -------------------------------------------------
         * 2. Token Refresh (when invalid)
         * ------------------------------------------------- */
        stage('Refresh Token') {
            when {
                expression { env.TOKEN_EXPIRED == "true" }
            }
            steps {
                echo "🔄 Refreshing token..."

                bat '''
                    cd C:\\Automation\\API_Test_Naver
                    python src\\utils\\get_refresh_token.py
                '''

                script {
                    // token.json 읽기
                    def jsonPath = "C:\\Automation\\API_Test_Naver\\token.json"
                    def json = readJSON file: jsonPath

                    def newAccess  = json.access_token
                    def newRefresh = json.refresh_token

                    echo "🟢 New tokens loaded from token.json"

                    /* -----------------------------------------
                     * 2-A. Update Jenkins Credentials
                     * ----------------------------------------- */
                    withCredentials([usernamePassword(
                        credentialsId: 'jenkins-admin',
                        usernameVariable: 'USER',
                        passwordVariable: 'PASS'
                    )]) {

                        bat """
                            curl -X POST ^
                                -u %USER%:%PASS% ^
                                -H "Content-Type: application/json" ^
                                -d "{ \\"credentials\\":{\\"scope\\":\\"GLOBAL\\", \\"id\\":\\"api_access_token\\", \\"secret\\":\\"${newAccess}\\", \\"$class\\":\\"org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl\\"} }" ^
                                http://3.36.219.242:8080/credentials/store/system/domain/_/credential/api_access_token

                            curl -X POST ^
                                -u %USER%:%PASS% ^
                                -H "Content-Type: application/json" ^
                                -d "{ \\"credentials\\":{\\"scope\\":\\"GLOBAL\\", \\"id\\":\\"api_refresh_token\\", \\"secret\\":\\"${newRefresh}\\", \\"$class\\":\\"org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl\\"} }" ^
                                http://3.36.219.242:8080/credentials/store/system/domain/_/credential/api_refresh_token
                        """
                    }

                    echo "🟢 Jenkins Credentials updated ✔"
                }
            }
        }

        /* -------------------------------------------------
         * 3. Run API Test
         * ------------------------------------------------- */
        stage('Run API Test') {
            steps {
                echo "🚀 Running pytest..."

                bat '''
                    cd C:\\Automation\\API_Test_Naver
                    pytest -v --disable-warnings
                '''
            }
        }
    }

    /* -------------------------------------------------
     * 4. Always copy latest HTML report
     * ------------------------------------------------- */
    post {
        always {
            echo "📄 Copy latest HTML report..."

            bat '''
                set "REPORT_DIR=C:\\Automation\\API_Test_Naver\\Result"

                for /f "delims=" %%i in ('dir "%REPORT_DIR%\\test_report_*.html" /b /o:-d') do (
                    set "LATEST_REPORT=%%i"
                    goto COPY_FILE
                )

                :COPY_FILE
                copy "%REPORT_DIR%\\%LATEST_REPORT%" "windows_%LATEST_REPORT%"
            '''

            archiveArtifacts artifacts: "windows_test_report_*.html", fingerprint: true
        }
    }
}
