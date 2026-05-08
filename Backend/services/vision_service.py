# services/vision_service.py

import os
from PIL import Image, ImageFilter
from PIL.ExifTags import TAGS
import math
import logging

logger = logging.getLogger(__name__)


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

        # 1) Unique color count — AI images sometimes have limited palettes
        try:
            colors = img.getcolors(maxcolors=1000000)
            unique_colors = len(colors) if colors else 0
        except Exception:
            unique_colors = 0

        # 2) Entropy (grayscale) — very low entropy suggests synthetic image
        try:
            gray = img.convert("L")
            hist = gray.histogram()
            total = sum(hist) or 1
            probs = [h / total for h in hist if h > 0]
            entropy = -sum(p * math.log2(p) for p in probs)
        except Exception:
            entropy = 0

        # 3) Edge density — synthetic images can be overly smooth
        try:
            edges = gray.filter(ImageFilter.FIND_EDGES)
            bw = edges.point(lambda p: 255 if p > 30 else 0)
            nonzero = sum(1 for px in bw.getdata() if px > 0)
            edge_density = nonzero / (bw.width * bw.height)
        except Exception:
            edge_density = 0

        logger.debug(
            "vision heuristics: unique_colors=%s entropy=%.2f edge_density=%.4f",
            unique_colors, entropy, edge_density,
        )

        # Heuristic thresholds (tuned to be conservative - may be adjusted)
        if unique_colors and unique_colors < 2000:
            return "ai_like"

        if entropy and entropy < 4.5:
            return "ai_like"

        if edge_density and edge_density < 0.01:
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

    # 2. Metadata check (missing metadata is a strong signal)
    meta = check_metadata(image_path)
    if meta == "no_metadata":
        score += 2
    elif meta == "edited":
        score += 3

    # 3. Heuristic check (color/entropy/edges)
    heuristic = heuristic_fake_detection(image_path)
    if heuristic == "ai_like":
        score += 3

    # ==================================================
    # 🎯 DECISION LOGIC
    # ==================================================
    # Lower the threshold: stronger signals are required to accept an image.
    if score >= 3:
        return {
            "type": "image_fake",
            "message": suspicious_message
        }

    return {
        "type": "image_valid",
        "message": "Image verified successfully."
    }