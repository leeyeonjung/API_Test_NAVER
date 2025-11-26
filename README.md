# Naver API Test

Naver API를 테스트하기 위한 pytest 기반 테스트 프로젝트입니다.

## 📁 프로젝트 구조

```
API_Test_Naver/
├── conftest.py                    # pytest 설정 및 fixture 정의
├── requirements.txt               # Python 패키지 의존성
├── .env                           # 환경 변수 파일 (민감 정보, Git 제외)
├── .env.example                   # 환경 변수 예시 파일
├── token.json                     # 토큰 저장 파일 (민감 정보, Git 제외)
├── token.json.example             # 토큰 파일 예시
├── .gitignore                     # Git 제외 파일 목록
│
├── src/
│   ├── services/
│   │   └── api_clients.py         # Naver API 클라이언트
│   └── utils/
│       ├── make_url.py            # 인증 URL 생성 스크립트
│       ├── code_to_token.py       # Code → Token 변환 스크립트
│       ├── get_refresh_token.py   # Refresh Token으로 새 Token 발급 스크립트
│       └── check_token.py         # Access Token 유효성 검사 스크립트
│
├── testcase/
│   └── test_api.py                # 테스트 케이스 (pytest)
│
├── Jenkins/                       # Jenkins CI/CD 파이프라인
│   ├── Jenkinsfile                # Jenkins 파이프라인 정의
│   └── ci/
│       ├── check_token_valid.sh   # Linux 토큰 검증 및 갱신 스크립트
│       ├── linux_run.sh           # Linux 테스트 실행 스크립트
│       └── windows_run.bat        # Windows 테스트 실행 스크립트
│
└── Result/                        # 테스트 리포트 저장 폴더 (자동 생성)
    └── test_report_*.html         # HTML 테스트 리포트
```

## 🚀 설치 방법

### 1. Python 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env.example` 파일을 참고하여 `.env` 파일을 생성하고 다음 값들을 입력하세요:

```env
# Naver API Configuration
NAVER_CLIENT_ID=your_client_id_here
NAVER_CLIENT_SECRET=your_client_secret_here
NAVER_REDIRECT_URI=your_redirect_uri_here

# Authorization URL (자동 생성됨)
AUTHORIZE_URL=

# Authentication Code and Tokens (자동 생성됨)
CODE=
ACCESS_TOKEN=
REFRESH_TOKEN=
```

