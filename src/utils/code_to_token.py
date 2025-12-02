"""
Authorization Code를 Access Token과 Refresh Token으로 변환하는 스크립트
"""
import os
import requests
from dotenv import load_dotenv
from dotenv import set_key

# .env 파일 로드
load_dotenv()


def get_token_from_code(code: str):
    """
    Authorization Code를 사용하여 Access Token과 Refresh Token 발급

    Args:
        code (str): Authorization Code

    Returns:
        dict: 토큰 정보 (access_token, refresh_token 등)
    """
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")
    redirect_uri = os.getenv("NAVER_REDIRECT_URI")

    if not all([client_id, client_secret, redirect_uri]):
        raise ValueError("NAVER_CLIENT_ID, NAVER_CLIENT_SECRET, and NAVER_REDIRECT_URI must be set in .env file")

    url = "https://nid.naver.com/oauth2.0/token"

    params = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "code": code,
        "state": "RANDOM_STATE"
    }

    response = requests.post(url, params=params)
    response.raise_for_status()

    token_data = response.json()

    # .env 파일에 토큰 저장
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    env_path = os.path.join(base_dir, ".env")

    if "access_token" in token_data:
        set_key(env_path, "ACCESS_TOKEN", token_data["access_token"], quote_mode="never")
        print("✓ ACCESS_TOKEN saved to .env")

    if "refresh_token" in token_data:
        set_key(env_path, "REFRESH_TOKEN", token_data["refresh_token"], quote_mode="never")
        print("✓ REFRESH_TOKEN saved to .env")

    return token_data


if __name__ == "__main__":
    # .env에서 CODE 읽기
    code = os.getenv("CODE")

    if not code:
        # 직접 입력받기
        code = input("Enter the authorization code: ").strip()
        if not code:
            print("Error: Code is required")
            exit(1)

        # 입력받은 CODE를 .env에 저장 (따옴표 없이)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        env_path = os.path.join(base_dir, ".env")
        set_key(env_path, "CODE", code, quote_mode="never")
        print("✓ CODE saved to .env")

    token_data = get_token_from_code(code)
    print("\n✓ Successfully obtained tokens!")
    print(f"Access Token: {token_data.get('access_token', 'N/A')[:20]}...")
    print(f"Refresh Token: {token_data.get('refresh_token', 'N/A')[:20]}...")
