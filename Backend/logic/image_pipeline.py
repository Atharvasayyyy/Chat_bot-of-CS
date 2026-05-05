# logic/image_pipeline.py

from ultralytics import YOLO

# 🔥 Load YOLO model once
model = YOLO("yolov8n.pt")


# ==================================================
# 🔧 YOLO OBJECT DETECTION
# ==================================================
def run_yolo(image_path):

    results = model(image_path)

    detections = []

    for r in results:
        if r.boxes is None:
            continue

        for box in r.boxes:
            label = model.names[int(box.cls)]
            confidence = float(box.conf)

            detections.append({
                "label": label,
                "confidence": confidence
            })

    return detections


# ==================================================
# 🚀 IMAGE PROCESSING (FIXED)
# ==================================================
def process_image(image_path):

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
            "object": label,
            "confidence": confidence,
            "damage_detected": False,
            "message": "Image is unclear. Please upload a clearer image."
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
    
    
    