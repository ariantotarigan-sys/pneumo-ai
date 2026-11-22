
import hashlib
from datetime import datetime
import streamlit as st


# ==========================================
# PNEUMO-AI | SESSION MANAGER
# Integrated X-Ray Analysis & Grad-CAM
# Session-based storage
# ==========================================

SESSION_DEFAULTS = {
    "active_case": None,
    "prediction_history": [],
    "latest_analysis": None,
    "latest_gradcam": None,
}


def initialize_session():
    """Initialize session state safely."""

    for key, default_value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default_value.copy() if isinstance(
                default_value, (dict, list)
            ) else default_value


def calculate_image_hash(image_bytes):
    """Create SHA-256 identity for an uploaded image."""

    return hashlib.sha256(image_bytes).hexdigest()


def set_active_case(filename, image_bytes, image):
    """
    Register an uploaded image as the active analysis case.
    A different image creates a new case.
    """

    initialize_session()

    image_hash = calculate_image_hash(image_bytes)
    current_case = st.session_state.active_case

    # Reuse existing case if image content is identical
    if (
        current_case is not None
        and current_case["image_hash"] == image_hash
    ):
        return current_case

    case_id = image_hash[:16]

    case = {
        "case_id": case_id,
        "image_hash": image_hash,
        "filename": filename,
        "image_bytes": image_bytes,
        "original_image": image.copy(),
        "created_at": datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        ),
        "prediction": None,
        "gradcam_results": {},
    }

    st.session_state.active_case = case

    # Reset only the latest display references.
    # Historical records are preserved.
    st.session_state.latest_analysis = None
    st.session_state.latest_gradcam = None

    return case


def get_active_case():
    """Return the current active case."""

    initialize_session()
    return st.session_state.active_case


def save_prediction(result):
    """Save prediction result to the active case."""

    initialize_session()

    case = st.session_state.active_case

    if case is None:
        raise RuntimeError("Belum ada citra aktif.")

    case["prediction"] = result

    record = {
        "case_id": case["case_id"],
        "image_hash": case["image_hash"],
        "filename": case["filename"],
        "timestamp": datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        ),
        "predicted_class": result["predicted_class"],
        "confidence": result["confidence"],
        "probabilities": result["probabilities"],
    }

    st.session_state.latest_analysis = record

    # Prevent duplicate history entries for the same case
    history = st.session_state.prediction_history

    existing_index = next(
        (
            index
            for index, item in enumerate(history)
            if item["case_id"] == case["case_id"]
        ),
        None
    )

    if existing_index is None:
        history.insert(0, record)
    else:
        history[existing_index] = record

    return record


def get_prediction():
    """Get prediction for the active case."""

    case = get_active_case()

    if case is None:
        return None

    return case["prediction"]


def save_gradcam(target_class, result):
    """Save Grad-CAM result for the active case and target class."""

    initialize_session()

    case = st.session_state.active_case

    if case is None:
        raise RuntimeError("Belum ada citra aktif.")

    target_class = target_class.upper()

    if target_class not in ("NORMAL", "PNEUMONIA"):
        raise ValueError("Target class tidak valid.")

    case["gradcam_results"][target_class] = result

    st.session_state.latest_gradcam = {
        "case_id": case["case_id"],
        "target_class": target_class,
        "result": result,
    }

    return result


def get_gradcam(target_class):
    """Retrieve cached Grad-CAM for the active case."""

    case = get_active_case()

    if case is None:
        return None

    return case["gradcam_results"].get(
        target_class.upper()
    )


def clear_active_case():
    """Clear active case without deleting session history."""

    initialize_session()

    st.session_state.active_case = None
    st.session_state.latest_analysis = None
    st.session_state.latest_gradcam = None


def clear_session_history():
    """Clear prediction history explicitly."""

    initialize_session()

    st.session_state.prediction_history = []
