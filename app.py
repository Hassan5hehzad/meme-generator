from flask import Flask, request, render_template, send_file, redirect, url_for
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_meme(image_path, top_text="", bottom_text=""):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    width, height = img.size
    font_size = int(height / 10)
    
    try:
        font = ImageFont.truetype("impact.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # Text drawing with better positioning
    def draw_text(text, y_position):
        text_width = draw.textlength(text, font=font)
        x = (width - text_width) / 2
        # Draw outline
        for offset in range(-2, 3):
            draw.text((x+offset, y_position+offset), text, font=font, fill="black")
        # Draw main text
        draw.text((x, y_position), text, font=font, fill="white")

    if top_text:
        draw_text(top_text.upper(), 10)
    if bottom_text:
        draw_text(bottom_text.upper(), height - font_size - 20)

    img_io = io.BytesIO()
    img.save(img_io, 'JPEG', quality=90)
    img_io.seek(0)
    return img_io

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            top_text = request.form.get('top_text', '')
            bottom_text = request.form.get('bottom_text', '')
            meme = generate_meme(file, top_text, bottom_text)
            return send_file(meme, mimetype='image/jpeg', as_attachment=True, download_name='meme.jpg')
    return render_template("index.html")

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)