**주의사항:**
- Naver Developer Console(https://developers.naver.com/apps/#/register)에서 발급받은 실제 값들을 입력해야 합니다.
- 값 입력 시 따옴표(`"`)를 사용하지 마세요. 예: `NAVER_CLIENT_ID=abc123` (올바름), `NAVER_CLIENT_ID="abc123"` (잘못됨)
- 모든 민감 정보는 `.env` 파일에 저장되며, Git에 커밋되지 않습니다.

### 3. 토큰 파일 설정 (선택사항)

Jenkins CI/CD를 사용하는 경우, `token.json.example` 파일을 참고하여 `token.json` 파일을 생성할 수 있습니다:

```json
{
    "access_token": "YOUR_ACCESS_TOKEN_HERE",
    "refresh_token": "YOUR_REFRESH_TOKEN_HERE"
}
```

**주의사항:**
- `token.json` 파일은 Git에 커밋되지 않습니다 (`.gitignore`에 포함).
- `get_refresh_token.py` 실행 시 자동으로 생성되므로 수동 생성은 선택사항입니다.

## 📖 사용 방법

### 1. 인증 URL 생성

```bash
python src/utils/make_url.py
```

이 명령어를 실행하면:
- Naver API 인증 URL이 생성되고 출력됩니다
- 생성된 URL을 브라우저에서 열어 인증을 진행하세요
- 인증 후 리다이렉트 URL에서 `code` 파라미터를 복사합니다
- 선택적으로 `.env` 파일에 `AUTHORIZE_URL`로 저장할 수 있습니다

### 2. Code로 Token 발급

생성된 인증 URL로 인증 후 받은 `code` 값을 사용하여 Access Token과 Refresh Token을 발급받습니다:

```bash
python src/utils/code_to_token.py
```

실행 시:
- `.env` 파일에 `CODE`가 있으면 자동으로 사용
- 없으면 직접 입력받습니다
- 입력받은 CODE는 `.env` 파일에 자동 저장됩니다
- 토큰 발급 후 `ACCESS_TOKEN`과 `REFRESH_TOKEN`이 `.env` 파일에 자동 저장됩니다

### 3. Refresh Token으로 새 Token 발급

Access Token이 만료되었을 때 Refresh Token을 사용하여 새 Access Token을 발급받습니다:

```bash
python src/utils/get_refresh_token.py
```

실행 시:
- `.env` 파일의 `REFRESH_TOKEN`을 사용하여 새 토큰 발급
- 새 `ACCESS_TOKEN`이 `.env` 파일에 자동 저장됩니다
- Refresh Token도 갱신된 경우 새 값으로 저장됩니다
- Jenkins에서 사용하기 위해 `token.json` 파일도 자동 생성됩니다

### 4. Access Token 유효성 검사

Access Token이 유효한지 확인합니다:

```bash
python src/utils/check_token.py
```

실행 시:
- Jenkins Credential (`NAVER_ACCESS_TOKEN`) 또는 `.env` 파일의 `ACCESS_TOKEN`을 사용
- 유효한 토큰이면 `VALID`, 만료되었거나 잘못된 토큰이면 `INVALID` 출력
- Jenkins 파이프라인에서 자동으로 토큰 만료 여부를 확인하는 용도로 사용됩니다

### 5. 테스트 실행

#### 모든 테스트 실행

```bash
pytest testcase/test_api.py
```

#### HTML 리포트 생성

테스트 실행 후 `Result/` 폴더에 HTML 리포트가 자동으로 생성됩니다.

## 🧪 테스트 케이스

모든 테스트는 함수 기반으로 작성되었으며, `pytest-check`를 사용하여 다중 검증을 지원합니다.

### test_get_user_profile
- 사용자 프로필 조회 API 테스트
- 프로필 응답 구조 검증
- resultcode가 "00"인지 확인
- 사용자 정보(id 또는 email) 존재 확인

### test_access_token_validity
- Access Token 유효성 검증
- Token이 None이 아니고, 빈 값이 아니며, 문자열인지 확인

### test_api_client_initialization
- API 클라이언트 초기화 테스트
- Access Token이 올바르게 설정되었는지 확인

### test_api_endpoints
- API 엔드포인트 테스트
- 응답이 올바른 형태(dict)인지 확인

## 🔧 주요 기능

### NaverAPIClient
- Naver API 호출을 위한 클라이언트 클래스
- Access Token을 사용하여 API 요청
- 사용자 프로필 조회 (`get_user_profile()`)
- 일반 API 호출 (`call_api()`)

### 자동 토큰 관리
- `conftest.py`의 `access_token` fixture가 자동으로 토큰 관리
- 우선순위: CLI 인자 (`--access-token`) > .env 파일 (`ACCESS_TOKEN`) > Refresh Token 자동 갱신
- Access Token이 없으면 자동으로 Refresh Token으로 새 토큰 발급 시도

### pytest-check 사용
- 모든 테스트에서 `pytest-check`의 `check` 메서드 사용
- 여러 검증 실패 시에도 테스트를 계속 진행하여 모든 실패를 한 번에 확인 가능
- `check.equal()`, `check.is_not_none()`, `check.is_instance()` 등 사용

## 🚀 Jenkins CI/CD

프로젝트는 Jenkins를 통한 자동화된 CI/CD 파이프라인을 지원합니다.

### 파이프라인 구조

1. **Check Token & Refresh** (Linux Agent)
   - Access Token 유효성 검사
   - 만료된 경우 자동으로 Refresh Token으로 갱신
   - Jenkins Credentials 자동 업데이트

2. **Windows API Test** (Windows Agent)
   - Windows 환경에서 API 테스트 실행
   - 테스트 리포트 자동 아카이빙 (`windows_test_report_*.html`)

3. **Linux API Test** (Linux Agent)
   - Linux 환경에서 API 테스트 실행
   - 테스트 리포트 자동 아카이빙 (`linux_test_report_*.html`)

### Jenkins 설정 요구사항

- **Credentials:**
  - `api_access_token`: Naver Access Token
  - `api_refresh_token`: Naver Refresh Token
  - `jenkins-admin`: Jenkins 관리자 계정 (Credential 업데이트용)

## 📝 환경 변수 설명

| 변수명 | 설명 | 필수 | 자동 생성 | 비고 |
|--------|------|------|----------|------|
| `NAVER_CLIENT_ID` | Naver API Client ID | ✅ | ❌ | Naver Developer Console에서 발급 |
| `NAVER_CLIENT_SECRET` | Naver API Client Secret | ✅ | ❌ | Naver Developer Console에서 발급 |
| `NAVER_REDIRECT_URI` | 리다이렉트 URI | ✅ | ❌ | Naver Developer Console에 등록된 URI |
| `AUTHORIZE_URL` | 인증 URL | ❌ | ✅ | `make_url.py` 실행 시 저장 |
| `CODE` | Authorization Code | ❌ | ✅ | 인증 후 받은 값, `code_to_token.py` 실행 시 저장 |
| `ACCESS_TOKEN` | Access Token | ❌ | ✅ | `code_to_token.py` 또는 `get_refresh_token.py` 실행 시 저장 |
| `REFRESH_TOKEN` | Refresh Token | ❌ | ✅ | `code_to_token.py` 실행 시 저장 |

## 🔐 보안 주의사항

- `.env` 파일은 Git에 포함되지 않습니다 (`.gitignore`에 포함)
- `.env.example` 파일은 Git에 포함되어 예시로 사용됩니다
- `token.json` 파일은 Git에 포함되지 않습니다 (`.gitignore`에 포함)
- `token.json.example` 파일은 Git에 포함되어 예시로 사용됩니다
- 실제 값들은 절대 Git에 커밋하지 마세요
- 환경 변수 값 입력 시 따옴표를 사용하지 마세요

## 📦 의존성 패키지

설치:
```bash
pip install -r requirements.txt
```