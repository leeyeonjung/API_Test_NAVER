pipeline {
    agent { label 'web_windows' }

    environment {
        NAVER_ACCESS_TOKEN  = credentials('api_access_token')
        NAVER_REFRESH_TOKEN = credentials('api_refresh_token')
    }

    stages {
        stage('Run Windows API Test') {
            steps {
                bat '''
                    cd C:\\Automation\\API_Test_Naver
                    pytest -v --disable-warnings
                '''
            }
        }
    }

    post {
        always {
            echo "📄 최신 HTML 리포트 찾고 복사합니다..."

            bat '''
                set "REPORT_DIR=C:\\Automation\\API_Test_Naver\\Result"

                REM 최신 HTML 리포트 찾기 (최신순 정렬)
                for /f "delims=" %%i in ('dir "%REPORT_DIR%\\test_report_*.html" /b /o:-d') do (
                    set "LATEST_REPORT=%%i"
                    goto COPY_FILE
                )

                :COPY_FILE
                echo 최신 파일 찾음: %LATEST_REPORT%

                REM Jenkins workspace에 windows_ prefix 붙여서 복사
                copy "%REPORT_DIR%\\%LATEST_REPORT%" "windows_%LATEST_REPORT%"
            '''

            // Jenkins artifact 저장
            archiveArtifacts artifacts: "windows_test_report_*.html", fingerprint: true
        }
    }
}
