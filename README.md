# ETF 브리핑 · 투자 Study 대시보드

GitHub Pages용 정적 HTML + GitHub Actions 예약 업데이트 프로젝트입니다.

## 설치 (GitHub)
1. GitHub에서 **Public** 저장소 `etf-study-dashboard`를 생성합니다. 공개 저장소에 개인 계좌정보, 보유수량, API 키를 넣지 마세요.
2. ZIP 압축을 해제한 **내용물 전체**를 저장소 최상위에 업로드합니다 (`.github/workflows/update.yml` 포함). 숨김 폴더 `.github`가 누락되지 않도록 확인하세요.
3. **Settings → Pages → Build and deployment → Deploy from a branch → main / (root) → Save**.
4. 몇 분 후 `https://<GitHub아이디>.github.io/etf-study-dashboard/`에서 접속합니다.
5. **Actions → Update ETF dashboard → Run workflow**를 눌러 첫 실행을 시험합니다.
6. 이후 월·수·금 한국시간 11:00(UTC 02:00)에 예약 실행을 시도합니다. GitHub 예약 실행은 지연·누락될 수 있습니다.

## 기능과 제약
- `index.html`: 날짜별 브리핑/검색/Study/추적 ETF/기기별 개인 메모.
- `briefings.json`: 날짜별 브리핑 데이터. Actions가 같은 날짜 기록을 갱신하고 과거 날짜는 보존합니다.
- `scripts/update.py`: Yahoo Finance **비공식** 일별 차트 API로 가격을 수집하고 Google News RSS 헤드라인을 수집합니다. 차단·지연·휴장·시차로 실패할 수 있으며 실패 시 `null`/미확인으로 남깁니다.
- **현재 자동화는 검증된 뉴스 해설을 생성하지 않습니다.** 뉴스 제목은 참고자료일 뿐 인과관계 분석이 아닙니다. 기존 ChatGPT 예약 브리핑과 자동 연동되지 않습니다.
- 한국 ETF 일부 종목은 정확한 거래소 코드를 검증하지 못하여 `WATCH`의 symbol이 빈 값입니다. 해당 종목은 가격을 표시하지 않습니다. 코드가 있는 ETF도 실제 상품과 매칭을 공식 자료로 재검증해야 합니다.
- GitHub Pages는 공개 사이트입니다. 개인 메모는 현재 사용 브라우저의 localStorage에만 저장되며 기기간 동기화되지 않습니다.
- 새 데이터는 `briefings.json`이 웹에 배포된 뒤 새로고침하면 반영됩니다. 브라우저 캐시를 우회하기 위해 `cache: no-store`를 사용합니다.
- **무료 서비스라고 해서 가격·뉴스 데이터의 완전성, GitHub 예약 정확성, 무중단 운영이 보장되는 것은 아닙니다.**

## 중복 예약 관리
기존 ChatGPT의 월·수·금 예약은 **이 코드에서 변경하지 않았습니다**. 웹사이트 갱신은 별도 GitHub Actions 예약입니다. 중복 알림을 원치 않으면 ChatGPT 예약을 사용자 확인 후 비활성화하세요.

## 데이터 형식
`briefings.json`은 `[{"date":"YYYY-MM-DD","title":"...","summary":"...","topics":[],"study":"...","sourceStatus":"...","etfs":[],"indices":[],"news":[]}]` 형식입니다.

## 검증
`python -m py_compile scripts/update.py` 및 `python -m unittest discover -s tests`로 기본 테스트를 수행합니다. 외부 네트워크가 없는 환경에서는 실제 API 연결을 검증할 수 없습니다.
