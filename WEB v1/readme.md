# Sunset Bistro Demo

Simple restaurant landing page built with Flask. The app renders a single page that highlights menu favorites, weekly specials, and a reservation/contact section.

## Requirements

- Python 3.9 or newer
- `pip` to install packages

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install flask
```

## Run

```bash
flask --app app run
```

Then open http://127.0.0.1:5000 in your browser.

## Customize

- Update menu and special items in `app.py`.
- Tweak layout or branding in `templates/home.html` and `static/styles.css`.
