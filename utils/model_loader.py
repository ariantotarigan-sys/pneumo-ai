
from pathlib import Path
import json
import os
import tempfile
import zipfile

import streamlit as st
import tensorflow as tf


# ==========================================
# PNEUMO-AI | MODEL CONFIGURATION
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "S2_011_BEST.keras"

MODEL_NAME = "S2_011"
ARCHITECTURE = "MobileNetV2"

IMAGE_SIZE = (224, 224)
CLASS_NAMES = ["NORMAL", "PNEUMONIA"]

PREPROCESSING = "tf.keras.applications.mobilenet_v2.preprocess_input"


# ==========================================
# MODEL CONFIG COMPATIBILITY
# ==========================================

def clean_model_config(obj):
    """
    Menghapus quantization_config bernilai None
    dari konfigurasi layer Dense.

    Tidak mengubah bobot atau file model asli.
    """
    removed_count = 0

    if isinstance(obj, dict):

        if obj.get("class_name") == "Dense":
            layer_config = obj.get("config", {})

            if layer_config.get(
                "quantization_config", "MISSING"
            ) is None:
                del layer_config["quantization_config"]
                removed_count += 1

        for value in obj.values():
            removed_count += clean_model_config(value)

    elif isinstance(obj, list):

        for value in obj:
            removed_count += clean_model_config(value)

    return removed_count


def create_compatible_model_copy(source_path):
    """
    Membuat salinan sementara model .keras
    dengan metadata yang kompatibel dengan Keras.

    Mengembalikan:
    - temporary model path
    - jumlah metadata yang dibersihkan
    """

    fd, temporary_path = tempfile.mkstemp(suffix=".keras")
    os.close(fd)

    try:
        with zipfile.ZipFile(source_path, "r") as source:

            if "config.json" not in source.namelist():
                raise ValueError(
                    "config.json tidak ditemukan dalam file model."
                )

            config = json.loads(
                source.read("config.json")
            )

            removed_count = clean_model_config(config)

            with zipfile.ZipFile(
                temporary_path, "w"
            ) as target:

                for item in source.infolist():

                    if item.filename == "config.json":
                        data = json.dumps(
                            config
                        ).encode("utf-8")

                    else:
                        data = source.read(item.filename)

                    target.writestr(item, data)

        return temporary_path, removed_count

    except Exception:
        if os.path.exists(temporary_path):
            os.remove(temporary_path)
        raise


# ==========================================
# MODEL LOADER
# ==========================================

@st.cache_resource(show_spinner="Memuat model PNEUMO-AI...")
def load_model():

    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            f"File model tidak ditemukan: {MODEL_PATH}"
        )

    temporary_path = None

    try:
        temporary_path, removed_count = (
            create_compatible_model_copy(MODEL_PATH)
        )

        model = tf.keras.models.load_model(
            temporary_path,
            compile=False
        )

        if model.input_shape[-3:] != (224, 224, 3):
            raise ValueError(
                f"Input shape model tidak sesuai: {model.input_shape}"
            )

        if model.output_shape[-1] != 1:
            raise ValueError(
                f"Output model tidak sesuai: {model.output_shape}"
            )

        print(
            "[PNEUMO-AI] Model berhasil dimuat:",
            MODEL_NAME
        )
        print(
            "[PNEUMO-AI] Metadata dibersihkan:",
            removed_count
        )
        print(
            "[PNEUMO-AI] Jumlah parameter:",
            model.count_params()
        )

        return model

    finally:

        if (
            temporary_path is not None
            and os.path.exists(temporary_path)
        ):
            os.remove(temporary_path)


# ==========================================
# MODEL INFORMATION
# ==========================================

def get_model_info():

    return {
        "model_name": MODEL_NAME,
        "architecture": ARCHITECTURE,
        "model_path": str(MODEL_PATH),
        "image_size": IMAGE_SIZE,
        "class_names": CLASS_NAMES,
        "preprocessing": PREPROCESSING,
        "input_shape": (224, 224, 3),
        "output_shape": (1,),
        "framework": f"TensorFlow {tf.__version__}",
        "keras_version": tf.keras.__version__,
    }
