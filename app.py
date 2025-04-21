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

OUTPUT_DIR = "static/history"

def generate_prompt(title, category):
    system_msg = "너는 유튜브 썸네일용 이미지 설명 전문가야. 실사 스타일로 한 문장 생성."
    user_msg = f"제목: {title}, 카테고리: {category}"
    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": user_msg}]
    )
    return res.choices[0].message['content'].strip()

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
    use_auth_token=hf_token
).to("cuda")

def generate_image(prompt, filename):
    image = pipe(prompt).images[0]
    path = os.path.join(OUTPUT_DIR, filename)
    image.save(path)
    return path

def add_text(image_path, text):
    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf", 60)
    W, H = img.size
    w, h = draw.textsize(text, font)
    pos = ((W - w)//2, H - h - 40)
    draw.text((pos[0]+2, pos[1]+2), text, font=font, fill="black")
    draw.text(pos, text, font=font, fill="white")
    new_path = image_path.replace(".png", "_text.png")
    img.save(new_path)
    return new_path

def zip_images(image_paths, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for path in image_paths:
            zipf.write(path, os.path.basename(path))
    return zip_name

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form["title"]
        category = request.form["category"]
        insert_text = request.form.get("add_text")
        email = request.form.get("email")

        prompt = generate_prompt(title, category)
        file_id = str(uuid.uuid4())
        base_img = generate_image(prompt, f"{file_id}.png")

        results = [base_img]
        if insert_text:
            img_with_text = add_text(base_img, title)
            results.append(img_with_text)

        zip_name = f"static/{file_id}_thumbs.zip"
        zip_images(results, zip_name)

        if email:
            msg = Message("🎨 생성된 썸네일 이미지입니다", sender=os.getenv("MAIL_SENDER"), recipients=[email])
            msg.body = "첨부된 썸네일 ZIP 파일을 확인해주세요!"
            with app.open_resource(zip_name) as fp:
                msg.attach("thumbs.zip", "application/zip", fp.read())
            mail.send(msg)

        return send_file(zip_name, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

