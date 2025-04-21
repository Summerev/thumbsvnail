# Thumbsvnail - AI 썸네일 자동 생성기

📸 유튜브 제목과 카테고리를 입력하면 GPT와 Stable Diffusion을 통해 자동으로 고화질 썸네일을 생성해주는 Flask 기반 웹앱입니다.

## 기능
- GPT로 썸네일 프롬프트 생성
- Stable Diffusion 이미지 생성
- 텍스트 자동 삽입
- ZIP 파일로 압축 및 다운로드
- 이메일 전송
- 이미지 미리보기 제공
- Freemium 요금제 구조 (3장 제한)

## 실행 방법 (로컬)
```bash
pip install -r requirements.txt
cp .env.example .env  # 후에 키 직접 입력
python app.py
```

## 배포 방법 (Render)
1. [https://render.com](https://render.com)에서 New → Web Service
2. GitHub 레포 연결
3. Start command: `python app.py`
4. Environment variables에 `.env` 값 입력
