# ✈️ Airline Reservation System

Flask + MySQL로 구현한 항공사 예약 관리 웹 애플리케이션입니다. 고객은 항공편을 검색하고 예매/취소할 수 있으며, 항공사 직원은 항공편·항공기·공항 정보를 관리할 수 있습니다.

## 주요 기능

### 👤 고객 (Customer)
- 회원가입 / 로그인
- 출발지·도착지·날짜 기준 항공편(편도/왕복) 검색
- 항공편 상태(정시/지연) 조회
- 항공권 예매 및 결제(checkout)
- 내 항공편 조회 (`view_myflights`)
- 항공권 취소 (출발 24시간 이전 건에 한함)

### 🧑‍✈️ 항공사 직원 (Airline Staff)
- 회원가입 / 로그인
- 소속 항공사의 항공편 대시보드 조회 (기간·출발지·도착지 필터)
- 신규 항공편 등록
- 항공편 지연/정시 상태 변경
- 소속 항공사의 항공기 조회 및 신규 등록
- 특정 항공편의 탑승 고객 목록 조회
- 공항 등록 및 조회

## 기술 스택

| 구분 | 내용 |
|---|---|
| Backend | Python, Flask |
| Database | MySQL (`pymysql`) |
| Frontend | Jinja2 템플릿, HTML/CSS |
| DB 설계 | MySQL Workbench (`airline_final_project.mwb`) |

## 프로젝트 구조

```
Databases/
├── project.py                   # Flask 애플리케이션 (라우트 & DB 쿼리)
├── airline_final_project.mwb    # MySQL Workbench ER 다이어그램 / 스키마 설계 파일
├── static/
│   └── static/styles.css        # 공통 스타일시트
└── templates/
    └── templates/
        ├── index.html               # 메인/항공편 검색
        ├── login.html                # 로그인
        ├── register_customer.html    # 고객 회원가입
        ├── register_staff.html       # 직원 회원가입
        ├── customer_dashboard.html   # 고객 대시보드
        ├── staff_dashboard.html      # 직원 대시보드
        ├── flight_status.html        # 항공편 상태 조회
        ├── book_ticket.html          # 항공권 예매
        ├── checkout.html             # 결제
        ├── myflight.html             # 내 항공편
        ├── cancel.html               # 항공권 취소
        ├── create_flights.html       # 항공편 등록
        ├── add_airplane.html         # 항공기 등록
        ├── view_airplanes.html       # 항공기 목록
        ├── add_airport.html          # 공항 등록
        ├── view_airport.html         # 공항 목록
        └── view_customers.html       # 탑승 고객 목록
```

## 데이터베이스 스키마

`project.py`의 쿼리를 기준으로 한 주요 테이블은 다음과 같습니다. (상세 ERD는 `airline_final_project.mwb`를 MySQL Workbench로 열어 확인하세요.)

| 테이블 | 설명 | 주요 컬럼 |
|---|---|---|
| `customer` | 고객 정보 | `fname`, `lname`, `email`(PK), `password`, `dob` |
| `airlinestaff` | 항공사 직원 정보 | `username`(PK), `password`, `airline_name` |
| `airplane` | 항공기 정보 | `ID`(PK), `seats`, `Airline_name`, `manufacturing_company`, `model_num`, `manufacturing_date`, `age` |
| `flight` | 항공편 정보 | `ID`(PK), `dep_airport`, `dep_date`, `dep_time`, `arr_airport`, `arr_date`, `arr_time`, `baseprice`, `status`, `Airplane_ID`(FK) |
| `ticket` | 예매 정보 | `id`(PK), `flight_id`(FK), `customer_email`(FK), `fname`, `lname`, `dob`, `price`, `card_type`, `card_num`, `exp_date`, `purchase_date` |
| `airport` | 공항 정보 | `code`(PK), `name`, `city`, `country`, `terminal`, `type` |

> 💡 좌석 점유율이 70% 이상인 항공편은 예매 시 기본 요금(`baseprice`)의 1.25배로 자동 책정됩니다.

## 시작하기

### 1. 요구 사항
- Python 3.x
- MySQL Server
- Flask, PyMySQL

```bash
pip install flask pymysql
```

### 2. 데이터베이스 준비
1. MySQL에 `aironline`이라는 이름으로 데이터베이스를 생성합니다.
2. `airline_final_project.mwb`를 MySQL Workbench로 열어 스키마를 확인하고, **Forward Engineer** 기능으로 위 테이블들을 생성합니다.

### 3. 접속 정보 설정
`project.py`의 접속 정보를 로컬 환경에 맞게 수정합니다.

```python
conn = pymysql.connect(host='localhost',
                        user='root',
                        password='',
                        db='aironline',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
```

### 4. 서버 실행

```bash
python project.py
```

서버가 실행되면 `http://127.0.0.1:5000` 에서 접속할 수 있습니다.

## ⚠️ 참고 사항

이 프로젝트는 학습/과제 목적의 데모 프로젝트입니다. 프로덕션에 배포하기 전에는 다음 사항을 반드시 개선해야 합니다.

- 비밀번호가 평문으로 저장·비교되고 있습니다. (해싱 필요)
- DB 접속 정보와 `SECRET_KEY`가 소스 코드에 하드코딩되어 있습니다. (환경 변수로 분리 필요)
- `debug=True` 상태로 실행되고 있어 운영 환경에는 적합하지 않습니다.
