# ============================================================
# app.py - 넷플릭스 스타일 주말 추천 서비스
# 실행 방법:
#   1. pip install flask
#   2. python app.py
#   3. 브라우저에서 http://127.0.0.1:5000 접속
# ============================================================

from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# ============================================================
# 더미 데이터: 넷플릭스 인기 작품 20개
# 각 항목: 제목, 장르, 평점(10점 만점), 포스터 URL, 줄거리, 넷플릭스 링크
# ============================================================
MOVIES = [
    {
        "title": "오징어 게임",
        "genre": "스릴러/드라마",
        "rating": 9.2,
        "poster": "https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=400&q=80",
        "summary": "456억 원의 상금을 걸고 목숨을 건 서바이벌 게임에 참가한 사람들의 이야기.",
        "link": "https://www.netflix.com/title/81040344"
    },
    {
        "title": "기묘한 이야기",
        "genre": "SF/공포/드라마",
        "rating": 8.7,
        "poster": "https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?w=400&q=80",
        "summary": "작은 마을에서 일어나는 초자연적 사건들과 그것을 파헤치는 아이들의 모험.",
        "link": "https://www.netflix.com/title/80057281"
    },
    {
        "title": "더 크라운",
        "genre": "역사/드라마",
        "rating": 8.6,
        "poster": "https://images.unsplash.com/photo-1549880338-65ddcdfd017b?w=400&q=80",
        "summary": "영국 왕실의 비밀과 엘리자베스 2세의 파란만장한 인생을 그린 대작 드라마.",
        "link": "https://www.netflix.com/title/80025678"
    },
    {
        "title": "나르코스",
        "genre": "범죄/드라마",
        "rating": 8.8,
        "poster": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=400&q=80",
        "summary": "콜롬비아 마약왕 파블로 에스코바르와 DEA 요원들의 치열한 추격전.",
        "link": "https://www.netflix.com/title/80025172"
    },
    {
        "title": "블랙 미러",
        "genre": "SF/스릴러",
        "rating": 8.8,
        "poster": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=400&q=80",
        "summary": "기술이 지배하는 미래 사회의 어두운 단면을 보여주는 앤솔로지 시리즈.",
        "link": "https://www.netflix.com/title/70264888"
    },
    {
        "title": "머니 하이스트",
        "genre": "범죄/액션",
        "rating": 8.9,
        "poster": "https://images.unsplash.com/photo-1580519542036-c47de6196ba5?w=400&q=80",
        "summary": "교수가 이끄는 강도단이 조폐국을 점령해 완벽한 작전을 펼치는 스페인 범죄 드라마.",
        "link": "https://www.netflix.com/title/80192098"
    },
    {
        "title": "위처",
        "genre": "판타지/액션",
        "rating": 8.2,
        "poster": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=400&q=80",
        "summary": "괴물 사냥꾼 게롤트가 운명으로 엮인 소녀 시리와 함께 세계를 구하는 판타지 서사.",
        "link": "https://www.netflix.com/title/80189685"
    },
    {
        "title": "종이의 집: 공동경제구역",
        "genre": "범죄/스릴러",
        "rating": 7.6,
        "poster": "https://images.unsplash.com/photo-1601128533718-374ffcca299b?w=400&q=80",
        "summary": "분단된 한반도를 배경으로 한 대규모 강도 작전과 예측 불허의 반전.",
        "link": "https://www.netflix.com/title/81166743"
    },
    {
        "title": "지금 우리 학교는",
        "genre": "좀비/액션/드라마",
        "rating": 7.8,
        "poster": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=400&q=80",
        "summary": "고등학교에서 좀비 바이러스가 퍼지고 학생들이 생존을 위해 사투를 벌이는 K-좀비물.",
        "link": "https://www.netflix.com/title/81237099"
    },
    {
        "title": "브리저튼",
        "genre": "로맨스/드라마",
        "rating": 7.3,
        "poster": "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=400&q=80",
        "summary": "19세기 런던 사교계를 배경으로 펼쳐지는 화려하고 달콤한 로맨스.",
        "link": "https://www.netflix.com/title/80232398"
    },
    {
        "title": "퀸스 갬빗",
        "genre": "드라마",
        "rating": 8.6,
        "poster": "https://images.unsplash.com/photo-1586165368502-1bad197a6461?w=400&q=80",
        "summary": "고아 소녀가 체스 천재로 성장하며 세계 챔피언을 향해 나아가는 성장 드라마.",
        "link": "https://www.netflix.com/title/80234304"
    },
    {
        "title": "오자크",
        "genre": "범죄/스릴러",
        "rating": 8.4,
        "poster": "https://images.unsplash.com/photo-1504701954957-2010ec3bcec1?w=400&q=80",
        "summary": "마약 카르텔의 돈세탁에 엮인 가족이 오자크 호수 마을에서 살아남으려는 사투.",
        "link": "https://www.netflix.com/title/80117552"
    },
    {
        "title": "루시퍼",
        "genre": "판타지/범죄/로맨스",
        "rating": 8.1,
        "poster": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=400&q=80",
        "summary": "지옥을 떠나 LA에 정착한 악마 루시퍼가 형사와 함께 사건을 해결하는 유쾌한 드라마.",
        "link": "https://www.netflix.com/title/80057918"
    },
    {
        "title": "스물다섯 스물하나",
        "genre": "로맨스/청춘드라마",
        "rating": 8.3,
        "poster": "https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?w=400&q=80",
        "summary": "꿈을 향해 달려가는 두 청춘이 서로 성장하며 사랑을 키워가는 청춘 로맨스.",
        "link": "https://www.netflix.com/title/81289543"
    },
    {
        "title": "D.P.",
        "genre": "군대/드라마",
        "rating": 8.0,
        "poster": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&q=80",
        "summary": "군 탈영병을 쫓는 헌병 부대원들이 마주하는 한국 군대의 현실을 날카롭게 그린 작품.",
        "link": "https://www.netflix.com/title/81280917"
    },
    {
        "title": "수리남",
        "genre": "범죄/액션",
        "rating": 7.4,
        "poster": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80",
        "summary": "남미 수리남에서 마약 조직에 연루된 사업가가 국정원과 협력해 조직을 무너뜨리는 이야기.",
        "link": "https://www.netflix.com/title/81166351"
    },
    {
        "title": "더 글로리",
        "genre": "복수/드라마/스릴러",
        "rating": 8.5,
        "poster": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&q=80",
        "summary": "학교폭력 피해자가 수십 년에 걸쳐 완벽한 복수를 계획하고 실행하는 다크 드라마.",
        "link": "https://www.netflix.com/title/81411069"
    },
    {
        "title": "솔로지옥",
        "genre": "리얼리티/연애",
        "rating": 7.0,
        "poster": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?w=400&q=80",
        "summary": "외딴 섬에서 펼쳐지는 한국판 리얼리티 연애 프로그램. 천국과 지옥을 오가는 감정의 롤러코스터.",
        "link": "https://www.netflix.com/title/81330711"
    },
    {
        "title": "종이의 집",
        "genre": "범죄/스릴러",
        "rating": 8.3,
        "poster": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&q=80",
        "summary": "스페인 조폐국 인질 강도 사건을 치밀하게 계획한 교수와 강도단의 두뇌 싸움.",
        "link": "https://www.netflix.com/title/80192098"
    },
    {
        "title": "웬즈데이",
        "genre": "미스터리/코미디/공포",
        "rating": 8.1,
        "poster": "https://images.unsplash.com/photo-1509248961158-e54f6934749c?w=400&q=80",
        "summary": "기숙학교에 전학 온 웬즈데이 아담스가 초능력으로 연쇄 살인 사건을 해결하는 블랙 코미디.",
        "link": "https://www.netflix.com/title/81231974"
    },
]


# ============================================================
# 라우트 1: 메인 페이지 렌더링
# ============================================================
@app.route("/")
def index():
    return render_template("index.html")


# ============================================================
# 라우트 2: 평점 높은 순 정렬 데이터 반환 (JSON)
# 프론트엔드에서 fetch("/movies/top")로 호출
# ============================================================
@app.route("/movies/top")
def movies_top():
    # rating 기준 내림차순 정렬
    sorted_movies = sorted(MOVIES, key=lambda x: x["rating"], reverse=True)
    return jsonify(sorted_movies)


# ============================================================
# 라우트 3: 랜덤 추천 1개 반환 (JSON)
# 프론트엔드에서 fetch("/movies/random")으로 호출
# ============================================================
@app.route("/movies/random")
def movies_random():
    pick = random.choice(MOVIES)
    return jsonify(pick)


# ============================================================
# 서버 실행
# ============================================================
if __name__ == "__main__":
    app.run(debug=True)

    
