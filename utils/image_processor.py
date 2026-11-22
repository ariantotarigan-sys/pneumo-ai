
from PIL import Image
import numpy as np

# ==========================================
# PNEUMO-AI | IMAGE PROCESSOR
# ==========================================

IMAGE_SIZE = (224, 224)


def preprocess_image(image):
    """
    Memproses citra X-Ray agar sesuai dengan
    input model MobileNetV2 S2_011.

    Parameters
    ----------
    image : PIL.Image

    Returns
    -------
    numpy.ndarray
        Shape: (1, 224, 224, 3)
        Range: [-1, 1]
    """

    # Pastikan format RGB
    image = image.convert("RGB")

    # Resize sesuai input model
    image = image.resize(
        IMAGE_SIZE,
        Image.Resampling.BILINEAR
    )

    # Konversi ke array float32
    image_array = np.asarray(
        image,
        dtype=np.float32
    )

    # Preprocessing MobileNetV2
    image_array = image_array / 127.5 - 1.0

    # Tambahkan batch dimension
    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    return image_array
