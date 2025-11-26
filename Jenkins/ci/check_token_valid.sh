#!/bin/bash
set -e

echo "=== 0. Activate VENV ==="
source /home/ubuntu/naver_api/naverapi_pytest/bin/activate

echo "=== 1. Git Pull for Token Scripts ==="
cd /home/ubuntu/naver_api/API_Test_NAVER
git fetch origin main
git reset --hard origin/main

echo "=== 2. Token Check ==="
RESULT=$(python3 src/utils/check_token.py)

echo "Token Check Result: $RESULT"

if [[ "$RESULT" == *"VALID"* ]]; then
    echo "🟢 Token is VALID"
    exit 0
fi

echo "🔴 Token INVALID → Refresh Start"
python3 src/utils/get_refresh_token.py

echo "=== 3. Load token.json ==="
ACCESS=$(jq -r '.access_token' token.json)
REFRESH=$(jq -r '.refresh_token' token.json)

echo "Access Token Loaded (masked)"
echo "Refresh Token Loaded (masked)"

echo "=== 4. Update Jenkins Credentials ==="

JENKINS_URL="http://3.36.219.242:8080"

curl -X POST \
    -u "$USER:$PASS" \
    -H "Content-Type: application/json" \
    -d "{ \"credentials\":{\"scope\":\"GLOBAL\", \"id\":\"api_access_token\", \"secret\":\"$ACCESS\", \"\\$class\":\"org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl\"} }" \
    "$JENKINS_URL/credentials/store/system/domain/_/credential/api_access_token"

curl -X POST \
    -u "$USER:$PASS" \
    -H "Content-Type: application/json" \
    -d "{ \"credentials\":{\"scope\":\"GLOBAL\", \"id\":\"api_refresh_token\", \"secret\":\"$REFRESH\", \"\\$class\":\"org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl\"} }" \
    "$JENKINS_URL/credentials/store/system/domain/_/credential/api_refresh_token"

echo "🟢 Jenkins Credential Update Completed"
exit 0
