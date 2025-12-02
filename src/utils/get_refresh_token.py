"""
Refresh Token을 사용하여 새로운 Access Token 발급 스크립트
"""
import os
import json
import requests
from dotenv import load_dotenv
from dotenv import set_key

# .env 파일 로드
load_dotenv()


def refresh_access_token(refresh_token: str = None):
    """
    Refresh Token을 사용하여 새로운 Access Token 발급

    Args:
        refresh_token (str, optional): Refresh Token (없으면 .env에서 읽음)

    Returns:
        dict: 새로운 토큰 정보
    """
    if not refresh_token:
        refresh_token = os.getenv("REFRESH_TOKEN")

    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")

    if not all([refresh_token, client_id, client_secret]):
        raise ValueError("REFRESH_TOKEN, NAVER_CLIENT_ID, and NAVER_CLIENT_SECRET must be set in .env file")

    url = "https://nid.naver.com/oauth2.0/token"

    params = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }

    response = requests.post(url, params=params)
    response.raise_for_status()

    token_data = response.json()

    # ----------------------------------------------------
    # 1) .env 파일에 Access Token / Refresh Token 저장
    # ----------------------------------------------------
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    env_path = os.path.join(base_dir, ".env")

    if "access_token" in token_data:
        set_key(env_path, "ACCESS_TOKEN", token_data["access_token"], quote_mode="never")
        print("✓ New ACCESS_TOKEN saved to .env")

    if "refresh_token" in token_data:
        set_key(env_path, "REFRESH_TOKEN", token_data["refresh_token"], quote_mode="never")
        print("✓ New REFRESH_TOKEN saved to .env")

    # ----------------------------------------------------
    # 2) token.json 파일로도 저장 (Jenkins에서 읽기 위함)
    # ----------------------------------------------------
    json_path = os.path.join(base_dir, "token.json")

    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(
            {
                "access_token": token_data.get("access_token"),
                "refresh_token": token_data.get("refresh_token")
            },
            jf,
            ensure_ascii=False,
            indent=4
        )

    print(f"✓ token.json created at: {json_path}")

    return token_data


if __name__ == "__main__":
    token_data = refresh_access_token()

    print("\n✓ Successfully refreshed access token!")
    print(f"New Access Token (first 20 chars): {token_data.get('access_token', 'N/A')[:20]}...")
