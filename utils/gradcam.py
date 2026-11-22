
import numpy as np
import tensorflow as tf
import cv2

from PIL import Image

from utils.model_loader import load_model
from utils.image_processor import preprocess_image


# ==========================================
# PNEUMO-AI | INTEGRATED GRAD-CAM ENGINE
# MobileNetV2 - S2_011
# ==========================================

BACKBONE_NAME = "mobilenetv2_1.00_224"
LAST_CONV_LAYER = "Conv_1"

IMAGE_SIZE = (224, 224)
CLASS_NAMES = ["NORMAL", "PNEUMONIA"]


def generate_gradcam(image, target_class=None):
    """
    Melakukan klasifikasi dan menghasilkan Grad-CAM
    dalam satu proses forward pass model.

    Parameters
    ----------
    image : PIL.Image
        Citra X-Ray asli.

    target_class : str or None
        NORMAL atau PNEUMONIA.
        None berarti menggunakan kelas hasil prediksi.

    Returns
    -------
    dict:
        predicted_class
        confidence
        probabilities
        original_image
        heatmap
        overlay
        target_class
        probability
    """

    # ======================================
    # 1. VALIDASI INPUT
    # ======================================

    if not isinstance(image, Image.Image):
        raise TypeError("Input harus berupa PIL.Image.")

    if target_class is not None:
        target_class = target_class.strip().upper()

        if target_class not in CLASS_NAMES:
            raise ValueError(
                "target_class harus NORMAL atau PNEUMONIA."
            )

    original_image = image.convert("RGB")

    image_array = preprocess_image(original_image)

    # ======================================
    # 2. MEMUAT MODEL
    # ======================================

    model = load_model()

    # ======================================
    # 3. MENGAKSES BACKBONE
    # ======================================

    backbone = model.get_layer(BACKBONE_NAME)

    target_layer = backbone.get_layer(LAST_CONV_LAYER)

    feature_model = tf.keras.Model(
        inputs=backbone.input,
        outputs=[
            target_layer.output,
            backbone.output
        ]
    )

    # ======================================
    # 4. CLASSIFICATION HEAD
    # ======================================

    head = tf.keras.Sequential([
        model.get_layer("global_average_pooling2d"),
        model.get_layer("classification_dropout"),
        model.get_layer("binary_classification")
    ])

    # ======================================
    # 5. FORWARD PASS + GRADIENT
    # ======================================

    with tf.GradientTape() as tape:

        activation, features = feature_model(
            image_array,
            training=False
        )

        prediction = head(
            features,
            training=False
        )

        pneumonia_probability = prediction[:, 0]

        normal_probability = 1.0 - pneumonia_probability

        # Kelas hasil prediksi otomatis
        predicted_class = (
            "PNEUMONIA"
            if float(pneumonia_probability[0].numpy()) >= 0.5
            else "NORMAL"
        )

        # Kelas yang akan dijelaskan
        selected_class = (
            target_class
            if target_class is not None
            else predicted_class
        )

        if selected_class == "PNEUMONIA":
            score = pneumonia_probability
        else:
            score = normal_probability

    # ======================================
    # 6. GRADIENT CALCULATION
    # ======================================

    gradients = tape.gradient(
        score,
        activation
    )

    if gradients is None:
        raise RuntimeError(
            "Gradien tidak terbentuk. "
            "Periksa koneksi target layer Grad-CAM."
        )

    gradient_finite = bool(
        tf.reduce_all(
            tf.math.is_finite(gradients)
        ).numpy()
    )

    if not gradient_finite:
        raise RuntimeError(
            "Gradien mengandung nilai NaN atau Inf."
        )

    # ======================================
    # 7. GENERATE CLASS ACTIVATION MAP
    # ======================================

    weights = tf.reduce_mean(
        gradients,
        axis=(1, 2)
    )

    activation = activation[0]
    weights = weights[0]

    cam = tf.reduce_sum(
        activation * weights,
        axis=-1
    )

    cam = tf.nn.relu(cam)

    cam_max = tf.reduce_max(cam)

    if float(cam_max.numpy()) <= 1e-8:
        raise RuntimeError(
            "Grad-CAM menghasilkan aktivasi kosong."
        )

    cam = cam / (
        cam_max + tf.constant(1e-8, dtype=cam.dtype)
    )

    heatmap_raw = cam.numpy()

    # ======================================
    # 8. PREPARE ORIGINAL IMAGE
    # ======================================

    original_resized = original_image.resize(
        IMAGE_SIZE,
        Image.Resampling.BILINEAR
    )

    original_array = np.asarray(
        original_resized,
        dtype=np.uint8
    )

    # ======================================
    # 9. CREATE COLORED HEATMAP
    # ======================================

    heatmap_resized = cv2.resize(
        heatmap_raw,
        IMAGE_SIZE,
        interpolation=cv2.INTER_LINEAR
    )

    heatmap_uint8 = np.uint8(
        255 * np.clip(heatmap_resized, 0, 1)
    )

    colored_heatmap = cv2.applyColorMap(
        heatmap_uint8,
        cv2.COLORMAP_JET
    )

    colored_heatmap = cv2.cvtColor(
        colored_heatmap,
        cv2.COLOR_BGR2RGB
    )

    # ======================================
    # 10. CREATE OVERLAY
    # ======================================

    overlay = cv2.addWeighted(
        original_array,
        0.6,
        colored_heatmap,
        0.4,
        0
    )

    # ======================================
    # 11. CLASS PROBABILITIES
    # ======================================

    pneumonia_probability = float(
        pneumonia_probability[0].numpy()
    )

    normal_probability = float(
        normal_probability[0].numpy()
    )

    probabilities = {
        "NORMAL": normal_probability,
        "PNEUMONIA": pneumonia_probability
    }

    confidence = probabilities[predicted_class]

    target_probability = probabilities[selected_class]

    # ======================================
    # 12. RETURN COMPLETE ANALYSIS
    # ======================================

    return {
        "predicted_class": predicted_class,
        "confidence": confidence,
        "probabilities": probabilities,

        "original_image": original_array,
        "heatmap": colored_heatmap,
        "heatmap_raw": heatmap_raw,
        "overlay": overlay,

        "target_class": selected_class,
        "probability": target_probability,

        "gradient_finite": gradient_finite,
        "model_name": "S2_011",
        "architecture": "MobileNetV2"
    }
