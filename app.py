from __future__ import annotations

from io import BytesIO
from pathlib import Path
import re

from flask import Flask, jsonify, request, send_file, send_from_directory
from PIL import Image


BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"
app = Flask(__name__)


def ingredient_files() -> set[str]:
    return {
        path.name
        for path in IMAGES_DIR.iterdir()
        if path.is_file() and path.name.startswith("IMG_") and path.suffix.lower() == ".png"
    }


def safe_filename(value: object) -> str:
    name = re.sub(r"[^a-zA-Z0-9_-]+", "-", str(value or "my-mala-keychain-shakers")).strip("-")
    return name or "my-mala-keychain-shakers"


@app.get("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/images/<path:filename>")
def image_asset(filename: str):
    if filename not in ingredient_files() and filename != "bowl.png":
        return "Not found", 404
    return send_from_directory(IMAGES_DIR, filename)


@app.post("/save-bowl")
def save_bowl():
    data = request.get_json(silent=True) or {}
    ingredients = data.get("ingredients")
    if not isinstance(ingredients, list) or not 1 <= len(ingredients) <= 6:
        return jsonify(error="Choose between one and six ingredients."), 400

    allowed_files = ingredient_files()
    bowl = Image.open(IMAGES_DIR / "bowl.png").convert("RGBA")
    canvas_width, canvas_height = bowl.size

    for ingredient in ingredients:
        if not isinstance(ingredient, dict) or ingredient.get("file") not in allowed_files:
            return jsonify(error="One of the chosen ingredients is invalid."), 400
        try:
            center_x = float(ingredient["centerX"])
            center_y = float(ingredient["centerY"])
            box_width = float(ingredient["width"])
            box_height = float(ingredient["height"])
        except (KeyError, TypeError, ValueError):
            return jsonify(error="Ingredient placement is invalid."), 400
        if not all(0 <= value <= 100 for value in (center_x, center_y, box_width, box_height)):
            return jsonify(error="Ingredient placement is outside the bowl."), 400

        source = Image.open(IMAGES_DIR / ingredient["file"]).convert("RGBA")
        target_width = max(1, round(canvas_width * box_width / 100))
        target_height = max(1, round(canvas_height * box_height / 100))
        scale = min(target_width / source.width, target_height / source.height)
        rendered_size = (max(1, round(source.width * scale)), max(1, round(source.height * scale)))
        rendered = source.resize(rendered_size, Image.Resampling.LANCZOS)
        x = round(canvas_width * center_x / 100 - rendered.width / 2)
        y = round(canvas_height * center_y / 100 - rendered.height / 2)
        bowl.alpha_composite(rendered, (x, y))

    output = BytesIO()
    bowl.save(output, format="PNG")
    output.seek(0)
    return send_file(output, mimetype="image/png", as_attachment=True, download_name=f"{safe_filename(data.get('filename'))}.png")


if __name__ == "__main__":
    app.run(debug=True)
