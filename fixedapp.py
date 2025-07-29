from flask import Flask, request, send_from_directory, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'images')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return "✅ Image Hosting Server Running!"

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/upload', methods=['POST'])
@app.route('/upload', methods=['POST'])
def upload():
    print("🔵 Upload route hit")
    print(f"🔵 Request content-type: {request.content_type}")
    print(f"🔵 Request files: {list(request.files.keys())}")

    if 'file' not in request.files:
        print("❌ No file key in request")
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)

    server_url = request.host_url.rstrip('/')
    image_url = f"{server_url}/images/{filename}"

    return jsonify({'image_url': image_url}), 200

if __name__ == '__main__':
    # 👇 Bind to PORT Render assigns dynamically
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
