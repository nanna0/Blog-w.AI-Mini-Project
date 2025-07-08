# 🧠 AI 기반 Django 블로그 프로젝트

AI 맞춤법 검사 기능이 내장된 Django 블로그입니다.  
회원가입, 게시글 CRUD, 첨부파일, 댓글, 좋아요, 카테고리, 검색 기능까지 지원합니다.

---

## ✨ 주요 기능

- ✅ **회원가입 / 로그인 / 로그아웃 / 인증**
- ✅ **게시글 작성 / 수정 / 삭제**
- ✅ **카테고리 분류**
- ✅ **첨부파일 업로드 및 다운로드**
- ✅ **댓글 작성 기능**
- ✅ **좋아요 (❤️) 기능**
- ✅ **게시글 검색 기능**
- ✅ **임시 게시글은 본인만 열람 가능**
- ✅ **OpenAI API 연동 - 맞춤법 검사 기능**
- ✅ **Bootstrap 기반 UI 적용**

---

## 📂 프로젝트 구조

```
Blog(w.AI)_Project2/
├── account/ # 사용자 관련 앱
├──── templates # account 관련 템플릿
├── blog/ # 블로그 게시글 관련 앱
├──── templates/ # blog 템플릿
├── config
├── media/
├──── attachment/ # 첨부파일 업로드
├── .env 
├── manage.py
└── requirements.txt
```

## 🤖 AI 맞춤법 검사 기능
- 게시글 작성 시 "맞춤법 검사" 버튼을 눌러 GPT 모델로 문장을 교정할 수 있습니다.
- OpenAI API 키가 필요합니다.

## 🔎 게시글 검색
- 블로그 리스트 상단에 검색창을 제공
- 제목/내용/작성자 이름을 기준으로 검색 가능

## 📌 기술 스택
- Python 3.11+
- Django 5.2.3
- PostgreSQL
- Bootstrap 5
- OpenAI API
- dotenv

## wbs
<img width="1107" alt="스크린샷 2025-07-04 오후 4 29 59" src="https://github.com/user-attachments/assets/cafec496-b629-41b6-87eb-4b5af4260e5f" />

## ERD
<img width="705" alt="스크린샷 2025-07-04 오후 4 25 08" src="https://github.com/user-attachments/assets/67bc242d-c352-4f7f-a8ea-f3f64c642a6d" />

