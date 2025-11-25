pipeline {
    agent { label 'web_windows' }

    environment {
        NAVER_ACCESS_TOKEN  = credentials('api_access_token')
        NAVER_REFRESH_TOKEN = credentials('api_refresh_token')
    }

    stages {
        stage('Setup Python Env') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run API Test') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    pytest -v --disable-warnings --html=C:\\Automation\\API_Test_Naver\\Result\\test_report_%DATE:~0,4%%DATE:~5,2%%DATE:~8,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%.html --self-contained-html
                '''
            }
        }
    }

    post {
        always {
            echo "📄 최신 HTML 리포트 찾는 중..."

            // 최신 파일 찾기 + 복사 (윈도우 CMD 방식)
            bat '''
                set "REPORT_DIR=C:\\Automation\\API_Test_Naver\\Result"

                REM 최신 HTML 리포트 파일 찾기
                for /f "delims=" %%i in ('dir "%REPORT_DIR%\\test_report_*.html" /b /o:-d') do (
                    set "LATEST_REPORT=%%i"
                    goto COPY_FILE
                )

                :COPY_FILE
                echo 최신 파일: %LATEST_REPORT%

                REM Prefix 붙여서 workspace로 복사
                copy "%REPORT_DIR%\\%LATEST_REPORT%" "windows_%LATEST_REPORT%"
            '''

            // Jenkins 아티팩트로 저장
            archiveArtifacts artifacts: "windows_test_report_*.html", fingerprint: true
        }
    }
}
