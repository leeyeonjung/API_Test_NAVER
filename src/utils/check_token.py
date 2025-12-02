"""
check_token.py
NAVER Access Token 유효성 검사 스크립트
Jenkins에서 토큰 만료 여부를 확인하는 용도로 사용됨.
"""

import os
import requests
from dotenv import load_dotenv

# .env 로드 (로컬 환경용)
load_dotenv()


def is_token_valid(access_token: str) -> bool:
    """
    Access Token 유효성 검사

    Returns:
        True  → 유효한 토큰
        False → 만료 or 잘못된 토큰
    """
    if not access_token:
        return False

    url = "https://openapi.naver.com/v1/nid/me"
    headers = {"Authorization": f"Bearer {access_token}"}

    res = requests.get(url, headers=headers, timeout=5)
    return res.status_code == 200


if __name__ == "__main__":
    # 1순위: Jenkins Credential (NAVER_ACCESS_TOKEN)
    # 2순위: 로컬 .env (ACCESS_TOKEN)
    access_token = os.getenv("NAVER_ACCESS_TOKEN") or os.getenv("ACCESS_TOKEN")

    if is_token_valid(access_token):
        print("VALID")
    else:
        print("INVALID")
