from flask import Flask, render_template, request, send_file
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('home.html')  

@app.route('/convert', methods=['POST'])
def convert():
    images = request.files.getlist('images')
    if not images:
        return "No images uploaded", 400

    image_objs = []
    for img in images:
        img_path = os.path.join(UPLOAD_FOLDER, img.filename)
        img.save(img_path)
        image = Image.open(img_path).convert('RGB')
        image_objs.append(image)

    pdf_path = os.path.join(UPLOAD_FOLDER, 'output.pdf')

    if image_objs:
        first_image = image_objs[0]
        if len(image_objs) > 1:
            first_image.save(pdf_path, save_all=True, append_images=image_objs[1:])
        else:
            first_image.save(pdf_path)

    # Optional: delete uploaded images after PDF creation
    for img in images:
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, img.filename))
        except Exception:
            pass

    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
