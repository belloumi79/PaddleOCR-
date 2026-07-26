"""
PaddleOCR Server for Tunisian License Plate Recognition
100% free, open source, best Arabic OCR available

Usage:
  pip install -r requirements.txt
  python server.py

Server runs on http://0.0.0.0:$PORT
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from paddleocr import PaddleOCR
import tempfile
import os
import sys

app = Flask(__name__)
CORS(app)

# Initialize PaddleOCR — Arabic + English, no GPU needed
ocr = None

def init_ocr():
    global ocr
    if ocr is None:
        print("Initializing PaddleOCR (Arabic + English)...")
        ocr = PaddleOCR(
            use_angle_cls=True,
            lang='en',
            use_gpu=False,
            show_log=False,
            det_db_thresh=0.3,
            det_db_unclip_ratio=1.8,
        )
        print("PaddleOCR ready!")
    return ocr


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'service': 'PaddleOCR License Plate Recognition',
        'status': 'running',
        'endpoints': {
            'POST /ocr': 'Upload image for OCR',
            'GET /health': 'Health check'
        }
    })


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'engine': 'PaddleOCR'})


@app.route('/ocr', methods=['POST'])
def ocr_endpoint():
    """Accept image file, return OCR text"""
    try:
        init_ocr()

        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if not file.filename:
            return jsonify({'error': 'Empty filename'}), 400

        # Save to temp file
        suffix = os.path.splitext(file.filename)[1] or '.jpg'
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name

        try:
            # Run OCR
            results = ocr.ocr(tmp_path, cls=True)

            texts = []
            if results and results[0]:
                for line in results[0]:
                    text = line[1][0]
                    confidence = line[1][1]
                    texts.append({'text': text, 'confidence': round(confidence, 4)})

            # Combine all detected text
            full_text = '\n'.join(t['text'] for t in texts)

            return jsonify({
                'text': full_text,
                'detections': texts,
            })
        finally:
            os.unlink(tmp_path)

    except Exception as e:
        print(f"OCR error: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting PaddleOCR server on port {port}")
    init_ocr()
    app.run(host='0.0.0.0', port=port, debug=False)
