"""
Naver API 클라이언트
"""
import os
import requests
from typing import Dict, Optional
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


class NaverAPIClient:
    """Naver API 클라이언트"""

    BASE_URL = "https://openapi.naver.com"

    def __init__(self, access_token: Optional[str] = None):
        """
        Naver API 클라이언트 초기화

        Args:
            access_token (str, optional): Access Token (없으면 .env에서 읽음)
        """
        self.access_token = access_token or os.getenv("ACCESS_TOKEN")
        if not self.access_token:
            raise ValueError("ACCESS_TOKEN must be provided or set in .env file")

    def _get_headers(self) -> Dict[str, str]:
        """API 요청 헤더 생성"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def get_user_profile(self) -> Dict:
        """
        사용자 프로필 조회

        Returns:
            dict: 사용자 프로필 정보
        """
        url = f"{self.BASE_URL}/v1/nid/me"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def call_api(self, endpoint: str, method: str = "GET", **kwargs) -> Dict:
        """
        일반 API 호출 메서드

        Args:
            endpoint (str): API 엔드포인트
            method (str): HTTP 메서드 (GET, POST, PUT, DELETE)
            **kwargs: requests 라이브러리의 추가 파라미터

        Returns:
            dict: API 응답
        """
        url = f"{self.BASE_URL}{endpoint}"
        headers = self._get_headers()

        if "headers" in kwargs:
            headers.update(kwargs.pop("headers"))

        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()

