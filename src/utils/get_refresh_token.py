"""
Refresh Token을 사용하여 새로운 Access Token 발급 스크립트
"""
import os
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
    
    # .env 파일에 새로운 Access Token 저장
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    env_path = os.path.join(base_dir, ".env")
    
    if "access_token" in token_data:
        set_key(env_path, "ACCESS_TOKEN", token_data["access_token"], quote_mode="never")
        print(f"✓ New ACCESS_TOKEN saved to .env")
    
    # Refresh Token도 갱신되었을 수 있음
    if "refresh_token" in token_data:
        set_key(env_path, "REFRESH_TOKEN", token_data["refresh_token"], quote_mode="never")
        print(f"✓ New REFRESH_TOKEN saved to .env")
    
    return token_data


if __name__ == "__main__":
    token_data = refresh_access_token()
    print("\n✓ Successfully refreshed access token!")
    print(f"New Access Token: {token_data.get('access_token', 'N/A')[:20]}...")