from math import cos, pi, sin
import json
import os
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "change-me")

MENU_ITEMS = [
    {"name": "Margherita Pizza", "description": "Fresh mozzarella, basil, San Marzano tomatoes", "price": 12},
    {"name": "Pollo", "description": "Citrus-marinated chicken, roasted seasonal vegetables", "price": 16},
    {"name": "Garden Salad", "description": "Mixed greens, cherry tomatoes, cucumber, house vinaigrette", "price": 9},
]

SPECIALS = [
    {"name": "Chef's Tasting Menu", "description": "Five courses featuring seasonal favorites", "price": 45},
    {"name": "Housemade Gelato Trio", "description": "Rotating flavors crafted daily", "price": 8},
]

RING_SIZE_FILE = Path(__file__).resolve().parent / "ring_sizes.json"

LOVE_STORY_PASSCODE = "lightbulb"

LOVE_STORY_BACKGROUNDS = {
    "hero": {"image": "images/space-texture.png", "color": "#05050f"},
    "constellation": {"image": "images/photo-7.jpg", "color": "#1b0a17"},
    "photo_left": {"image": "images/photo-1.jpg", "color": "#090612"},
    "story_sunrise": {"image": "images/space.png", "color": "#06060d"},
    "photo_right": {"image": "images/photo-2.JPEG", "color": "#080713"},
    "story_home": {"image": "images/photo-11.jpg", "color": "#05050f"},
    "gallery": {"image": "images/photo-6.jpg", "color": "#05050f"},
    "photo_third": {"image": "images/photo-8.jpg", "color": "#070414"},
    "story_finale_intro": {"image": "images/photo-9.jpg", "color": "#070511"},
    "finale": {"image": "images/photo-9.jpg", "color": "#06030b"},
}

def _append_ring_size_entry(ring_size: str) -> None:
    entry = {"ring_size": ring_size, "timestamp": datetime.utcnow().isoformat() + "Z"}

    try:
        if RING_SIZE_FILE.exists():
            existing = json.loads(RING_SIZE_FILE.read_text(encoding="utf-8"))
            if not isinstance(existing, list):
                existing = []
        else:
            existing = []
    except json.JSONDecodeError:
        existing = []

    existing.append(entry)
    RING_SIZE_FILE.write_text(json.dumps(existing, indent=2), encoding="utf-8")

def _build_python_heart(steps: int = 240, scale: float = 9.5, padding: float = 14.0) -> dict:
    """Generate a smooth SVG path for a heart using the classic parametric equation."""

    points = []
    for step in range(steps):
        t = (2 * pi * step) / steps
        x = 16 * sin(t) ** 3
        y = 13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t)
        points.append((x, y))

    xs = [x for x, _ in points]
    ys = [y for _, y in points]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    width = (max_x - min_x) * scale + padding * 2
    height = (max_y - min_y) * scale + padding * 2

    # Flip vertically for SVG and translate so the shape sits inside the padded viewBox.
    path_coords = []
    for x, y in points:
        svg_x = (x - min_x) * scale + padding
        svg_y = (max_y - y) * scale + padding
        path_coords.append((svg_x, svg_y))

    move_x, move_y = path_coords[0]
    commands = [f"M{move_x:.3f},{move_y:.3f}"]
    commands.extend(f"L{x:.3f},{y:.3f}" for x, y in path_coords[1:])
    commands.append("Z")

    return {
        "path": " ".join(commands),
        "viewbox": f"0 0 {width:.3f} {height:.3f}",
    }

@app.route("/")
def home():
    return render_template(
        "home.html",
        menu_items=MENU_ITEMS,
        specials=SPECIALS,
    )

@app.route("/presentation")
def presentation():
    return render_template("presentation.html")

@app.route("/ring-size", methods=["POST"])
def capture_ring_size():
    payload = request.get_json(silent=True) or {}
    ring_size = str(payload.get("ringSize", "")).strip()

    if not ring_size:
        return jsonify({"ok": False, "error": "Please share a ring size before sending."}), 400

    if len(ring_size) > 120:
        return jsonify({"ok": False, "error": "That looks a bit long. Try a shorter note."}), 400

    _append_ring_size_entry(ring_size)
    return jsonify({"ok": True})


@app.route("/unlock", methods=["POST"])
def unlock_love_story():
    payload = request.get_json(silent=True) or {}
    passcode = str(payload.get("passcode", "")).strip()

    if passcode.lower() == LOVE_STORY_PASSCODE.lower():
        return jsonify({"ok": True})

    return jsonify({"ok": False, "error": "That password doesn't match. Try again?"}), 401


@app.route("/love-story")
def love_story():
    python_heart = _build_python_heart()
    return render_template("love_story.html", python_heart=python_heart, backgrounds=LOVE_STORY_BACKGROUNDS, unlocked=False)

if __name__ == "__main__":
    app.run(debug=True)
