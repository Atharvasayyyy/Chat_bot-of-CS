# logic/image_pipeline.py

import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

# Lazy-load YOLO model to avoid import-time failures in constrained environments
_yolo_model = None

def get_yolo_model():
    global _yolo_model
    if _yolo_model is not None:
        return _yolo_model

    try:
        from ultralytics import YOLO

        # Attempt to load model; wrap in try/except because loading may fail in some
        # build environments (torch serialization restrictions, missing libs, etc.).
        _yolo_model = YOLO("yolov8n.pt")
        logger.info("YOLO model loaded successfully")
    except Exception as e:
        # Log error and continue. The rest of the app will function without vision features.
        logger.exception("Failed to load YOLO model: %s", e)
        _yolo_model = None

    return _yolo_model


# ==================================================
# 🔧 YOLO OBJECT DETECTION
# ==================================================
def run_yolo(image_path: str) -> List[Dict]:
    """Run YOLO detection on the provided image path.

    Returns empty list if the model is unavailable or no detections found.
    """
    model = get_yolo_model()
    if model is None:
        logger.warning("YOLO model unavailable — skipping vision processing")
        return []

    try:
        results = model(image_path)
    except Exception:
        logger.exception("Error running YOLO on image: %s", image_path)
        return []

    detections: List[Dict] = []

    for r in results:
        if getattr(r, 'boxes', None) is None:
            continue

        for box in r.boxes:
            try:
                label = model.names[int(box.cls)]
            except Exception:
                label = str(getattr(box, 'cls', ''))
            try:
                confidence = float(getattr(box, 'conf', 0.0))
            except Exception:
                confidence = 0.0

            detections.append({
                "label": label,
                "confidence": confidence
            })

    return detections


# ==================================================
# 🚀 IMAGE PROCESSING (FIXED)
# ==================================================
def process_image(image_path):

    suspicious_message = "Image appears to be edited, AI-generated, or unclear. Please upload a real product photo."

    print("📸 Processing image:", image_path)

    detections = run_yolo(image_path)

    # ==================================================
    # ❌ NO OBJECT DETECTED
    # ==================================================
    if not detections:
        return {
            "type": "image_ok",
            "object": None,
            "confidence": 0.0,
            "damage_detected": False,
            "message": "No clear object detected. Please upload a clearer image."
        }

    # ==================================================
    # 🔥 BEST DETECTION
    # ==================================================
    best = max(detections, key=lambda x: x["confidence"])

    label = best["label"]
    confidence = best["confidence"]

    print(f"🔍 Detected: {label} ({confidence:.2f})")

    # ==================================================
    # ⚠️ LOW CONFIDENCE
    # ==================================================
    if confidence < 0.4:
        return {
            "type": "image_ok",
            "object": None,
            "confidence": confidence,
            "damage_detected": False,
            "message": suspicious_message
        }

    # ==================================================
    # 🔥 VALID OBJECT DETECTED
    # ==================================================
    return {
        "type": "image_ok",
        "object": label,
        "confidence": confidence,
        "damage_detected": False,  # 🔥 IMPORTANT: YOLO doesn't detect damage
        "message": f"Detected object: {label}"
    }
    
    
    