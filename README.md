# PaddleOCR License Plate Server

Free, open-source OCR server for Tunisian license plate recognition.
Deployed on Render free tier.

## API

### `GET /health`
Health check — returns `{"status": "ok", "engine": "PaddleOCR"}`

### `POST /ocr`
Upload an image, get OCR text back.

```bash
curl -X POST https://your-url.onrender.com/ocr \
  -F "file=@plate.jpg"
```

Response:
```json
{
  "text": "123 TUNIS 4567",
  "detections": [
    {"text": "123 TUNIS 4567", "confidence": 0.98}
  ]
}
```

## Local Development

```bash
pip install -r requirements.txt
python server.py
# Server runs on http://localhost:5000
```

## Deploy on Render

1. Push this repo to GitHub
2. Go to https://render.com → New Web Service
3. Connect your GitHub repo
4. Render auto-detects the Dockerfile
5. Deploy — free tier included

## Environment

- `PORT` — Server port (default: 5000)
