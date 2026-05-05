# logic/evidence.py

def analyze_evidence(text=None, image_url=None):
    return {
        "has_image": image_url is not None,
        "text_length": len(text) if text else 0,
        "description_quality": "high" if text and len(text) > 30 else "low"
    }