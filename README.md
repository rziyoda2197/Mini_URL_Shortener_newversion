# Mini URL Shortener

Flask + SQLite asosida URL qisqartirish servisi.

## Install
pip install -r requirements.txt

## Run
python app.py

## Endpoints

POST /shorten
Body:
{
  "url": "https://google.com"
}

GET /<short_code>
→ Redirect qiladi

GET /stats/<short_code>
→ Click count
