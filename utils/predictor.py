
import numpy as np

from utils.model_loader import load_model
from utils.image_processor import preprocess_image

# ==========================================
# PNEUMO-AI | PREDICTION ENGINE
# ==========================================

CLASS_NAMES = ["NORMAL", "PNEUMONIA"]


def predict_image(image):
    """
    Melakukan prediksi citra X-Ray menggunakan
    model MobileNetV2 S2_011.

    Returns
    -------
    dict:
        predicted_class
        confidence
        probabilities
    """

    model = load_model()

    # Preprocessing citra
    image_array = preprocess_image(image)

    # Inferensi model
    prediction = model.predict(
        image_array,
        verbose=0
    )

    # Model binary sigmoid:
    # output = probabilitas kelas PNEUMONIA
    pneumonia_probability = float(
        np.asarray(prediction).reshape(-1)[0]
    )

    # Batasi untuk menjaga validitas numerik
    pneumonia_probability = float(
        np.clip(pneumonia_probability, 0.0, 1.0)
    )

    normal_probability = 1.0 - pneumonia_probability

    probabilities = {
        "NORMAL": normal_probability,
        "PNEUMONIA": pneumonia_probability
    }

    predicted_class = (
        "PNEUMONIA"
        if pneumonia_probability >= 0.5
        else "NORMAL"
    )

    confidence = probabilities[predicted_class]

    return {
        "predicted_class": predicted_class,
        "confidence": confidence,
        "probabilities": probabilities
    }
