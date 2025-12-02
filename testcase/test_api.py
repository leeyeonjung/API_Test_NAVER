"""
Naver API 테스트 케이스
"""
import logging
from pytest_check import check
from src.services.api_clients import NaverAPIClient

# Logger setting
log = logging.getLogger(__name__)


def test_get_user_profile(access_token):
    """사용자 프로필 조회 테스트"""
    client = NaverAPIClient(access_token=access_token)
    profile = client.get_user_profile()
    log.info(f"Profile response: {profile}")

    # 응답 검증
    check.is_in("resultcode", profile)
    check.is_in("message", profile)

    # resultcode가 "00"이면 성공
    check.equal(profile["resultcode"], "00", msg=f"API call failed: {profile.get('message')}")

    # 사용자 정보 확인
    check.is_in("response", profile)
    user_info = profile["response"]
    check.is_true("id" in user_info or "email" in user_info, msg="User info not found")


def test_access_token_validity(access_token):
    """Access Token 유효성 검증 테스트"""
    log.info(f"Access token: {access_token[:20]}..." if access_token else "Access token: None")
    check.is_not_none(access_token, msg="Access token is None")
    check.greater(len(access_token), 0, msg="Access token is empty")
    check.is_instance(access_token, str, msg="Access token must be a string")


def test_api_client_initialization(access_token):
    """API 클라이언트 초기화 테스트"""
    client = NaverAPIClient(access_token=access_token)
    log.info(f"Client initialized with access token: {client.access_token[:20]}..." if client.access_token else "Client initialized with access token: None")
    check.equal(client.access_token, access_token)
    check.is_not_none(client.access_token)


def test_api_endpoints(access_token):
    """API 엔드포인트 테스트"""
    client = NaverAPIClient(access_token=access_token)
    endpoint = "/v1/nid/me"
    response = client.call_api(endpoint)
    log.info(f"API endpoint response ({endpoint}): {response}")
    check.is_not_none(response)
    check.is_instance(response, dict)
