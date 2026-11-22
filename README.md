# PNEUMO-AI

Research prototype for binary chest X-ray image classification (NORMAL / PNEUMONIA) using MobileNetV2 experiment S2_011, with Grad-CAM explainability.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Project contents

- `app.py` — Streamlit application
- `models/S2_011_BEST.keras` — selected model checkpoint
- `utils/` — preprocessing, prediction, model loading, session and Grad-CAM utilities
- `dataset_gallery/` — 10 NORMAL and 10 PNEUMONIA training-image examples with `manifest.csv`

## Deployment

Deploy this repository using Streamlit Community Cloud and set the main file path to `app.py`.

Before making the repository public, verify that the original dataset license and terms permit redistribution/display of the selected images. Do not upload patient-identifiable images or private records. Keep secrets out of the repository.

## Research and medical-use notice

PNEUMO-AI is a research and educational prototype, not a medical device or clinical diagnostic system. Its predictions and Grad-CAM visualizations must not be used as the sole basis for diagnosis or treatment decisions. Clinical interpretation must be performed by qualified healthcare professionals.
