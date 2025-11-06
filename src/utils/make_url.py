"""
Naver API 인증 URL 생성 스크립트
"""
import os
from dotenv import load_dotenv
from urllib.parse import urlencode

# .env 파일 로드
load_dotenv()

def make_authorize_url():
    """
    Naver API 인증 URL 생성
    
    Returns:
        str: 인증 URL
    """
    client_id = os.getenv("NAVER_CLIENT_ID")
    redirect_uri = os.getenv("NAVER_REDIRECT_URI")
    state = "RANDOM_STATE"  # CSRF 방지를 위한 상태값
    
    if not client_id or not redirect_uri:
        raise ValueError("NAVER_CLIENT_ID and NAVER_REDIRECT_URI must be set in .env file")
    
    base_url = "https://nid.naver.com/oauth2.0/authorize"
    
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "state": state
    }
    
    authorize_url = f"{base_url}?{urlencode(params)}"
    
    print(f"Generated Authorization URL:")
    print(authorize_url)
    print("\nPlease visit this URL and authorize the application.")
    print("After authorization, you will be redirected with a code parameter.")
    
    return authorize_url


if __name__ == "__main__":
    url = make_authorize_url()
    
    # .env 파일에 저장 (선택사항)
    save_to_env = input("\nDo you want to save this URL to .env file? (y/n): ")
    if save_to_env.lower() == 'y':
        from dotenv import set_key
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
        set_key(env_path, "AUTHORIZE_URL", url, quote_mode="never")
        print("URL saved to .env file as AUTHORIZE_URL")

