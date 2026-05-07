# services/vision_service.py

import os
from PIL import Image
from PIL.ExifTags import TAGS


# ==================================================
# 🔍 BASIC QUALITY CHECK
# ==================================================
def basic_check(image_path):
    try:
        img = Image.open(image_path)

        width, height = img.size
        size_kb = os.path.getsize(image_path) / 1024

        if width < 200 or height < 200:
            return "low_quality"

        if size_kb < 10:
            return "suspicious"

        return "ok"

    except:
        return "invalid"


# ==================================================
# 🧠 EXIF METADATA CHECK (VERY POWERFUL)
# ==================================================
def check_metadata(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()

        if not exif_data:
            return "no_metadata"   # ⚠️ AI images often have no EXIF

        metadata = {}

        for tag, value in exif_data.items():
            decoded = TAGS.get(tag, tag)
            metadata[decoded] = value

        software = str(metadata.get("Software", "")).lower()

        # 🔥 Detect editing tools
        if any(x in software for x in ["photoshop", "gimp", "canva", "editor"]):
            return "edited"

        return "ok"

    except:
        return "unknown"


# ==================================================
# 🎯 FAKE IMAGE HEURISTIC DETECTOR
# ==================================================
def heuristic_fake_detection(image_path):
    try:
        img = Image.open(image_path).convert("RGB")
        pixels = list(img.getdata())

        # 🔍 Check color variation (AI images often too smooth)
        unique_colors = len(set(pixels))

        if unique_colors < 500:
            return "ai_like"

        return "ok"

    except:
        return "unknown"


# ==================================================
# 🎯 FINAL DECISION ENGINE
# ==================================================
def validate_image(image_path):
    score = 0
    suspicious_message = "Image appears to be edited, AI-generated, or unclear. Please upload a real product photo."

    # 1. Basic check
    basic = basic_check(image_path)
    if basic != "ok":
        return {
            "type": "image_rejected",
            "message": suspicious_message
        }

    # 2. Metadata check
    meta = check_metadata(image_path)
    if meta == "no_metadata":
        score += 1
    elif meta == "edited":
        score += 2

    # 3. Heuristic check
    heuristic = heuristic_fake_detection(image_path)
    if heuristic == "ai_like":
        score += 2

    # ==================================================
    # 🎯 DECISION LOGIC
    # ==================================================
    if score >= 3:
        return {
            "type": "image_fake",
            "message": suspicious_message
        }

    return {
        "type": "image_valid",
        "message": "Image verified successfully."
    }