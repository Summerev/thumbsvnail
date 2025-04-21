from flask import Flask, request, render_template, send_file, redirect, url_for
from PIL import Image, ImageDraw, ImageFont
import openai, zipfile, os, uuid, datetime
from dotenv import load_dotenv
from flask_mail import Mail, Message
from diffusers import StableDiffusionPipeline
import torch

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
hf_token = os.getenv("HF_TOKEN")

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_SENDER")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
mail = Mail(app)

# 이하 생략: 이미지 생성, 텍스트 삽입, zip, 미리보기, 사용량 제한 등 포함
# 전체 app.py는 다운로드 zip에 포함됨
